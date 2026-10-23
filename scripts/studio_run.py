#!/usr/bin/env python3
"""Isolated Studio runner: one fresh executor per operation (studio/execution.md).

A workspace holds a Project Context in <ws>/project and one record directory per operation in
<ws>/records.

  studio_run.py init   <ws> --from <fixture-dir>
  studio_run.py intake <ws> "<owner request>"
  studio_run.py next   <ws>                 # Step (+ dry-run simulator), then Route: separate executors
  studio_run.py run    <ws> [--max-ops 25]  # repeat until done, Owner escalation, or a stop condition
  studio_run.py step   <ws>  |  route <ws>  |  simulate <ws>   # simulate: re-run the dry-run simulator
  studio_run.py decide <ws> "<owner words>" # Resume after an Owner escalation
  studio_run.py replay <ws> <record-dir>    # re-run a recorded Route packet; compare the decision
  studio_run.py packet <ws> step|route      # print the packet that would be sent; run nothing
  studio_run.py status <ws>

Options: --runtime claude|codex, --model NAME, --goal G-NNN, --handoff FILE (parallel steps).
"""

import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDIO = ROOT / "studio"
ROLES = sorted(p.stem for p in (STUDIO / "roles").glob("*.md"))
PARTICIPANTS = set(ROLES) | {"studio", "owner"}
REQUIRED = {
    "handoff": [
        "Task",
        "Context",
        "Findings",
        "Decisions already made",
        "Constraints",
        "Open questions",
        "Expected output",
        "Load",
    ],
    "escalation": [
        "Question",
        "Why this needs the Owner",
        "Options",
        "Studio recommendation",
        "Reasoning",
        "Owner decision required",
    ],
    "decision": ["Decision", "Rationale", "Alternatives considered", "Revisit when"],
    "goal": [
        "Owner request",
        "Interpretation",
        "Unknowns",
        "Route",
        "Route changes",
        "Next action",
        "Outcome",
    ],
}
SELF_ASSESSMENT = re.compile(
    r"(?i)\b(root cause|own tests?|tests? (all )?pass(ed|es)?|confiden(t|ce))\b"
)
BLOCK = re.compile(r"^<<<FILE (\S+)[ \t]*\n(.*?)^>>>END[ \t]*$", re.M | re.S)
SYSTEM_PROMPT = (
    "You execute one operation of a game-development studio process. Everything you "
    "need is in the user's message; follow it exactly."
)
SIMULATOR = """You are the dry-run build simulator. You are not a Studio Role and make no decisions.

The game does not exist; its build and code are described in text. A change was just implemented.
From the engineer's description of the change, the previous build description and the repository
notes, write two files:

1. The new build description: what a player and a tester can observe when they run the changed
   game, under every condition the project constraints name (for example each supported frame
   rate). Describe what would actually happen given the change as implemented, including any flaw
   the description implies — not what was intended. Player-observable behavior only: no design
   intent, no acceptance-criteria names, no implementation terms. Do not copy HTML comments.
   Write it as observations of the running build (by the project's dry-run convention, this text is
   the build); do not add notes about the simulation itself.
2. The updated repository notes: implementation facts after the change.

Write each file as a file block (<<<FILE <path> ... >>>END) using exactly the paths under
"You may write". Text outside file blocks is discarded."""


class Rejected(Exception):
    """An operation's input or output breaks a Studio rule. Nothing is written."""


# --- Markdown artifacts ------------------------------------------------------------------------


def parse(text):
    """Flat frontmatter (`key: value`, ` #` starts a comment) and body."""
    if not text.startswith("---\n"):
        return {}, text
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.split(" #")[0].strip()
    return meta, body


