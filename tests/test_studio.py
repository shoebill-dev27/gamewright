"""Structural checks for the Studio definition and dry-run assertions for the sample projects.

Run with `python3 -m pytest tests/` or, without pytest, `python3 tests/test_studio.py`.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDIO = ROOT / "studio"
PROJECTS = ROOT / "examples" / "projects"

ROLE_IDS = {p.stem for p in (STUDIO / "roles").glob("*.md")}
SKILL_IDS = {p.stem for p in (STUDIO / "skills").glob("*.md")}
PARTICIPANTS = ROLE_IDS | {"studio", "owner"}
STAGES = {
    "Observe",
    "Diagnose",
    "Decide",
    "Design",
    "Plan",
    "Build",
    "Verify",
    "Play",
    "Review",
    "Next",
}
OUTCOMES = {"routed", "done", "partial", "pass", "fail", "question", "goal-met", "goal-not-met"}

REQUIRED_SECTIONS = {
    "role": [
        "Responsibility",
        "Decides",
        "Must not",
        "Works from",
        "Produces",
        "Hands back / escalates when",
        "Typical skills",
    ],
    "skill": ["When to use", "Inputs", "Method", "Output", "Do not"],
    # spec §10
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
    # spec §11
    "decision": ["Decision", "Rationale", "Alternatives considered", "Revisit when"],
    # spec §5
    "escalation": [
        "Question",
        "Why this needs the Owner",
        "Options",
        "Studio recommendation",
        "Reasoning",
        "Owner decision required",
    ],
    "goal": [
        "Owner request",
        "Interpretation",
        "Unknowns",
        "Route",
        "Route changes",
        "Next action",
        "Outcome",
    ],
    # spec §6
    "project": ["Vision", "Current state", "Constraints", "Design index"],
}

TOOL_TERMS = re.compile(
    r"\b(claude|codex|anthropic|openai|chatgpt|gemini|gpt|opus|sonnet|haiku|mcp|agents\.md)\b",
    re.I,
)


def parse(path):
    """Return (frontmatter dict, body). Frontmatter is flat `key: value`; ` #` starts a comment."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.split(" #")[0].strip()
    return meta, body


def headings(body):
    return {m.group(1).strip() for m in re.finditer(r"^## (.+)$", body, re.M)}


def section(body, name):
    m = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


def slug(heading):
    return re.sub(r"[^a-z0-9-]", "", heading.lower().replace(" ", "-"))


def artifacts(kind, project=None):
    for p in sorted(PROJECTS.glob(f"{project or '*'}/**/*.md")):
        meta, body = parse(p)
        if meta.get("kind") == kind:
            yield p, meta, body


def project_dir(path):
    return PROJECTS / path.relative_to(PROJECTS).parts[0]


def goal_artifacts(project, goal_id):
    """Handoffs and escalations of one goal, in seq order."""
    items = [
        (p, m, b)
        for kind in ("handoff", "escalation")
        for p, m, b in artifacts(kind, project)
        if m["goal"] == goal_id
    ]
    return sorted(items, key=lambda item: int(item[1]["seq"]))


def goal_record(project, goal_id):
    return next(
        (p, m, b) for p, m, b in artifacts("goal", project) if m["id"] == goal_id
    )


def route_rows(body):
    rows = []
    for line in section(body, "Route").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and re.fullmatch(r"\d+[a-z]?", cells[0]):
            rows.append(
                dict(zip(["n", "stage", "role", "skills", "status", "handoff"], cells))
            )
    return rows


def load_paths(body):
    return re.findall(r"[\w./-]+\.md(?:#[\w-]+)?", section(body, "Load"))


def resolve(path, project):
    file, _, anchor = path.partition("#")
    return (ROOT / file if file.startswith("studio/") else project / file), anchor


def participants(items):
    return {m["from"] for _, m, _ in items} | {m["to"] for _, m, _ in items}


# --- Studio definition -------------------------------------------------------------------------


def test_role_contracts_are_complete():
    assert ROLE_IDS == {
        "game-director",
        "game-designer",
        "technical-director",
        "gameplay-engineer",
        "art-director",
        "qa",
        "playtester",
    }
    for role in ROLE_IDS:
        meta, body = parse(STUDIO / "roles" / f"{role}.md")
        assert meta.get("id") == role
        missing = set(REQUIRED_SECTIONS["role"]) - headings(body)
        assert not missing, f"{role}: missing {missing}"
        typical = {
            s.strip() for s in section(body, "Typical skills").split(",") if s.strip()
        }
        assert typical <= SKILL_IDS, f"{role}: unknown skills {typical - SKILL_IDS}"


def test_independent_roles_declare_independence():
    for role in ("qa", "playtester"):
        _, body = parse(STUDIO / "roles" / f"{role}.md")
        assert "Independence" in headings(body)


def test_skills_are_complete_and_not_owned_by_a_role():
    for skill in SKILL_IDS:
        meta, body = parse(STUDIO / "skills" / f"{skill}.md")
        assert meta.get("name") == skill and meta.get("description")
        missing = set(REQUIRED_SECTIONS["skill"]) - headings(body)
        assert not missing, f"{skill}: missing {missing}"
        assert "Typical roles:" in body


def test_catalogue_matches_files():
    _, body = parse(STUDIO / "README.md")
    for name, ids in (("Roles", ROLE_IDS), ("Skills", SKILL_IDS)):
        listed = set(re.findall(r"^\| `([a-z-]+)` \|", section(body, name), re.M))
        assert listed == ids, f"{name} catalogue differs: {listed ^ ids}"


def test_studio_and_project_artifacts_are_tool_neutral():
    for path in [*STUDIO.rglob("*.md"), *PROJECTS.rglob("*.md")]:
        hits = TOOL_TERMS.findall(path.read_text(encoding="utf-8"))
        assert not hits, f"{path.relative_to(ROOT)} names tools: {set(hits)}"


def test_studio_is_project_neutral():
    terms = set()
    for p, meta, _ in artifacts("project"):
        terms |= {meta["id"], meta["name"].replace("(sample)", "").strip()}
    for path in STUDIO.rglob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        found = {t for t in terms if t.lower() in text}
        assert not found, f"{path.relative_to(ROOT)} mentions project {found}"


# --- Project artifacts -------------------------------------------------------------------------


def test_artifacts_have_required_sections():
    for kind in ("handoff", "decision", "escalation", "goal", "project"):
        found = list(artifacts(kind))
        assert found, f"no {kind} artifacts"
        for path, _, body in found:
            missing = set(REQUIRED_SECTIONS[kind]) - headings(body)
            assert not missing, f"{path.relative_to(ROOT)}: missing {missing}"


def test_projects_declare_repository_and_owner_language():
    for path, meta, _ in artifacts("project"):
        assert meta.get("repository") and meta.get("owner_language"), path


def test_handoff_fields_and_filenames():
    for kind in ("handoff", "escalation"):
        for path, meta, _ in artifacts(kind):
            assert meta["from"] in PARTICIPANTS and meta["to"] in PARTICIPANTS, path
            assert (
                path.name == f"{int(meta['seq']):02d}-{meta['from']}-to-{meta['to']}.md"
            ), path
            if kind == "handoff":
                assert meta["stage"] in STAGES | {"Route"}, path
                assert meta["outcome"] in OUTCOMES, path
            else:
                assert meta["to"] == "owner" and meta["status"] in {
                    "open",
                    "resolved",
                }, path


def test_load_lists_resolve_and_include_the_recipient_role():
    for path, meta, body in artifacts("handoff"):
        project = project_dir(path)
        for ref in load_paths(body):
            target, anchor = resolve(ref, project)
            assert target.is_file(), f"{path.relative_to(ROOT)}: missing {ref}"
            if anchor:
                assert anchor in {
                    slug(h) for h in headings(parse(target)[1])
                }, f"{path}: {ref}"
        if meta["to"] in ROLE_IDS:
            assert f"studio/roles/{meta['to']}.md" in load_paths(body), path


def test_referenced_decisions_exist():
    for project in PROJECTS.iterdir():
        ids = {m["id"] for _, m, _ in artifacts("decision", project.name)}
        for path in (project / "goals").rglob("*.md"):
            refs = set(re.findall(r"\bD-\d{3}\b", path.read_text(encoding="utf-8")))
            assert refs <= ids, f"{path.relative_to(ROOT)}: unknown {refs - ids}"


def test_route_tables_are_valid():
    for path, _, body in artifacts("goal"):
        rows = route_rows(body)
        assert rows, path
        for row in rows:
            assert row["role"] in PARTICIPANTS, (path, row)
            skills = {s.strip() for s in row["skills"].split(",")} - {"—"}
            assert skills <= SKILL_IDS, (path, row)
            if row["handoff"] != "—":
                assert (path.parent / row["handoff"]).is_file(), (path, row)