def items(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def slug(heading):
    return re.sub(r"[^a-z0-9-]", "", heading.lower().replace(" ", "-"))


def _sections(text):
    marks = [
        (m.start(), m.group(1).strip()) for m in re.finditer(r"^## (.+)$", text, re.M)
    ]
    return [
        (name, start, marks[i + 1][0] if i + 1 < len(marks) else len(text))
        for i, (start, name) in enumerate(marks)
    ]


def headings(text):
    return {name for name, _, _ in _sections(text)}


def section(text, name):
    for heading, start, end in _sections(text):
        if heading == name:
            return text[start:end].split("\n", 1)[1] if "\n" in text[start:end] else ""
    return ""


def extract(text, anchor):
    for heading, start, end in _sections(text):
        if slug(heading) == anchor:
            return text[start:end]
    raise Rejected(f"no section #{anchor}")


def strip(text, names):
    for heading, start, end in reversed(_sections(text)):
        if heading in names:
            text = text[:start] + text[end:]
    return text


def load_entries(text):
    """Load list entries: Markdown files (with an optional `#section`, normalized to the heading
    slug) and files of any type given with a directory, such as build sources (`repo/game.py`).
    """
    entries = re.findall(
        r"[\w./-]+\.md(?:#[\w-]+)?|[\w.-]+/[\w./-]*\.\w+",
        section(parse(text)[1], "Load"),
    )
    return [
        e.partition("#")[0] + ("#" + slug(e.partition("#")[2]) if "#" in e else "")
        for e in entries
    ]


def route_rows(goal_text):
    rows = []
    for line in section(goal_text, "Route").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and re.fullmatch(r"\d+\S*", cells[0]):
            # The file name of the incoming Handoff; tolerate links, paths and trailing notes.
            name = re.search(r"\d{2,}-[\w-]+\.md", cells[5])
            cells[5] = name.group(0) if name else cells[5]
            rows.append(
                dict(zip(["n", "stage", "role", "skills", "status", "handoff"], cells))
            )
    return rows


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


# --- Project Context ---------------------------------------------------------------------------


def resolve(project, entry):
    file, _, anchor = entry.partition("#")
    return (ROOT / file if file.startswith("studio/") else project / file), anchor


def read_entry(project, entry):
    path, anchor = resolve(project, entry)
    if not path.is_file():
        raise Rejected(f"Load entry does not exist: {entry}")
    text = path.read_text(encoding="utf-8")
    return extract(text, anchor) if anchor else text


def role_policy(role):
    meta, body = parse((STUDIO / "roles" / f"{role}.md").read_text(encoding="utf-8"))
    policy = {
        k: items(meta.get(k))
        for k in (
            "receives_from",
            "load_only",
            "load_forbid",
            "strip_sections",
            "writes",
            "runs",
        )
    }
    policy["escalates"] = "prepare-owner-escalation" in section(body, "Typical skills")
    return policy


def matches(entry, patterns, project_meta):
    expanded = []
    for pattern in patterns:
        expanded += (
            items(project_meta.get("player_visible"))
            if pattern == "@player_visible"
            else [pattern]
        )
    return any(fnmatch.fnmatch(entry, p) for p in expanded)


def project_meta(project):
    return parse((project / "project.md").read_text(encoding="utf-8"))[0]


def run_commands(project):
    """The build commands a project declares (`run_<name>: <command>`), if it has a build."""
    meta = project_meta(project)
    if not meta.get("build"):
        return {}
    return {k[4:]: v for k, v in meta.items() if k.startswith("run_") and v}


def goal_dir(project, goal_id=None):
    dirs = sorted((project / "goals").glob("G-*"), key=lambda d: d.name)
    if goal_id:
        dirs = [d for d in dirs if d.name.startswith(goal_id + "-")]
    if not dirs:
        raise Rejected(f"no goal {goal_id or ''} in {project}")
    return dirs[-1]


def seq_of(path):
    """The number an artifact's file name starts with (two digits, more past 99)."""
    return int(re.match(r"\d+", Path(path).name).group())


def goal_artifacts(gdir):
    found = []
    for path in gdir.glob("[0-9][0-9]*-*.md"):
        if not re.match(r"\d+-", path.name):
            continue
        meta, _ = parse(path.read_text(encoding="utf-8"))
        seq = str(meta.get("seq", ""))
        found.append((int(seq) if seq.isdigit() else seq_of(path), path, meta))
    return [(p, m) for _, p, m in sorted(found, key=lambda f: f[0])]


def next_seq(gdir):
    return max([seq_of(p) for p, _ in goal_artifacts(gdir)] + [0]) + 1


def next_decision(project):
    nums = [
        int(p.name[2:5]) for p in (project / "decisions").glob("D-[0-9][0-9][0-9]-*.md")
    ]
    return f"D-{max(nums + [0]) + 1:03d}"


def owner_request(gdir):
    text = (gdir / "goal.md").read_text(encoding="utf-8")
    return "\n".join(
        l.lstrip("> ").rstrip()
        for l in section(text, "Owner request").strip().splitlines()
    ).strip()


def project_files(project):
    return "\n".join(
        sorted(str(p.relative_to(project)) for p in project.rglob("*") if p.is_file())
    )


def decision_titles(project):
    lines = []
    for path in sorted((project / "decisions").glob("D-*.md")):
        title = next(
            (
                l[2:]
                for l in path.read_text(encoding="utf-8").splitlines()
                if l.startswith("# ")
            ),
            "",
        )
        lines.append(f"{path.relative_to(project)} — {title}")
    return "\n".join(lines) or "none"


def open_handoffs(gdir):
    rows = route_rows((gdir / "goal.md").read_text(encoding="utf-8"))
    return [
        gdir / r["handoff"]
        for r in rows
        if r["status"].lower().startswith("open")
        and r["role"] in ROLES
        and r["handoff"] != "—"
    ]


# --- Rules -------------------------------------------------------------------------------------


def check_artifact(project, name, text, request=None, full=True, pending=None):
    """Structural rules for a handoff or escalation; with full=True also Load and recipient policy.

    `pending` holds files the same operation is about to write; Load entries may point at them.
    """
    meta, body = parse(text)
    kind, errors = meta.get("kind"), []
    if kind not in ("handoff", "escalation"):
        return [f"{name}: kind must be handoff or escalation"]
    missing = set(REQUIRED[kind]) - headings(body)
    if missing:
        errors.append(f"{name}: missing sections {sorted(missing)}")
    if meta.get("from") not in PARTICIPANTS or meta.get("to") not in PARTICIPANTS:
        errors.append(f"{name}: from/to must be Role ids, studio or owner")
    elif (
        not str(meta.get("seq", "")).isdigit()
        or Path(name).name
        != f"{int(meta['seq']):02d}-{meta['from']}-to-{meta['to']}.md"
    ):
        errors.append(
            f"{name}: filename must be NN-<from>-to-<to>.md matching seq/from/to"
        )
    if kind == "escalation" or not full or meta.get("to") not in ROLES:
        return errors
    to, loads, pmeta = meta["to"], load_entries(text), project_meta(project)
    for entry in loads:
        path, anchor = resolve(project, entry)
        content = (pending or {}).get(entry.partition("#")[0])
        if content is None and path.is_file():
            content = path.read_text(encoding="utf-8")
        if content is None:
            in_goal = Path(name).parent / entry.partition("#")[0]
            if "/" not in entry and (project / in_goal).is_file():
                hint = f"did you mean {in_goal}? Paths are relative to the project"
            else:
                folder = path.parent
                nearby = (
                    sorted(f.name for f in folder.glob("*") if f.is_file())
                    if folder.is_dir()
                    else []
                )
                hint = f"existing files there: {', '.join(nearby) or 'none'}"
            errors.append(f"{name}: Load entry missing: {entry} ({hint})")
        elif anchor and anchor not in {slug(h) for h in headings(content)}:
            have = ", ".join(f"#{slug(h)}" for h in headings(content)) or "none"
            errors.append(
                f"{name}: Load section missing: {entry} (only `## ` headings can be loaded as "
                f"sections; this file has: {have}; or load the whole file)"
            )
    if f"studio/roles/{to}.md" not in loads:
        errors.append(f"{name}: Load must include studio/roles/{to}.md")
    policy = role_policy(to)
    if policy["receives_from"] and meta["from"] not in policy["receives_from"]:
        errors.append(
            f"{name}: {to} only receives Handoffs from {policy['receives_from']}"
        )
    for entry in loads:
        if policy["load_only"] and not matches(entry, policy["load_only"], pmeta):
            errors.append(f"{name}: {to} may not load {entry}")
        if policy["load_forbid"] and matches(entry, policy["load_forbid"], pmeta):
            errors.append(f"{name}: {to} may not load {entry}")
    if to == "playtester":
        if request and request in body:
            errors.append(f"{name}: the Owner request must not reach the Playtester")
        if re.search(r"\bD-\d{3}\b", body) or "## Sender assessment" in body:
            errors.append(
                f"{name}: Decisions and Sender assessment must not reach the Playtester"
            )
    if to == "qa" and meta["from"] == "gameplay-engineer":
        if SELF_ASSESSMENT.search(strip(body, ["Sender assessment", "Load"])):
            errors.append(
                f"{name}: implementer self-assessment belongs under ## Sender assessment"
            )
    return errors


def check_goal(text):
    meta, body = parse(text)
    errors = []
    if meta.get("kind") != "goal":
        errors.append("goal.md: kind must be goal")
    if meta.get("status") not in ("active", "blocked-on-owner", "done", "abandoned"):
        errors.append("goal.md: invalid status")
    missing = set(REQUIRED["goal"]) - headings(body)
    if missing:
        errors.append(f"goal.md: missing sections {sorted(missing)}")
    if "budget" in meta and not (meta["budget"].isdigit() and int(meta["budget"]) > 0):
        errors.append(
            "goal.md: budget must be a whole number of operations (e.g. budget: 30)"
        )
    for row in route_rows(body):
        if row["role"] not in PARTICIPANTS:
            errors.append(
                f"goal.md: route row {row['n']} has unknown role {row['role']}; a Role cell holds "
                "exactly one role id (or studio, owner), and a parallel step gets its own row (5, 5b)"
            )
    return errors


ROUTE_CHANGES_MAX, UNKNOWNS_MAX, CELL_MAX, GOAL_MAX_BYTES = 600, 3000, 80, 20_000
DEFAULT_BUDGET = 40  # for Goals written before budgets existed


def goal_budget(text):
    raw = parse(text)[0].get("budget", "")
    return int(raw) if raw.isdigit() and int(raw) > 0 else DEFAULT_BUDGET


def goal_ops(records, gid):
    """Operations (Intake, Steps, Routes, Resumes) the runtime has run on this Goal."""
    if not records or not records.is_dir():
        return 0
    count = 0
    for path in records.glob("*/record.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        count += bool(
            record.get("op") in ("Intake", "Step", "Route", "Resume")
            and str(record.get("goal", "")).startswith(gid)
            and record.get("attempts")
        )
    return count


def budget_line(used, budget):
    return f"{used} of {budget} operations used" + (
        " — over budget: add no stages except a game-director step that cuts the remaining "
        "work to what the Owner request needs, or an owner step that escalates the cost; planned "
        "steps may still be opened"
        if used >= budget
        else ""
    )


def check_goal_size(text):
    """goal.md holds the current state only; the history lives in log.md."""
    errors = []
    changes = section(text, "Route changes").strip()
    if len(changes) > ROUTE_CHANGES_MAX:
        errors.append(
            f"goal.md: ## Route changes has {len(changes)} characters (limit {ROUTE_CHANGES_MAX}); "
            "write only this operation's change in 1-3 lines, the runtime keeps the history in log.md"
        )
    unknowns = section(text, "Unknowns").strip()
    if len(unknowns) > UNKNOWNS_MAX:
        errors.append(
            f"goal.md: ## Unknowns has {len(unknowns)} characters (limit {UNKNOWNS_MAX}); keep what is "
            "still unknown and why each stage exists, not the story of earlier passes (log.md and the "
            "Handoffs keep it)"
        )
    for row in route_rows(text):
        for cell in ("stage", "status"):
            if len(row[cell]) > CELL_MAX:
                errors.append(
                    f"goal.md: route row {row['n']} {cell} cell has {len(row[cell])} characters "
                    f"(limit {CELL_MAX}); put the details in the Handoff"
                )
    size = len(strip(text, ["Outcome"]).encode())
    if size > GOAL_MAX_BYTES:
        errors.append(
            f"goal.md is {size} bytes without its Outcome (limit {GOAL_MAX_BYTES}); "
            "shorten it, the Handoffs and log.md carry the details"
        )
    return errors


KEPT_WHY = {
    "Owner request": "the Owner's words never change",
    "Interpretation": "reinterpreting the Goal is the Owner's decision, so escalate instead",
}


def check_kept(before, after, names):
    """Sections an operation must leave as they were (whitespace aside)."""
    return [
        f"goal.md: keep ## {name} exactly as it was; {KEPT_WHY[name]}"
        for name in names
        if section(before, name).split() != section(after, name).split()
    ]


CURRENT_STATE_MAX = 1_500


def check_project_update(before, after, closing):
    """At Close the Studio refreshes project.md's Current state; the rest belongs to the Owner."""
    if not closing:
        return [
            "project.md: update ## Current state only at Close (the Route that sets the Goal "
            "done or abandoned)"
        ]
    errors = []
    if parse(before)[0] != parse(after)[0]:
        errors.append("project.md: keep the frontmatter as it was")
    names = sorted((headings(before) | headings(after)) - {"Current state"})
    errors += [
        f"project.md: keep ## {name} as it was; only ## Current state changes at Close"
        for name in names
        if section(before, name).split() != section(after, name).split()
    ]
    rest = lambda text: text.replace(section(text, "Current state"), "", 1).split()
    if not errors and rest(before) != rest(after):
        errors.append("project.md: change only the text of ## Current state")
    size = len(section(after, "Current state").strip())
    if size > CURRENT_STATE_MAX:
        errors.append(
            f"project.md: ## Current state has {size} characters (limit 1,500); say what exists "
            "now (build, content, known problems, how to run it), not how it came about"
        )
    return errors


def check_decision(name, text, decided_by=None):
    meta, body = parse(text)
    errors = (
        [
            f"{name}: missing sections {sorted(set(REQUIRED['decision']) - headings(body))}"
        ]
        if set(REQUIRED["decision"]) - headings(body)
        else []
    )
    if (
        meta.get("kind") != "decision"
        or not meta.get("id")
        or not Path(name).name.startswith(meta["id"] + "-")
    ):
        errors.append(f"{name}: kind/id must match the filename")
    if decided_by and meta.get("decided_by") != decided_by:
        errors.append(f"{name}: decided_by must be {decided_by}")
    return errors


def check_writes(files, patterns, project, create_only=()):
    errors = []
    for path in files:
        if path.startswith("/") or ".." in Path(path).parts:
            errors.append(f"{path}: paths must be inside the project")
        elif not any(fnmatch.fnmatch(path, p) for p in patterns):
            errors.append(f"{path}: not on the write list")
        elif (
            any(fnmatch.fnmatch(path, p) for p in create_only)
            and (project / path).exists()
        ):
            errors.append(f"{path}: may only create new files here")
    return errors


def check_open_steps(project, gdir_rel, files, request):
    """After Route/Resume/Intake: every open step's Handoff must satisfy the recipient's policy."""
    goal_text = files[f"{gdir_rel}/goal.md"]
    errors = []
    status = parse(goal_text)[0].get("status")
    opened = [
        r
        for r in route_rows(goal_text)
        if r["status"].lower().startswith("open") and r["role"] in ROLES
    ]
    if status == "active" and not opened:
        errors.append(
            "goal.md: an active Goal needs its next step marked `open` with its Handoff"
        )
    for row in route_rows(goal_text):
        if row["status"].lower().startswith("open") and row["role"] in ROLES:
            name = f"{gdir_rel}/{row['handoff']}"
            text = files.get(name) or (
                (project / name).read_text(encoding="utf-8")
                if (project / name).is_file()
                else None
            )
            if text is None:
                errors.append(
                    f"open step {row['n']}: handoff {row['handoff']} does not exist"
                )
                continue
            if parse(text)[0].get("to") != row["role"]:
                errors.append(
                    f"open step {row['n']}: {row['handoff']} is not addressed to {row['role']}"
                )
            errors += check_artifact(project, name, text, request, pending=files)
    return errors


def decision_summary(files):
    """What the Studio decided, from an operation's output files only."""
    summary = {}
    for path, text in files.items():
        meta, body = parse(text)
        if path.endswith("/goal.md"):
            summary["status"] = meta.get("status")
            summary["open"] = [
                (r["role"], r["stage"])
                for r in route_rows(body)
                if r["status"].lower().startswith("open")
            ]
        elif (
            meta.get("kind") in ("handoff", "escalation")
            and meta.get("from") == "studio"
        ):
            summary["new"] = (meta.get("to"), meta.get("stage"))
    return summary


# --- Packets -----------------------------------------------------------------------------------


class Packet:
    def __init__(self, op, **header):
        self.op, self.header, self.inputs, self.writes = op, header, [], []
        self.allow_need = False
        # Run requests (Steps of Roles that may run the build): see run_round().
        self.runs, self.build, self.write_patterns, self.rounds = [], None, [], 0
        self.proposed, self.run_log, self.base_inputs = {}, [], None
        # The answer's shape, repeated after every input (answer_shape); a Step's outgoing
        # Handoff pattern (build_check).
        self.answer, self.out = "", None
        self.strip_names = ()  # sections removed from Handoffs added by @need (Steps)

    def add(self, label, content):
        self.inputs.append((label, content.rstrip() + "\n"))

    def add_entry(self, project, entry, strip_names=()):
        text = read_entry(project, entry)
        if strip_names and entry.startswith("goals/"):
            text = strip(text, strip_names)
        self.add(entry, text)

    def add_studio_context(self, project, templates):
        for entry in (
            "studio/README.md",
            "studio/orchestration.md",
            "studio/workflows/development-loop.md",
        ):
            self.add_entry(project, entry)
        for role in ROLES:
            text = (STUDIO / "roles" / f"{role}.md").read_text(encoding="utf-8")
            for anchor in ("works-from", "independence"):
                if anchor in {slug(h) for h in headings(text)}:
                    self.add(f"studio/roles/{role}.md#{anchor}", extract(text, anchor))
        for name in templates:
            self.add_entry(project, f"studio/templates/{name}.md")
        self.add_entry(project, "project.md")
        self.add("@project-files", project_files(project))
        self.add("@decision-titles", decision_titles(project))

    def render(self):
        head = "# Studio operation packet\n\n" + "".join(
            f"{k}: {v}\n" for k, v in self.header.items()
        )
        head += (
            "\n## You may write\n\n"
            + "".join(f"- {w}\n" for w in self.writes)
            + "\n## Inputs\n\n"
        )
        body = "\n".join(
            f"<<<FILE {label}\n{content}>>>END\n" for label, content in self.inputs
        )
        return (
            head + body + (f"\n## Your answer\n\n{self.answer}" if self.answer else "")
        )

    def manifest(self):
        return [
            {"path": label, "sha256": sha(content), "bytes": len(content.encode())}
            for label, content in self.inputs
        ]


def answer_shape(out, escalates, checked=False):
    """A short reminder at the very end of a Step packet, after long inputs and run results."""
    lines = [
        f"- Write the outgoing Handoff as {out.replace('*', '<recipient>')} with every section of "
        f"studio/templates/handoff.md, in this order: {', '.join(REQUIRED['handoff'])}. Your own "
        "report goes inside Findings. Address it to the recipient the incoming Handoff's "
        "Expected output names, if it names one."
    ]
    if escalates:
        lines.append(
            "- An Escalation instead keeps the sections of studio/templates/escalation.md: "
            + ", ".join(REQUIRED["escalation"])
            + "."
        )
    if checked:
        lines.append(
            "- The runtime tests the build as you write it and adds the result to your Handoff "
            "(## Build check): you need not ask for another test run after your final answer. If "
            "the work is not finished, say what remains and set outcome: partial."
        )
    lines.append(
        "- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output "
        "protocol in studio/execution.md)."
    )
    return "\n".join(lines) + "\n"


def executor_instructions():
    return extract(
        (STUDIO / "execution.md").read_text(encoding="utf-8"), "executor-instructions"
    )


def current_build(project):
    """The build Verify and Play observe: the project's build directory, or the newest simulated one."""
    build = project_meta(project).get("build")
    if build:
        digest = hashlib.sha256()
        for path in sorted(p for p in (project / build).rglob("*") if p.is_file()):
            digest.update(str(path.relative_to(project)).encode() + path.read_bytes())
        digest = digest.hexdigest()
        return f"{build}/ (sha {digest[:12]}; run through the project's run commands)"
    builds = sorted(
        (project / "sim").glob("build-*.md"),
        key=lambda p: [int(x) for x in re.findall(r"\d+", p.stem)],
    )
    return (
        f"{builds[-1].relative_to(project)} (newest simulated build; older ones are history)"
        if builds
        else None
    )


def new_packet(op, **header):
    packet = Packet(op, operation=op, **header)
    packet.add("studio/execution.md#executor-instructions", executor_instructions())
    return packet


def build_intake(project, request):
    number = f"G-{len(list((project / 'goals').glob('G-*'))) + 1:03d}"
    packet = new_packet(
        "Intake",
        goal=f"{number} (new)",
        owner_language=project_meta(project).get("owner_language", ""),
    )
    packet.add_studio_context(project, ["goal", "handoff"])
    packet.add("@owner-request", request)
    packet.writes = [
        f"goals/{number}-<slug>/goal.md",
        f"goals/{number}-<slug>/01-studio-to-<role>.md",
    ]

    def validate(files):
        dirs = {str(Path(p).parent) for p in files}
        errors = (
            []
            if len(dirs) == 1
            and re.fullmatch(rf"goals/{number}-[a-z0-9-]+", next(iter(dirs)))
            else [f"write exactly goal.md and one handoff in goals/{number}-<slug>/"]
        )
        if errors:
            return errors
        gdir = dirs.pop()
        errors += check_writes(
            files, [f"{gdir}/goal.md", f"{gdir}/01-studio-to-*.md"], project
        )
        if f"{gdir}/goal.md" not in files:
            return errors + ["goal.md missing"]
        errors += check_goal(files[f"{gdir}/goal.md"])
        errors += check_goal_size(files[f"{gdir}/goal.md"])
        if "budget" not in parse(files[f"{gdir}/goal.md"])[0]:
            errors.append(
                "goal.md: set budget: <operations> in the frontmatter, the Steps and Routes this "
                "Goal should need (orchestration.md, Intake step 7)"
            )
        if request.strip() not in files[f"{gdir}/goal.md"]:
            errors.append("goal.md must quote the Owner request verbatim")
        return errors + check_open_steps(project, gdir, files, request)

    return packet, validate


def build_step(project, gdir, handoff):
    text = handoff.read_text(encoding="utf-8")
    meta = parse(text)[0]
    role, rel = meta.get("to"), str(handoff.relative_to(project))
    if meta.get("kind") != "handoff" or role not in ROLES:
        raise Rejected(f"{rel} is not a handoff to a Role")
    errors = check_artifact(project, rel, text, owner_request(gdir))
    if errors:
        raise Rejected("incoming handoff breaks the rules:\n" + "\n".join(errors))
    policy, seq, gid = role_policy(role), next_seq(gdir), gdir.name[:5]
    packet = new_packet("Step", goal=gid, role=role, incoming_handoff=rel, next_seq=seq)
    packet.add_entry(project, rel, policy["strip_sections"])
    for entry in load_entries(text):
        if entry != rel:
            packet.add_entry(project, entry, policy["strip_sections"])
    for label, listing in directory_listings(project, text, role):
        packet.add(label, listing)
    templates = (
        ["handoff"]
        + (["escalation"] if policy["escalates"] else [])
        + (["decision"] if "decisions/*" in policy["writes"] else [])
    )
    for name in templates:
        packet.add_entry(project, f"studio/templates/{name}.md")
    out = f"goals/{gdir.name}/{seq:02d}-{role}-to-*.md"
    decision, build = next_decision(project), project_meta(project).get("build")
    extra = []
    for w in policy["writes"]:
        if w == "@build":
            extra += [f"{build}/*"] if build else []
        else:
            extra.append(f"decisions/{decision}-*.md" if w == "decisions/*" else w)
    packet.writes = [out.replace("*", "<recipient>")] + [
        w.replace("*", "<path> (full file content)" if w == f"{build}/*" else "<name>")
        for w in extra
    ]
    commands = run_commands(project)
    packet.out = out
    packet.answer = answer_shape(
        out,
        policy["escalates"],
        bool(build) and "@build" in policy["writes"] and "tests" in commands,
    )
    runs = [r for r in policy["runs"] if r in commands]
    if runs:
        packet.runs, packet.build, packet.write_patterns = runs, build, [out] + extra
        packet.header["runs"] = f"{', '.join(runs)} (up to {MAX_RUNS} rounds)"
        for name in runs:
            packet.header[f"run_{name}"] = commands[name]
        packet.writes.append(
            f"@run/<{'|'.join(runs)}>[/<label>]: instead of your final files, up to {MAX_RUNS} "
            "times: one block per run, holding its input script for a command with {script} (empty "
            f"otherwise), plus any {build}/ files you may write that the run should use. A new "
            "executor gets the results and must write every file to keep in its final answer "
            "(EDIT blocks always apply to the project files as written, never to a proposal)"
        )
    packet.allow_need, packet.strip_names = True, policy["strip_sections"]
    packet.header["context_request"] = f"allowed once (@need, up to {MAX_NEED} paths)"
    packet.writes.append(
        f"@need: instead of your files, once: a file block `<<<FILE @need` with one path per line "
        f"(up to {MAX_NEED} project or Studio files your Role may load), then `>>>END`, to add "
        "them to this packet"
    )

    def validate(files):
        errors = check_writes(
            files, [out] + extra, project, create_only=["decisions/*"]
        )
        artifacts = [p for p in files if fnmatch.fnmatch(p, out)]
        if len(artifacts) != 1:
            return errors + [
                "write exactly one outgoing handoff or escalation"
                + (
                    "; to try proposed build files first, add @run/<name> blocks instead"
                    if packet.runs
                    and any(p.startswith(f"{packet.build}/") for p in files)
                    else ""
                )
            ]
        ameta = parse(files[artifacts[0]])[0]
        if (
            ameta.get("from") != role
            or ameta.get("goal") != gid
            or str(ameta.get("seq")) != str(seq)
        ):
            errors.append(
                f"outgoing artifact must have from: {role}, goal: {gid}, seq: {seq}"
            )
        errors += check_artifact(project, artifacts[0], files[artifacts[0]], full=False)
        for path in files:
            if path.startswith("decisions/"):
                errors += check_decision(path, files[path], decided_by=role)
        return errors

    return packet, validate


STUDIO_OPS = ("Intake", "Route", "Resume")
MAX_NEW_HANDOFFS = 3
MAX_NEED = 8
LOG_RECENT = 5
LOG_HEAD = (
    "# Goal log\n\nOne entry per Intake, Route and Resume, appended by whoever runs the operation.\n"
    "Entries are never edited.\n"
)


def log_recent(gdir):
    """The last LOG_RECENT entries of the Goal log (None if there is no log), and the entry count."""
    log = gdir / "log.md"
    if not log.is_file():
        return None, 0
    text = log.read_text(encoding="utf-8")
    entries = _sections(text)
    return (text[entries[-LOG_RECENT:][0][1] :] if entries else ""), len(entries)


def append_log(gdir, name, before=None):
    """Append the operation's entry to the Goal log. Only the runtime writes it: no write list has it."""
    log, text = gdir / "log.md", (gdir / "goal.md").read_text(encoding="utf-8")
    if not log.exists():
        old = section(before or "", "Route changes").strip()
        log.write_text(
            LOG_HEAD + (f"\n## Before the log\n\n{old}\n" if old else ""),
            encoding="utf-8",
        )
    opened = ", ".join(h.name for h in open_handoffs(gdir)) or "none"
    with log.open("a", encoding="utf-8") as f:
        f.write(
            f"\n## {name} · {datetime.date.today().isoformat()}\n\n"
            f"Status: {parse(text)[0].get('status')}. Open: {opened}.\n\n"
            f"{section(text, 'Route changes').strip() or '—'}\n"
        )


def add_log(packet, gdir, grel):
    recent, count = log_recent(gdir)
    if recent is not None:
        packet.header["log"] = (
            f"last {min(count, LOG_RECENT)} of {count} entries in @log-recent; "
            f"the full history is {grel}/log.md"
        )
        packet.add("@log-recent", recent or "(no entries yet)")


def seen_through(records, gid):
    """Highest artifact seq the last Studio operation on this goal had in view (None if unknown)."""
    if not records or not records.is_dir():
        return None
    for rec in sorted(records.iterdir(), reverse=True):
        path = rec / "record.json"
        if not path.is_file():
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        if (
            record.get("op") in STUDIO_OPS
            and str(record.get("goal", "")).startswith(gid)
            and record.get("status") == "ok"
        ):
            return record.get("seen_through_seq")
    return None


def unseen(gdir, seen):
    """Artifacts after seq `seen`; with no Studio operation on record (a Goal run by hand so far),
    the artifacts goal.md does not name yet."""
    artifacts = goal_artifacts(gdir)
    if seen is None:
        named = (gdir / "goal.md").read_text(encoding="utf-8")
        return [(p, m) for p, m in artifacts if p.name not in named]
    return [(p, m) for p, m in artifacts if seq_of(p) > seen]


LISTING_MAX = 80


def directory_listings(project, text, role):
    """A Load entry that names a directory (e.g. "the build in repo/") brings no file. List the
    names of the files in it that the Role may load, so the Step can ask for them with @need.
    """
    policy, pmeta, listings = role_policy(role), project_meta(project), []
    for token in dict.fromkeys(
        re.findall(r"[\w.-]+(?:/[\w.-]*)+", section(parse(text)[1], "Load"))
    ):
        folder, _ = resolve(project, token.rstrip("/"))
        if not folder.is_dir():
            continue
        base = ROOT if token.startswith("studio/") else project
        names = [
            str(f.relative_to(base))
            for f in sorted(folder.rglob("*"))
            if f.is_file() and "__pycache__" not in f.parts
        ]
        names = [
            n
            for n in names
            if not (policy["load_only"] and not matches(n, policy["load_only"], pmeta))
            and not (policy["load_forbid"] and matches(n, policy["load_forbid"], pmeta))
        ]
        if names:
            more = len(names) - LISTING_MAX
            listings.append(
                (
                    f"@files/{token.rstrip('/')}",
                    "Files in this directory (names only, not their contents; ask for the ones "
                    "you need with @need):\n\n"
                    + "".join(f"- {n}\n" for n in names[:LISTING_MAX])
                    + (f"- … and {more} more\n" if more > 0 else ""),
                )
            )
    return listings


def check_need(project, entries, role=None):
    """A one-time request for more context: project or Studio files only, and for a Step only what
    its Role may load."""
    errors = [] if entries else ["@need lists no paths"]
    if role:
        policy, pmeta = role_policy(role), project_meta(project)
        errors += [
            f"@need: {role} may not load {entry}"
            for entry in entries
            if (policy["load_only"] and not matches(entry, policy["load_only"], pmeta))
            or (policy["load_forbid"] and matches(entry, policy["load_forbid"], pmeta))
        ]
    if len(entries) > MAX_NEED:
        errors.append(f"@need may list at most {MAX_NEED} paths")
    for entry in entries:
        file, _, anchor = entry.partition("#")
        if file.startswith(("/", "records")) or ".." in Path(file).parts:
            errors.append(f"@need: {entry} is outside the project and Studio files")
            continue
        path, _ = resolve(project, entry)
        if path.is_dir():
            inside = sorted(
                f"{file.rstrip('/')}/{f.name}{'/' if f.is_dir() else ''}"
                for f in path.iterdir()
                if f.name != "__pycache__"
            )
            errors.append(
                f"@need: {entry} is a directory; ask for its files one per line, e.g. "
                + ", ".join(inside[:8])
            )
        elif not path.is_file():
            errors.append(f"@need: {entry} does not exist")
        elif anchor and slug(anchor) not in {
            slug(h) for h in headings(path.read_text(encoding="utf-8"))
        }:
            errors.append(f"@need: no section #{anchor} in {file}")
    return errors


def build_route(project, gdir, records=None, since=None):
    artifacts, gid, seq = goal_artifacts(gdir), gdir.name[:5], next_seq(gdir)
    seen = since if since is not None else seen_through(records, gid)
    fresh = unseen(gdir, seen) or artifacts[-1:]
    rels = [str(p.relative_to(project)) for p, _ in fresh]
    grel = str(gdir.relative_to(project))
    packet = new_packet(
        "Route",
        goal=gid,
        step_artifacts=", ".join(rels),
        next_seq=seq,
        context_request=f"allowed once (@need, up to {MAX_NEED} paths)",
    )
    if current_build(project):
        packet.header["current_build"] = current_build(project)
    packet.add_studio_context(project, ["handoff", "escalation", "goal"])
    packet.add_entry(project, f"{grel}/goal.md")
    add_log(packet, gdir, grel)
    for rel in rels:
        packet.add_entry(project, rel)
    news = [
        f"{grel}/{s:02d}-studio-to-*.md" for s in range(seq, seq + MAX_NEW_HANDOFFS)
    ]
    packet.writes = (
        [f"{grel}/goal.md"]
        + [
            f"{rel} (in place: keep kind, goal, seq, from, to and any Sender assessment)"
            for rel in rels
        ]
        + [
            "project.md: only in the Route that closes the Goal, and only its ## Current state "
            "(at most 1,500 characters)"
        ]
        + [
            f"{grel}/NN-studio-to-<role or owner>.md: up to {MAX_NEW_HANDOFFS} new artifacts, "
            f"consecutive NN starting at {seq:02d}",
            f"@need: instead of all other files, once: a file block `<<<FILE @need` with one path per "
            f"line (up to {MAX_NEED} project or Studio files), then `>>>END`, to add them to this "
            "packet before you route",
        ]
    )
    packet.allow_need = True
    request = owner_request(gdir)
    before = (gdir / "goal.md").read_text(encoding="utf-8")
    used, budget = goal_ops(records, gid), goal_budget(before)
    packet.header["goal_budget"] = budget_line(used, budget)

    def validate(files):
        errors = check_writes(
            files, [f"{grel}/goal.md", "project.md"] + rels + news, project
        )
        new_goal = files.get(f"{grel}/goal.md", "")
        raw = parse(new_goal)[0].get("budget")
        if (raw or parse(before)[0].get("budget")) and goal_budget(new_goal) != budget:
            errors.append(
                "goal.md: keep budget as it was; only the Owner changes it (through Resume)"
            )
        old_rows = {r["n"] for r in route_rows(before)}
        added = [r for r in route_rows(new_goal) if r["n"] not in old_rows]
        if used >= budget and any(
            r["role"] not in ("game-director", "owner") for r in added
        ):
            errors.append(
                f"goal.md: the Goal has used {used} of its {budget} operations, so add no stages "
                "but one: a game-director step to cut the remaining work to what the Owner request "
                "needs (the rest is then skipped), or an owner step to escalate the cost. Planned "
                "steps may still be opened"
            )
        if f"{grel}/goal.md" not in files:
            return errors + ["goal.md must be written"]
        if "project.md" in files:
            closing = parse(files[f"{grel}/goal.md"])[0].get("status") in (
                "done",
                "abandoned",
            )
            errors += check_project_update(
                (project / "project.md").read_text(encoding="utf-8"),
                files["project.md"],
                closing,
            )
        errors += check_goal(files[f"{grel}/goal.md"])
        errors += check_goal_size(files[f"{grel}/goal.md"])
        errors += check_kept(
            before, files[f"{grel}/goal.md"], ["Owner request", "Interpretation"]
        )
        for (path, meta), rel in zip(fresh, rels):
            if rel not in files:
                continue
            nmeta = parse(files[rel])[0]
            if any(
                nmeta.get(k) != meta.get(k)
                for k in ("kind", "goal", "seq", "from", "to")
            ):
                errors.append(
                    f"{rel}: in-place edits must keep kind, goal, seq, from and to"
                )
            kept = section(
                parse(path.read_text(encoding="utf-8"))[1], "Sender assessment"
            )
            if (
                kept.strip()
                and section(parse(files[rel])[1], "Sender assessment").strip()
                != kept.strip()
            ):
                errors.append(
                    f"{rel}: keep ## Sender assessment unchanged; the runtime withholds it where needed"
                )
        created = sorted(
            seq_of(p) for p in files if any(fnmatch.fnmatch(p, n) for n in news)
        )
        if created != list(range(seq, seq + len(created))):
            errors.append(
                f"new artifacts must use consecutive seq numbers starting at {seq:02d}"
            )
        for path in files:
            if any(fnmatch.fnmatch(path, n) for n in news):
                errors += check_artifact(
                    project, path, files[path], request, pending=files
                )
        status = parse(files[f"{grel}/goal.md"])[0].get("status")
        if (
            any(
                m.get("kind") == "escalation" and m.get("status") == "open"
                for _, m in fresh
            )
            and status != "blocked-on-owner"
        ):
            errors.append("an open Escalation must set the Goal to blocked-on-owner")
        written = [
            t for f, t in files.items() if any(fnmatch.fnmatch(f, n) for n in news)
        ]
        open_escalation = any(
            m.get("kind") == "escalation" and m.get("status") == "open"
            for _, m in artifacts
        ) or any(
            parse(t)[0].get("kind") == "escalation"
            and parse(t)[0].get("status") == "open"
            for t in written
        )
        already = [
            p.name
            for p, m in artifacts
            if m.get("kind") == "escalation" and m.get("status") == "open"
        ]
        if already and any(
            parse(t)[0].get("kind") == "escalation"
            and parse(t)[0].get("status") == "open"
            for t in written
        ):
            errors.append(
                f"an Escalation is already open ({', '.join(already)}); do not open another, keep "
                "waiting for the Owner's answer to it"
            )
        if status == "blocked-on-owner" and not open_escalation:
            errors.append(
                "blocked-on-owner needs an open Escalation; while a Role prepares the brief, keep the "
                "Goal active with that Role's step open"
            )
        return errors + check_open_steps(project, grel, files, request)

    return packet, validate


def build_resume(project, gdir, records=None):
    esc = next(
        (
            p
            for p, m in reversed(goal_artifacts(gdir))
            if m.get("kind") == "escalation" and m.get("status") == "open"
        ),
        None,
    )
    if esc is None:
        raise Rejected("no open Escalation to resume")
    erel, grel, gid, seq = (
        str(esc.relative_to(project)),
        str(gdir.relative_to(project)),
        gdir.name[:5],
        next_seq(gdir),
    )
    decision = next_decision(project)
    packet = new_packet(
        "Resume", goal=gid, escalation=erel, next_seq=seq, next_decision=decision
    )
    packet.header["goal_budget"] = (
        budget_line(
            goal_ops(records, gid),
            goal_budget((gdir / "goal.md").read_text(encoding="utf-8")),
        )
        + " (the Owner may change the budget in this decision)"
    )
    if current_build(project):
        packet.header["current_build"] = current_build(project)
    packet.add_studio_context(project, ["decision", "handoff", "goal", "escalation"])
    packet.add_entry(project, f"{grel}/goal.md")
    add_log(packet, gdir, grel)
    packet.add_entry(project, erel)
    new = f"{grel}/{seq:02d}-studio-to-*.md"
    packet.writes = [
        f"decisions/{decision}-<slug>.md",
        erel,
        f"{grel}/goal.md",
        new.replace("*", "<role>"),
        "project.md: only if the Owner's choice ends the Goal (status done or abandoned), and only "
        "its ## Current state (at most 1,500 characters)",
    ]
    request = owner_request(gdir)
    said = re.findall(
        r"^\*\*Owner response \([^)]*\):\*\* (.+)$",
        esc.read_text(encoding="utf-8"),
        re.M,
    )
    before = (gdir / "goal.md").read_text(encoding="utf-8")

    def validate(files):
        errors = check_writes(
            files,
            [f"decisions/{decision}-*.md", erel, f"{grel}/goal.md", new, "project.md"],
            project,
        )
        dec = [p for p in files if p.startswith("decisions/")]
        if len(dec) != 1 or f"{grel}/goal.md" not in files or erel not in files:
            return errors + [
                "write the Owner Decision, the resolved Escalation and goal.md"
            ]
        errors += check_decision(dec[0], files[dec[0]], decided_by="owner")
        if said and not all(said[-1].strip() in files[p] for p in (dec[0], erel)):
            errors.append(
                "the Owner's words must appear verbatim in the Decision and the resolved Escalation"
            )
        emeta = parse(files[erel])[0]
        if emeta.get("status") != "resolved" or emeta.get("decision") != decision:
            errors.append(f"{erel}: status must be resolved with decision: {decision}")
        errors += check_goal(files[f"{grel}/goal.md"])
        errors += check_goal_size(files[f"{grel}/goal.md"])
        errors += check_kept(before, files[f"{grel}/goal.md"], ["Owner request"])
        status = parse(files[f"{grel}/goal.md"])[0].get("status")
        closing = status in ("done", "abandoned")  # the Owner's choice ends the Goal
        if not closing and status != "active":
            errors.append(
                "goal.md: status must return to active, or be done or abandoned when the "
                "Owner's choice ends the Goal (then fill ## Outcome; orchestration.md, Close)"
            )
        if closing and not section(files[f"{grel}/goal.md"], "Outcome").strip(" \n—-"):
            errors.append("goal.md: a closed Goal needs its ## Outcome for the Owner")
        if "project.md" in files:
            errors += check_project_update(
                (project / "project.md").read_text(encoding="utf-8"),
                files["project.md"],
                closing,
            )
        for path in files:
            if fnmatch.fnmatch(path, new):
                errors += check_artifact(
                    project, path, files[path], request, pending=files
                )
        return errors + (
            [] if closing else check_open_steps(project, grel, files, request)
        )

    return packet, validate


def build_simulator(project, gdir, artifact):
    builds = sorted(
        (project / "sim").glob("build-*.md"),
        key=lambda p: [int(x) for x in re.findall(r"\d+", p.stem)],
    )
    major, minor = (int(x) for x in re.findall(r"\d+", builds[-1].stem)[:2])
    target = f"sim/build-{major}.{minor + 1}.md"
    packet = Packet(
        "Simulate",
        operation="Simulate (dry-run harness, not a Studio operation)",
        goal=gdir.name[:5],
    )
    packet.add("simulator-instructions", SIMULATOR)
    packet.add_entry(project, str(artifact.relative_to(project)))
    packet.add_entry(project, str(builds[-1].relative_to(project)))
    packet.add_entry(project, "sim/repo-notes.md")
    packet.add_entry(project, "project.md#constraints")
    packet.writes = [target, "sim/repo-notes.md"]

    def validate(files):
        errors = check_writes(files, [target, "sim/repo-notes.md"], project)
        if target not in files:
            errors.append(f"{target} must be written")
        elif "<!--" in files[target] or "Sender assessment" in files[target]:
            errors.append(
                f"{target}: no comments or sender assessments in a build description"
            )
        return errors

    return packet, validate


# --- Runtimes ----------------------------------------------------------------------------------


def run_claude(packet_text, model=None):
    cwd = tempfile.mkdtemp(prefix="step-")
    cmd = [
        "claude",
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--tools",
        "",
        "--setting-sources",
        "project",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--no-session-persistence",
        "--system-prompt",
        SYSTEM_PROMPT,
    ]
    if model:
        cmd += ["--model", model]
    env = {**os.environ, "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}
    try:
        proc = subprocess.run(
            cmd,
            input=packet_text,
            capture_output=True,
            text=True,
            cwd=cwd,
            env=env,
            timeout=1800,
        )
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    init = result = None
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            init = event
        elif event.get("type") == "result":
            result = event
    if not init or not result or result.get("is_error"):
        raise RuntimeError(
            f"claude run failed: {proc.stderr[-800:] or (result or {}).get('result')}"
        )
    if init.get("tools") or init.get("mcp_servers"):
        raise Rejected(
            f"isolation broken: tools={init.get('tools')} mcp={init.get('mcp_servers')}"
        )
    return {
        "runtime": "claude",
        "text": result.get("result", ""),
        "session_id": result.get("session_id"),
        "model": init.get("model"),
        "tools": init.get("tools"),
        "mcp_servers": init.get("mcp_servers"),
        "tool_uses": [],
        "usage": result.get("usage"),
        "cost_usd": result.get("total_cost_usd"),
    }


CODEX_TOOL_FEATURES = [
    "shell_tool",
    "unified_exec",
    "apps",
    "browser_use",
    "browser_use_external",
    "computer_use",
    "in_app_browser",
    "plugins",
    "skill_search",
    "sleep_tool",
    "tool_suggest",
    "code_mode_host",
    "goals",
    "image_generation",
    "multi_agent",
    "view_image",
    "realtime_conversation",
]


def run_codex(packet_text, model=None):
    cwd = tempfile.mkdtemp(prefix="step-")
    cmd = [
        "codex",
        "exec",
        "--json",
        "--skip-git-repo-check",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "-s",
        "read-only",
        "-C",
        cwd,
        "-c",
        "project_doc_max_bytes=0",
        "-c",
        'web_search="disabled"',
        "-c",
        'model_reasoning_effort="low"',  # --ignore-user-config drops the user's effort setting; keep runs light
    ]
    for feature in CODEX_TOOL_FEATURES:
        cmd += ["--disable", feature]
    if model:
        cmd += ["-m", model]
    try:
        proc = subprocess.run(
            cmd + ["-"], input=packet_text, capture_output=True, text=True, timeout=1800
        )
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    thread, messages, commands, warnings, usage = None, [], [], [], None
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        item = event.get("item") or {}
        if event.get("type") == "thread.started":
            thread = event.get("thread_id")
        elif (
            event.get("type") == "item.completed"
            and item.get("type") == "agent_message"
        ):
            messages.append(item.get("text", ""))
        elif event.get("type") == "item.completed" and item.get("type") == "error":
            warnings.append(item.get("message", "")[:300])
        elif event.get("type") == "item.completed" and item.get("type") not in (
            "agent_message",
            "reasoning",
            "todo_list",
        ):
            commands.append(
                {
                    k: item.get(k)
                    for k in ("type", "command", "path", "query")
                    if item.get(k)
                }
            )
        elif event.get("type") == "turn.completed":
            usage = event.get("usage")
        elif event.get("type") in ("error", "turn.failed"):
            raise RuntimeError(f"codex run failed: {line[:800]}")
    if not messages:
        raise RuntimeError(f"codex run failed: {proc.stderr[-800:]}")
    if commands:
        raise Rejected(f"isolation broken: the executor used tools {commands}")
    return {
        "runtime": "codex",
        "text": messages[-1],
        "session_id": thread,
        "model": model or "default",
        "tools": f"disabled: {','.join(CODEX_TOOL_FEATURES)}; any use rejected",
        "mcp_servers": [],
        "tool_uses": commands,
        "usage": usage,
        "cost_usd": None,
        "warnings": warnings,
        # ponytail: Codex always loads $CODEX_HOME/AGENTS.md; a throwaway CODEX_HOME would need the auth file
        "ambient_instructions": "user-level $CODEX_HOME/AGENTS.md (cannot be disabled by flags)",
    }


RUNTIMES = {"claude": run_claude, "codex": run_codex}


# --- Execution ---------------------------------------------------------------------------------


EDIT_BLOCK = re.compile(  # a block left open ends where the next one starts
    r"^<<<EDIT (\S+)[ \t]*\n(.*?)(?:^>>>END[ \t]*$|(?=^<<<EDIT ))", re.M | re.S
)
EDIT_PAIR = re.compile(
    r"^<<<<<<< SEARCH[ \t]*\n(.*?)^=======[ \t]*\n(.*?)^>>>>>>> REPLACE[ \t]*$",
    re.M | re.S,
)
# Lines of the output format itself that leak into file text: block or edit markers, tool calls.
STRAY_LINE = re.compile(
    r"^[ \t]*(?:(?:<{3,}|>{3,})[ \t]*(?:SEARCH|REPLACE|EDIT|FILE|END).*"
    r"|</?(?:[a-z_]+:)?(?:invoke|parameter|function_calls)\b[^>]*>[ \t]*)$",
    re.M,
)


class Edits(list):
    """SEARCH/REPLACE pairs for one existing file, applied in order (see resolve_edits)."""

    mixed = False  # the same answer also wrote the file whole
    malformed = False  # a pair whose markers are not on lines of their own


def parse_output(text):
    files = {m.group(1): m.group(2).rstrip() + "\n" for m in BLOCK.finditer(text)}
    for path in [p for p, c in files.items() if c.startswith("<<<EDIT ")]:
        del files[
            path
        ]  # an EDIT block wrapped in a FILE block: the EDIT block is what was meant
    for m in EDIT_BLOCK.finditer(text):
        body = m.group(2)
        pairs = EDIT_PAIR.findall(body)
        if (
            body.count("<<<<<<< SEARCH") == len(pairs) + 1
        ):  # a forgotten last REPLACE marker
            pairs = EDIT_PAIR.findall(body.rstrip("\n") + "\n>>>>>>> REPLACE\n")
        earlier = files.get(m.group(1))
        if isinstance(
            earlier, Edits
        ):  # several EDIT blocks for one file: one list, in order
            earlier.extend(pairs)
            earlier.malformed |= body.count("<<<<<<< SEARCH") != len(pairs)
            continue
        edits = Edits(pairs)
        edits.mixed = earlier is not None
        edits.malformed = body.count("<<<<<<< SEARCH") != len(edits)
        files[m.group(1)] = edits
    bare = text.strip().splitlines()
    if (
        not files and bare and bare[0].strip() == "@need"
    ):  # tolerate an unwrapped context request
        files["@need"] = "\n".join(bare[1:]) + "\n"
    return files


def resolve_edits(project, packet, files):
    """Turn every EDIT block into the whole file it produces, in place; return the errors."""
    errors = []
    for path, edits in list(files.items()):
        if not isinstance(edits, Edits):
            continue
        del files[path]
        if edits.mixed:
            errors.append(
                f"{path}: write a file either whole or as EDIT blocks, not both"
            )
            continue
        if path.startswith("/") or ".." in Path(path).parts:
            errors.append(f"{path}: paths must be inside the project")
            continue
        if (
            project / path
        ).is_file():  # never a run-round proposal: every answer is complete
            text = (project / path).read_text(encoding="utf-8")
        else:
            errors.append(
                f"{path}: an EDIT block changes an existing file; write a new file as a whole <<<FILE block"
            )
            continue
        if not edits or edits.malformed:
            errors.append(
                f"{path}: an EDIT block needs <<<<<<< SEARCH / ======= / >>>>>>> REPLACE pairs, each "
                "marker on a line of its own"
            )
            continue
        for number, (search, replace) in enumerate(edits, 1):
            found = text.count(search) if search.strip() else 0
            if found == 0 and search.endswith("\n") and text.count(search[:-1]) == 1:
                # SEARCH holds part of a line: match it without its line break
                search, replace = search[:-1], (
                    replace[:-1] if replace.endswith("\n") else replace
                )
                found = 1
            if found != 1:
                errors.append(
                    f"{path}: EDIT pair {number}: the SEARCH text "
                    + ("is empty" if not search.strip() else f"occurs {found} times")
                    + "; copy it exactly from the project file as written (not from a run-round "
                    "proposal), with enough lines around it to match exactly once"
                )
                break
            text = text.replace(search, replace, 1)
        else:
            files[path] = text if text.endswith("\n") else text + "\n"
    return errors


def stray_lines(project, files):
    """Lines of the output format (markers, tool calls) new to a file: never file content."""
    errors = []
    for path, text in files.items():
        if path.startswith("@") or not isinstance(text, str):
            continue
        old = project / path
        known = (
            set(old.read_text(encoding="utf-8").splitlines())
            if old.is_file()
            else set()
        )
        for line in STRAY_LINE.findall(text):
            if line not in known:
                errors.append(
                    f"{path}: a line looks like a marker or tool-call syntax from the output "
                    f"format, not file content ({line.strip()}); remove it (end each EDIT pair "
                    "with >>>>>>> REPLACE on a line of its own)"
                )
                break
    return errors


CHECK_TAIL = 2_000


def build_check(project, packet, files):
    """After a Step writes build files, run the project's tests on the build exactly as written and
    add the result to the outgoing Handoff (## Build check). A failure is recorded, not rejected.
    """
    build, command = project_meta(project).get("build"), run_commands(project).get(
        "tests"
    )
    written = {p: c for p, c in files.items() if build and p.startswith(f"{build}/")}
    handoff = next(
        (p for p in files if fnmatch.fnmatch(p, getattr(packet, "out", "") or "-")),
        None,
    )
    if packet.op != "Step" or not command or not written or not handoff:
        return None
    if parse(files[handoff])[0].get("kind") != "handoff":
        return None
    with tempfile.TemporaryDirectory(prefix="check-") as tmp:
        work = Path(tmp) / "build"
        shutil.copytree(project / build, work)
        for path, content in written.items():
            target = work / Path(path).relative_to(build)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        (work / SCRIPT_NAME).write_text("", encoding="utf-8")
        code, output, seconds = sandboxed(
            work, shlex.split(command.replace("{script}", SCRIPT_NAME))
        )
    note = (
        f"## Build check\n\nThe runtime ran `run_tests` (`{command}`) on the build exactly as this "
        f"step wrote it: exit {code} ({seconds} s).\n\n```text\n{output.rstrip()[-CHECK_TAIL:]}\n```\n\n"
    )
    text = files[handoff]
    load = re.search(r"^## Load[ \t]*$", text, re.M)
    files[handoff] = (
        text[: load.start()] + note + text[load.start() :]
        if load
        else text.rstrip() + "\n\n" + note
    )
    return {"command": command, "exit": code, "seconds": seconds, "output": output}


# --- Build runs (sandboxed) -------------------------------------------------------------------

MAX_RUNS, RUN_TIMEOUT, RUN_OUTPUT_MAX = 3, 30, 20_000
SCRIPT_NAME = "input.script"
SANDBOX = [
    "bwrap",
    "--ro-bind", "/usr", "/usr",
    "--symlink", "usr/bin", "/bin",
    "--symlink", "usr/lib", "/lib",
    "--symlink", "usr/lib64", "/lib64",
    "--symlink", "usr/sbin", "/sbin",
    "--dev", "/dev",
    "--proc", "/proc",
    "--tmpfs", "/tmp",
    "--unshare-all",
    "--die-with-parent",
    "--new-session",
    "--clearenv",
    "--setenv", "PATH", "/usr/bin",
    "--setenv", "HOME", "/work",
    "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
]  # fmt: skip


def sandboxed(work, argv):
    """Run one build command where only /usr (read-only) and the build copy (/work) exist, offline."""
    if not shutil.which("bwrap"):
        raise RuntimeError(
            "sandbox unavailable: bubblewrap (bwrap) not found; build commands never run unsandboxed"
        )
    started = time.time()
    try:
        proc = subprocess.run(
            SANDBOX + ["--bind", str(work), "/work", "--chdir", "/work"] + argv,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT,
        )
        code, output = proc.returncode, proc.stdout + proc.stderr
    except subprocess.TimeoutExpired as error:
        parts = [error.stdout, error.stderr]
        code = "timeout"
        output = (
            "".join(
                p.decode(errors="replace") if isinstance(p, bytes) else (p or "")
                for p in parts
            )
            + f"\n[stopped after {RUN_TIMEOUT} s]"
        )
    if (
        len(output) > RUN_OUTPUT_MAX
    ):  # keep the start and the end, where results usually are
        head, tail = RUN_OUTPUT_MAX * 7 // 10, RUN_OUTPUT_MAX * 3 // 10
        cut = len(output) - head - tail
        output = output[:head] + f"\n[... {cut} characters cut ...]\n" + output[-tail:]
    return code, output, round(time.time() - started, 1)


def check_runs(packet, files):
    if not packet.runs:
        return [
            "@run is not available here (only in a Step whose Role may run the project's build)"
        ]
    if packet.rounds >= MAX_RUNS:
        return [f"all {MAX_RUNS} run rounds are used; write your final files now"]
    errors = []
    for path in files:
        if path.startswith("@run/"):
            if path.split("/")[1] not in packet.runs:
                errors.append(f"{path}: you may run only {', '.join(packet.runs)}")
        elif (
            path.startswith("/")
            or ".." in Path(path).parts
            or not any(fnmatch.fnmatch(path, p) for p in packet.write_patterns)
        ):
            errors.append(
                f"{path}: not a file your Role may write; leave it out (if it needs changing, say so "
                "in your Handoff for the Role that owns it)"
            )
        elif not path.startswith(packet.build + "/"):
            errors.append(
                f"{path}: a run round carries only {packet.build}/ files; write it in your final answer"
            )
    return errors


def run_round(project, packet, files, rec):
    """Run the requested commands on a copy of the build with every proposed file applied, and put
    the results (and the proposals, which are not written) into the packet for a new executor.
    """
    commands = run_commands(project)
    packet.proposed.update(
        {p: c for p, c in files.items() if not p.startswith("@run/")}
    )
    packet.rounds += 1
    results = []
    labels = [label for label in files if label.startswith("@run/")]
    with tempfile.TemporaryDirectory(prefix="build-") as tmp:
        for number, label in enumerate(labels):
            # A fresh copy per run, prepared before any sandboxed code touches it: the host never
            # writes into a directory a command could have filled with links.
            work = Path(tmp) / f"run{number}"
            shutil.copytree(project / packet.build, work)
            for path, content in packet.proposed.items():
                target = work / Path(path).relative_to(packet.build)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            script, command = files[label], commands[label.split("/")[1]]
            (work / SCRIPT_NAME).write_text(script, encoding="utf-8")
            code, output, seconds = sandboxed(
                work, shlex.split(command.replace("{script}", SCRIPT_NAME))
            )
            results.append(
                {
                    "run": label,
                    "command": command,
                    "script": script,
                    "exit": code,
                    "seconds": seconds,
                    "output": output,
                }
            )
    (rec / f"runs-round{packet.rounds}.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    for r in results:
        script = (
            f"Script:\n\n```text\n{r['script'].rstrip()}\n```\n\n"
            if r["script"].strip()
            else ""
        )
        packet.run_log.append(
            f"### Round {packet.rounds}: {r['run']} — `{r['command']}`\n\n{script}"
            f"Exit: {r['exit']} ({r['seconds']} s). Output:\n\n```text\n{r['output'].rstrip()}\n```\n"
        )
    if packet.base_inputs is None:
        packet.base_inputs = list(packet.inputs)
    packet.inputs = list(packet.base_inputs)
    for path, content in packet.proposed.items():
        packet.add(f"{path} (proposed in a run round; not written)", content)
    packet.add("@run-results", "\n".join(packet.run_log))
    left = MAX_RUNS - packet.rounds
    packet.header["runs"] = (
        f"{', '.join(packet.runs)} ({left} rounds left; results in @run-results)"
    )
    if not left:
        packet.writes = [w for w in packet.writes if not w.startswith("@run/")]
    return results


def record_dir(ws, op, role=None):
    records = ws / "records"
    records.mkdir(parents=True, exist_ok=True)
    number = len([d for d in records.iterdir() if d.is_dir()]) + 1
    path = records / f"{number:03d}-{op.lower().split()[0]}{'-' + role if role else ''}"
    path.mkdir()
    return path


def save_record(rec, record):
    (rec / "record.json").write_text(
        json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8"
    )


def execute(ws, packet, validate, args, role=None):
    """Run one operation in fresh executors (one per attempt); write only validated files.

    A Route may first answer with an @need block: its listed files are added to the packet and a
    new executor runs once more. That round does not count as a retry."""
    rec = record_dir(ws, packet.op, role)
    base = packet.render()
    (rec / "packet.md").write_text(base, encoding="utf-8")
    (rec / "manifest.json").write_text(
        json.dumps(packet.manifest(), indent=1), encoding="utf-8"
    )
    record = {
        "op": packet.op,
        "role": role,
        "goal": packet.header.get("goal"),
        "attempts": [],
    }
    feedback, retries_left, attempt = "", args.retries, 0
    while True:
        attempt += 1
        started = time.time()
        if attempt > 1:
            (rec / f"packet-attempt{attempt}.md").write_text(
                base + feedback, encoding="utf-8"
            )
        try:
            result = RUNTIMES[args.runtime](base + feedback, args.model)
        except (RuntimeError, Rejected, OSError) as error:
            record.update(status="error", errors=[str(error)])
            save_record(rec, record)
            # An OSError means the runtime could not start (e.g., its CLI is missing or mid-update).
            if isinstance(error, OSError):
                raise RuntimeError(f"runtime could not start: {error}") from error
            raise
        text = result.pop("text")
        (rec / f"output-attempt{attempt}.txt").write_text(text, encoding="utf-8")
        files = parse_output(text)
        edit_errors = resolve_edits(ws / "project", packet, files)
        edit_errors += stray_lines(ws / "project", files)
        need = None
        runs = [p for p in files if p.startswith("@run/")]
        if edit_errors:
            errors = edit_errors
        elif runs and "@need" not in files:
            errors = check_runs(packet, files)
        elif "@need" in files:
            if packet.allow_need:
                need = [
                    l.strip().lstrip("-* ").strip()
                    for l in files["@need"].splitlines()
                    if l.strip()
                ]
                errors = check_need(
                    ws / "project",
                    need,
                    packet.header.get("role") if packet.op == "Step" else None,
                )
            else:
                errors = ["@need is not available here (only once per operation)"]
        else:
            errors = list(dict.fromkeys(validate(files)))
        record["attempts"].append(
            {
                **result,
                "attempt": attempt,
                "started": datetime.datetime.fromtimestamp(started).isoformat(
                    timespec="seconds"
                ),
                "seconds": round(time.time() - started, 1),
                "errors": errors,
                **({"need": need} if need is not None else {}),
                **({"runs": runs} if runs else {}),
            }
        )
        if need is not None and not errors:
            for entry in need:
                packet.add_entry(ws / "project", entry, packet.strip_names)
                if packet.base_inputs is not None:  # keep it through later run rounds
                    packet.base_inputs.append(packet.inputs[-1])
            packet.allow_need = False
            packet.writes = [w for w in packet.writes if not w.startswith("@need")]
            packet.header["context_request"] = (
                "used (the requested files are in Inputs)"
            )
            base, feedback = packet.render(), ""
            (rec / f"manifest-attempt{attempt + 1}.json").write_text(
                json.dumps(packet.manifest(), indent=1), encoding="utf-8"
            )
            print(f"[{rec.name}] context requested: {', '.join(need)}")
            continue
        if runs and not errors:
            try:
                results = run_round(ws / "project", packet, files, rec)
            except RuntimeError as error:
                record.update(status="error", errors=[str(error)])
                save_record(rec, record)
                raise
            base, feedback = packet.render(), ""
            (rec / f"manifest-attempt{attempt + 1}.json").write_text(
                json.dumps(packet.manifest(), indent=1), encoding="utf-8"
            )
            print(
                f"[{rec.name}] run round {packet.rounds}: "
                + ", ".join(f"{r['run']} exit {r['exit']}" for r in results)
            )
            continue
        if not errors:
            try:
                check = build_check(ws / "project", packet, files)
            except RuntimeError as error:
                record.update(status="error", errors=[str(error)])
                save_record(rec, record)
                raise
            if check:
                (rec / "build-check.json").write_text(
                    json.dumps(check, indent=1, ensure_ascii=False), encoding="utf-8"
                )
                print(f"[{rec.name}] build check: run_tests exit {check['exit']}")
            goal_file = next((p for p in files if p.endswith("/goal.md")), None)
            goal_path = ws / "project" / goal_file if goal_file else None
            before = (
                goal_path.read_text(encoding="utf-8")
                if goal_path and goal_path.is_file()
                else None
            )
            for path, content in files.items():
                (ws / "project" / path).parent.mkdir(parents=True, exist_ok=True)
                (ws / "project" / path).write_text(content, encoding="utf-8")
            record.update(
                status="ok",
                written={p: sha(c) for p, c in files.items()},
                decision=decision_summary(files),
            )
            if packet.op in STUDIO_OPS and goal_file:
                gdir = goal_path.parent
                record["seen_through_seq"] = max(
                    [seq_of(a) for a, _ in goal_artifacts(gdir)] + [0]
                )
                append_log(gdir, rec.name, before)
            save_record(rec, record)
            print(
                f"[{rec.name}] ok ({result['runtime']}, session {result['session_id']}): {', '.join(files)}"
            )
            return files
        print(f"[{rec.name}] attempt {attempt} rejected:\n  " + "\n  ".join(errors))
        if retries_left == 0:
            break
        retries_left -= 1
        feedback = (
            "\n## Validation feedback\n\nA previous executor's output was rejected for these reasons. "
            "Produce the operation's files again, fixing them:\n\n"
            + "".join(f"- {e}\n" for e in errors)
        )
    record["status"] = "rejected"
    save_record(rec, record)
    raise Rejected(f"{rec.name}: output rejected after {attempt} attempts")


def do_step(ws, args, handoff=None):
    """One Step (and the dry-run simulator after a finished Build). Returns (role, outcome)."""
    project = ws / "project"
    gdir = goal_dir(project, args.goal)
    status = parse((gdir / "goal.md").read_text(encoding="utf-8"))[0].get("status")
    if status != "active":
        raise Rejected(
            f"goal is {status}; "
            + ("run decide" if status == "blocked-on-owner" else "nothing to run")
        )
    if handoff is None:
        handoffs = [project / args.handoff] if args.handoff else open_handoffs(gdir)
        if len(handoffs) != 1:
            raise Rejected(
                f"expected one open step, found {[h.name for h in handoffs]} (use --handoff or run)"
            )
        handoff = handoffs[0]
    packet, validate = build_step(project, gdir, handoff)
    files = execute(ws, packet, validate, args, role=packet.header["role"])
    artifact = next(project / p for p in files if p.startswith("goals/"))
    meta = parse(artifact.read_text(encoding="utf-8"))[0]
    if (
        packet.header["role"] == "gameplay-engineer"
        and meta.get("outcome") == "done"
        and (project / "sim").is_dir()
    ):
        sim_packet, sim_validate = build_simulator(project, gdir, artifact)
        execute(ws, sim_packet, sim_validate, args, role="simulator")
    return packet.header["role"], meta.get("outcome")


def do_simulate(ws, args):
    """Re-run the dry-run simulator for the latest finished Build (e.g., after a runtime failure)."""
    project = ws / "project"
    gdir = goal_dir(project, args.goal)
    artifact = next(
        (
            p
            for p, m in reversed(goal_artifacts(gdir))
            if m.get("from") == "gameplay-engineer" and m.get("outcome") == "done"
        ),
        None,
    )
    if artifact is None:
        raise Rejected("no finished Build to simulate")
    packet, validate = build_simulator(project, gdir, artifact)
    execute(ws, packet, validate, args, role="simulator")


def do_route(ws, args):
    project = ws / "project"
    packet, validate = build_route(
        project,
        goal_dir(project, args.goal),
        ws / "records",
        getattr(args, "since", None),
    )
    execute(ws, packet, validate, args)
    do_status(ws, args)


def no_progress(role, history, opened):
    """Mechanical backstop for the orchestration loop limits within one `run`."""
    if history.get(role, [])[-2:] == ["question", "question"]:
        return f"no progress: {role} handed back `question` twice and was opened again"
    if opened[role] >= 3:
        return f"no progress: {role} would be opened a 4th time in this run"
    return None


def open_escalations(gdir):
    return [
        p
        for p, m in goal_artifacts(gdir)
        if m.get("kind") == "escalation" and m.get("status") == "open"
    ]


def unrouted(records, gdir):
    """Artifacts newer than the last Studio operation's view (e.g., a Route failed after a Step)."""
    return bool(unseen(gdir, seen_through(records, gdir.name[:5])))


def do_run(ws, args):
    """Run Steps and Routes until the Goal closes, needs the Owner, or a stop condition fires."""
    project, records = ws / "project", ws / "records"
    gdir = goal_dir(project, args.goal)
    before = {d.name for d in records.iterdir()}
    used = lambda: len(
        {d.name for d in records.iterdir() if d.is_dir()} - before
    )  # noqa: E731
    history, opened, reason, code, announced = {}, Counter(), None, 0, set()
    try:
        while reason is None:
            for esc in open_escalations(
                gdir
            ):  # an Owner question the Studio works around
                if esc.name not in announced:
                    announced.add(esc.name)
                    print(
                        f"[run] Owner question open: {esc.relative_to(project)} "
                        "(the Studio continues with other steps meanwhile)"
                    )
            status = parse((gdir / "goal.md").read_text(encoding="utf-8"))[0].get(
                "status"
            )
            handoffs = open_handoffs(gdir) if status == "active" else []
            roles = [
                parse(h.read_text(encoding="utf-8"))[0].get("to") for h in handoffs
            ]
            if status != "active":
                reason = status
            elif used() >= args.max_ops:
                reason = f"operation budget reached ({args.max_ops})"
            elif not handoffs:
                reason = "no open step"
            else:
                reason = next(
                    (r for r in (no_progress(x, history, opened) for x in roles) if r),
                    None,
                )
            if reason:
                break
            if unrouted(
                records, gdir
            ):  # route what earlier Steps produced before stepping again
                do_route(ws, args)
                continue
            for handoff in handoffs:
                role, outcome = do_step(ws, args, handoff=handoff)
                opened[role] += 1
                history.setdefault(role, []).append(outcome)
            do_route(ws, args)
    except Rejected as error:
        reason, code = f"rejected: {error}", 2
    except RuntimeError as error:
        reason, code = f"runtime error: {error}", 3
    text = (gdir / "goal.md").read_text(encoding="utf-8")
    status = parse(text)[0].get("status")
    escalation = next(
        (str(p.relative_to(project)) for p in reversed(open_escalations(gdir))), None
    )
    wsr = os.path.relpath(ws, ROOT) if ws.is_relative_to(ROOT) else str(ws)
    summary = {
        "op": "Run",
        "goal": gdir.name[:5],
        "operations": sorted(
            {d.name for d in records.iterdir() if d.is_dir()} - before
        ),
        "stop_reason": reason,
        "status": status,
        "owner_reads": (
            escalation
            if escalation and status in ("blocked-on-owner", "active")
            else (
                str((gdir / "goal.md").relative_to(project)) + "#outcome"
                if status == "done"
                else None
            )
        ),
        "next": (
            f'decide {wsr} "<answer>"'
            if escalation and status in ("blocked-on-owner", "active")
            else {"done": None, "abandoned": None}.get(status, f"run {wsr}")
        ),
    }
    save_record(record_dir(ws, "run"), summary)
    print(f"\n[run] {len(summary['operations'])} operations; stopped: {reason}")
    if summary["owner_reads"]:
        print(f"[run] Owner: read {summary['owner_reads']}")
    if summary["next"]:
        print(f"[run] next: python3 scripts/studio_run.py {summary['next']}")
    return code


def do_decide(ws, args):
    """Record the Owner's words on the open Escalation verbatim, then Resume in a fresh executor."""
    project = ws / "project"
    gdir = goal_dir(project, args.goal)
    esc = next(
        (
            p
            for p, m in reversed(goal_artifacts(gdir))
            if m.get("kind") == "escalation" and m.get("status") == "open"
        ),
        None,
    )
    if esc is None:
        raise Rejected("no open Escalation")
    if args.text:
        with esc.open("a", encoding="utf-8") as f:
            f.write(
                f"\n---\n\n**Owner response ({datetime.date.today()}):** {args.text}\n"
            )
    packet, validate = build_resume(project, gdir, ws / "records")
    execute(ws, packet, validate, args)
    do_status(ws, args)


def do_status(ws, args):
    gdir = goal_dir(ws / "project", args.goal)
    text = (gdir / "goal.md").read_text(encoding="utf-8")
    print(
        f"{gdir.name}: {parse(text)[0].get('status')}\n{section(text, 'Next action').strip()}"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "command",
        choices=[
            "init",
            "intake",
            "next",
            "step",
            "simulate",
            "route",
            "decide",
            "replay",
            "packet",
            "status",
            "run",
        ],
    )
    parser.add_argument("workspace", type=Path)
    parser.add_argument("text", nargs="?")
    parser.add_argument("--from", dest="source", type=Path)
    parser.add_argument("--runtime", choices=sorted(RUNTIMES), default="claude")
    parser.add_argument("--model")
    parser.add_argument("--goal")
    parser.add_argument("--handoff")
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument(
        "--max-ops", type=int, default=25, help="run: operation budget per invocation"
    )
    parser.add_argument(
        "--since",
        type=int,
        help="route: re-route the artifacts after this seq (recovery)",
    )
    args = parser.parse_args(argv)
    ws, project = args.workspace.resolve(), args.workspace.resolve() / "project"
    try:
        if args.command == "init":
            shutil.copytree(args.source, project)
            (project / "goals").mkdir(exist_ok=True)
            (ws / "records").mkdir()
        elif args.command == "run":
            return do_run(ws, args)
        elif args.command == "intake":
            packet, validate = build_intake(project, args.text)
            execute(ws, packet, validate, args)
            do_status(ws, args)
        elif args.command == "next":
            do_step(ws, args)
            do_route(ws, args)
        elif args.command == "step":
            do_step(ws, args)
        elif args.command == "route":
            do_route(ws, args)
        elif args.command == "simulate":
            do_simulate(ws, args)
        elif args.command == "decide":
            do_decide(ws, args)
        elif args.command == "replay":
            rec = Path(args.text).resolve()
            original = json.loads((rec / "record.json").read_text(encoding="utf-8"))
            result = RUNTIMES[args.runtime](
                (rec / "packet.md").read_text(encoding="utf-8"), args.model
            )
            replay = {
                "of": rec.name,
                "runtime": result["runtime"],
                "session_id": result["session_id"],
                "decision": decision_summary(parse_output(result["text"])),
                "original": original.get("decision"),
            }

            def core(d):  # the routing decision itself; stage labels are free text
                d = d or {}
                return (
                    d.get("status"),
                    sorted(r for r, _ in d.get("open", [])),
                    (d.get("new") or [None])[0],
                )

            replay["same_decision"] = core(replay["decision"]) == core(
                replay["original"]
            )
            out = record_dir(ws, "replay")
            (out / "output-attempt1.txt").write_text(result["text"], encoding="utf-8")
            (out / "record.json").write_text(
                json.dumps(replay, indent=1, ensure_ascii=False), encoding="utf-8"
            )
            print(json.dumps(replay, ensure_ascii=False))
        elif args.command == "packet":
            gdir = goal_dir(project, args.goal)
            if args.text == "step":
                handoffs = (
                    [project / args.handoff] if args.handoff else open_handoffs(gdir)
                )
                print(build_step(project, gdir, handoffs[0])[0].render())
            else:
                print(build_route(project, gdir)[0].render())
        elif args.command == "status":
            do_status(ws, args)
    except Rejected as error:
        print(f"rejected: {error}", file=sys.stderr)
        return 2
    except RuntimeError as error:
        print(f"runtime error: {error}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