def test_every_role_starts_from_a_previous_handoff():
    for path, meta, _ in artifacts("goal"):
        items = goal_artifacts(project_dir(path).name, meta["id"])
        received = set()
        for p, m, _ in items:
            if m["from"] in ROLE_IDS:
                assert (
                    m["from"] in received
                ), f"{p.relative_to(ROOT)}: sender never received work"
            received.add(m["to"])


# --- Dry-run assertions (test requirements) ----------------------------------------------------


def test_bug_goal_takes_the_short_route_and_qa_failure_returns_to_build():
    _, goal, body = goal_record("lantern-depths", "G-001")
    items = goal_artifacts("lantern-depths", "G-001")
    assert participants(items) == {"studio", "qa", "gameplay-engineer"}
    assert {r["role"] for r in route_rows(body)} == {
        "studio",
        "qa",
        "gameplay-engineer",
    }
    flow = [(m["from"], m["to"], m.get("outcome")) for _, m, _ in items]
    fail = flow.index(("qa", "gameplay-engineer", "fail"))
    assert flow[fail + 1][:2] == ("gameplay-engineer", "qa")
    assert flow[-1] == ("qa", "studio", "pass") and goal["status"] == "done"


def test_experience_goal_expands_only_to_needed_roles():
    used = participants(goal_artifacts("lantern-depths", "G-002"))
    assert {
        "playtester",
        "game-designer",
        "game-director",
        "technical-director",
        "gameplay-engineer",
        "qa",
    } <= used
    assert "art-director" not in used  # no visual cause was diagnosed
    assert "art-director" in participants(goal_artifacts("tidepool-garden", "G-001"))


def test_engineer_hands_spec_gaps_back_to_the_designer():
    items = goal_artifacts("lantern-depths", "G-002")
    flow = [(m["from"], m["to"], m.get("outcome")) for _, m, _ in items]
    gap = flow.index(("gameplay-engineer", "game-designer", "question"))
    _, answer, body = items[gap + 1]
    assert (answer["from"], answer["to"]) == ("game-designer", "gameplay-engineer")
    cited = re.findall(r"D-\d{3}", section(body, "Decisions already made"))
    deciders = {
        m["id"]: m["decided_by"] for _, m, _ in artifacts("decision", "lantern-depths")
    }
    assert "game-designer" in {deciders[d] for d in cited}


def test_playtest_findings_return_to_design_roles():
    for project in ("lantern-depths", "tidepool-garden"):
        for path, meta, _ in artifacts("handoff", project):
            if meta["from"] == "playtester":
                assert meta["to"] in {"game-designer", "game-director", "studio"}, path
    senders = {
        m["to"]
        for _, m, _ in goal_artifacts("lantern-depths", "G-002")
        if m["from"] == "playtester"
    }
    assert senders == {"game-designer", "game-director"}


def test_owner_escalation_stops_with_options_and_resumes():
    items = goal_artifacts("lantern-depths", "G-002")
    index = next(i for i, (_, m, _) in enumerate(items) if m["kind"] == "escalation")
    _, esc, body = items[index]
    assert len(re.findall(r"^### Option", section(body, "Options"), re.M)) >= 2
    assert section(body, "Studio recommendation").strip()
    decision = next(
        m
        for _, m, _ in artifacts("decision", "lantern-depths")
        if m["id"] == esc["decision"]
    )
    assert esc["status"] == "resolved" and decision["decided_by"] == "owner"
    _, after, after_body = items[index + 1]
    assert after["from"] == "studio" and esc["decision"] in section(
        after_body, "Decisions already made"
    )


def test_playtester_handoffs_are_blind():
    for path, meta, body in artifacts("handoff"):
        if meta["to"] != "playtester":
            continue
        _, _, goal_body = goal_record(project_dir(path).name, meta["goal"])
        request = section(goal_body, "Owner request").strip().lstrip("> ").strip()
        assert request not in body, f"{path.relative_to(ROOT)} leaks the Owner request"
        for ref in load_paths(body):
            assert not ref.startswith(
                ("design/", "goals/", "decisions/", "sim/repo")
            ), (path, ref)


def test_same_role_contracts_serve_multiple_projects():
    loaded = {}
    for path, _, body in artifacts("handoff"):
        for ref in load_paths(body):
            if ref.startswith("studio/roles/"):
                loaded.setdefault(ref, set()).add(project_dir(path).name)
    for role in ("playtester", "game-designer"):
        assert loaded[f"studio/roles/{role}.md"] == {
            "lantern-depths",
            "tidepool-garden",
        }


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} checks passed")
