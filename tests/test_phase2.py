"""Phase 2: execution-level isolation. Deterministic — a fake runtime stands in for executors.

Recorded live runs under examples/runs/ are checked too, when present.
Run with `python3 -m pytest tests/`.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import studio_run as sr  # noqa: E402

FIXTURE = ROOT / "examples" / "fixtures" / "lantern-depths"
RUNS = ROOT / "examples" / "runs"
REQUEST = "ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。"
G = "goals/G-001-test"


def goal(rows, status="active"):
    table = "".join(
        f"| {n} | {stage} | {role} | {skills} | {st} | {h} |\n"
        for n, stage, role, skills, st, h in rows
    )
    return (
        f"---\nkind: goal\nid: G-001\nproject: lantern-depths\nstatus: {status}\ncreated: 2026-10-10\n---\n"
        f"# G-001: test\n\n## Owner request\n\n> {REQUEST}\n\n## Interpretation\n\nx\n\n## Unknowns\n\nx\n\n"
        f"## Route\n\n| # | Stage | Role | Skills | Status | Handoff |\n|---|---|---|---|---|---|\n{table}\n"
        "## Route changes\n\nNone.\n\n## Next action\n\nx\n\n## Outcome\n\n—\n"
    )


def handoff(seq, frm, to, stage, loads, findings="x", extra="", outcome="routed"):
    return (
        f"---\nkind: handoff\ngoal: G-001\nseq: {seq}\nfrom: {frm}\nto: {to}\nstage: {stage}\noutcome: {outcome}\n---\n"
        f"# {seq:02d}: {frm} → {to} — test\n\n## Task\n\nx\n\n## Context\n\nx\n\n## Findings\n\n{findings}\n\n"
        "## Decisions already made\n\nNone.\n\n## Constraints\n\nNone.\n\n## Open questions\n\nNone.\n\n"
        f"## Expected output\n\nx\n\n{extra}## Load\n\n"
        + "".join(f"- {l}\n" for l in loads)
    )


def block(path, content):
    return f"<<<FILE {path}\n{content}>>>END\n"


@pytest.fixture
def ws(tmp_path):
    workspace = tmp_path / "ws"
    assert sr.main(["init", str(workspace), "--from", str(FIXTURE)]) == 0
    (workspace / "project" / G).mkdir(parents=True)
    return workspace


def write(ws, path, text):
    (ws / "project" / path).parent.mkdir(parents=True, exist_ok=True)
    (ws / "project" / path).write_text(text, encoding="utf-8")


def fake(outputs, sessions):
    """A runtime that returns canned outputs and records each fresh 'session'."""

    def run(packet_text, model=None):
        sessions.append(packet_text)
        return {
            "runtime": "fake",
            "text": outputs.pop(0),
            "session_id": f"fake-{len(sessions)}",
            "model": "fake",
            "tools": [],
            "mcp_servers": [],
            "tool_uses": [],
            "usage": None,
            "cost_usd": None,
        }

    return run


def args(**kw):
    return SimpleNamespace(
        **{
            "runtime": "fake",
            "model": None,
            "retries": 0,
            "goal": None,
            "handoff": None,
            **kw,
        }
    )


ENGINEER_LOAD = [
    "studio/roles/gameplay-engineer.md",
    "studio/skills/implement-change.md",
    "design/combat.md",
    "sim/repo-notes.md",
]
QA_LOAD = [
    "studio/roles/qa.md",
    "studio/skills/verify-change.md",
    "design/combat.md",
    "sim/build-0.3.md",
]
PLAYTESTER_LOAD = [
    "studio/roles/playtester.md",
    "studio/skills/playtest-session.md",
    "project.md#player-profile",
    "sim/build-0.3.md",
]


def labels(packet):
    return [label for label, _ in packet.inputs]


# --- Packet = allowlist ------------------------------------------------------------------------


def test_step_packet_contains_exactly_the_handoff_and_its_load_list(ws):
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    1,
                    "Build",
                    "gameplay-engineer",
                    "implement-change",
                    "open",
                    "01-studio-to-gameplay-engineer.md",
                )
            ]
        ),
    )
    write(
        ws,
        f"{G}/01-studio-to-gameplay-engineer.md",
        handoff(1, "studio", "gameplay-engineer", "Build", ENGINEER_LOAD),
    )
    project = ws / "project"
    packet, _ = sr.build_step(
        project, project / G, project / G / "01-studio-to-gameplay-engineer.md"
    )
    assert labels(packet) == [
        "studio/execution.md#executor-instructions",
        f"{G}/01-studio-to-gameplay-engineer.md",
        *ENGINEER_LOAD,
        "studio/templates/handoff.md",
    ]
    rendered = packet.render()
    assert re.findall(r"^<<<FILE (\S+)$", rendered, re.M) == labels(packet)
    assert (
        "ZX-DESIGN-4420" in rendered and "ZX-IMPL-7731" in rendered
    )  # engineer may know both


def test_section_entries_load_only_that_section(ws):
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    1,
                    "Observe",
                    "playtester",
                    "playtest-session",
                    "open",
                    "01-studio-to-playtester.md",
                )
            ]
        ),
    )
    write(
        ws,
        f"{G}/01-studio-to-playtester.md",
        handoff(1, "studio", "playtester", "Observe", PLAYTESTER_LOAD),
    )
    project = ws / "project"
    packet, _ = sr.build_step(
        project, project / G, project / G / "01-studio-to-playtester.md"
    )
    profile = dict(packet.inputs)["project.md#player-profile"]
    assert (
        profile.startswith("## Player profile")
        and "Constraints" not in profile
        and "Vision" not in profile
    )


# --- Engineer -> QA: unrecorded reasoning and self-assessment never reach QA --------------------


def test_engineer_reasoning_and_self_assessment_do_not_reach_qa(ws, monkeypatch):
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    1,
                    "Build",
                    "gameplay-engineer",
                    "implement-change",
                    "open",
                    "01-studio-to-gameplay-engineer.md",
                ),
                (2, "Verify", "qa", "verify-change", "planned", "—"),
            ]
        ),
    )
    write(
        ws,
        f"{G}/01-studio-to-gameplay-engineer.md",
        handoff(1, "studio", "gameplay-engineer", "Build", ENGINEER_LOAD),
    )
    engineer_handoff = handoff(
        2,
        "gameplay-engineer",
        "qa",
        "Verify",
        QA_LOAD,
        outcome="done",
        findings="Changed the invulnerability timer. Exercise: dash after a hit.",
        extra="## Sender assessment\n\nRoot cause found; own tests pass. CANARY-SELF-ASSESSMENT\n\n",
    )
    raw = (
        "I think the real issue is CANARY-UNRECORDED-REASONING; I also read ZX-IMPL-7731.\n"
        + block(f"{G}/02-gameplay-engineer-to-qa.md", engineer_handoff)
    )
    simulated = block(
        "sim/build-0.4.md", "# Build 0.4\n\nDashing after a hit now protects you.\n"
    ) + block("sim/repo-notes.md", "# Notes\n\nInvulnerability uses one end time.\n")
    sessions = []
    monkeypatch.setitem(sr.RUNTIMES, "fake", fake([raw, simulated], sessions))
    sr.do_step(ws, args())
    project = ws / "project"
    assert (
        len(sessions) == 2 and "CANARY-UNRECORDED-REASONING" not in sessions[1]
    )  # simulator: artifacts only
    assert (
        "CANARY-UNRECORDED-REASONING"
        not in (project / G / "02-gameplay-engineer-to-qa.md").read_text()
    )
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    1,
                    "Build",
                    "gameplay-engineer",
                    "implement-change",
                    "done",
                    "01-studio-to-gameplay-engineer.md",
                ),
                (
                    2,
                    "Verify",
                    "qa",
                    "verify-change",
                    "open",
                    "02-gameplay-engineer-to-qa.md",
                ),
            ]
        ),
    )
    qa_packet, _ = sr.build_step(
        project, project / G, project / G / "02-gameplay-engineer-to-qa.md"
    )
    text = qa_packet.render()
    for canary in (
        "CANARY-UNRECORDED-REASONING",
        "CANARY-SELF-ASSESSMENT",
        "own tests pass",
        "ZX-IMPL-7731",
    ):
        assert canary not in text, canary
    assert "Changed the invulnerability timer" in text


def test_self_assessment_outside_its_section_is_rejected_for_qa(ws):
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    2,
                    "Verify",
                    "qa",
                    "verify-change",
                    "open",
                    "02-gameplay-engineer-to-qa.md",
                )
            ]
        ),
    )
    write(
        ws,
        f"{G}/02-gameplay-engineer-to-qa.md",
        handoff(
            2,
            "gameplay-engineer",
            "qa",
            "Verify",
            QA_LOAD,
            findings="Root cause fixed; all tests pass.",
        ),
    )
    project = ws / "project"
    with pytest.raises(sr.Rejected, match="self-assessment"):
        sr.build_step(
            project, project / G, project / G / "02-gameplay-engineer-to-qa.md"
        )


# --- Designer/Engineer -> Playtester: expected results never reach the Playtester ---------------


def test_expected_results_placed_for_the_playtester_are_not_passed(ws):
    write(
        ws,
        "design/expected-results.md",
        "# Expected\n\nPlayers should now dodge. CANARY-EXPECTED-RESULT\n",
    )
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    3,
                    "Play",
                    "playtester",
                    "playtest-session",
                    "open",
                    "03-studio-to-playtester.md",
                )
            ]
        ),
    )
    project = ws / "project"
    cases = {
        "clean": handoff(3, "studio", "playtester", "Play", PLAYTESTER_LOAD),
        "in-load": handoff(
            3,
            "studio",
            "playtester",
            "Play",
            PLAYTESTER_LOAD + ["design/expected-results.md"],
        ),
        "from-designer": handoff(
            3, "studio", "playtester", "Play", PLAYTESTER_LOAD
        ).replace("from: studio", "from: game-designer"),
        "owner-request": handoff(
            3, "studio", "playtester", "Play", PLAYTESTER_LOAD, findings=REQUEST
        ),
        "sender-assessment": handoff(
            3,
            "studio",
            "playtester",
            "Play",
            PLAYTESTER_LOAD,
            extra="## Sender assessment\n\nCANARY-EXPECTED-RESULT\n\n",
        ),
    }
    for case, text in cases.items():
        name = (
            "03-game-designer-to-playtester.md"
            if case == "from-designer"
            else "03-studio-to-playtester.md"
        )
        for old in (project / G).glob("03-*"):
            old.unlink()
        write(ws, f"{G}/{name}", text)
        if case == "clean":
            packet, _ = sr.build_step(project, project / G, project / G / name)
            rendered = packet.render()
            assert (
                "CANARY-EXPECTED-RESULT" not in rendered
                and "ZX-DESIGN-4420" not in rendered
            )
            assert "ZX-IMPL-7731" not in rendered and REQUEST not in rendered
        else:
            with pytest.raises(sr.Rejected):
                sr.build_step(project, project / G, project / G / name)


def test_engineer_may_not_load_playtester_reports(ws):
    write(
        ws,
        f"{G}/01-studio-to-playtester.md",
        handoff(1, "studio", "playtester", "Observe", PLAYTESTER_LOAD),
    )
    write(
        ws,
        f"{G}/02-playtester-to-game-designer.md",
        handoff(2, "playtester", "game-designer", "Diagnose", []),
    )
    write(
        ws,
        f"{G}/03-studio-to-gameplay-engineer.md",
        handoff(
            3,
            "studio",
            "gameplay-engineer",
            "Build",
            ENGINEER_LOAD + [f"{G}/02-playtester-to-game-designer.md"],
        ),
    )
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [
                (
                    3,
                    "Build",
                    "gameplay-engineer",
                    "implement-change",
                    "open",
                    "03-studio-to-gameplay-engineer.md",
                )
            ]
        ),
    )
    project = ws / "project"
    with pytest.raises(sr.Rejected, match="may not load"):
        sr.build_step(
            project, project / G, project / G / "03-studio-to-gameplay-engineer.md"
        )


# --- Steps cannot route; outputs are limited to the write list ---------------------------------


def test_step_write_list_blocks_routing_and_other_artifacts(ws):
    write(
        ws,
        f"{G}/goal.md",
        goal([(1, "Observe", "qa", "reproduce-defect", "open", "01-studio-to-qa.md")]),
    )
    write(ws, f"{G}/01-studio-to-qa.md", handoff(1, "studio", "qa", "Observe", QA_LOAD))
    project = ws / "project"
    _, validate = sr.build_step(
        project, project / G, project / G / "01-studio-to-qa.md"
    )
    good = handoff(2, "qa", "gameplay-engineer", "Build", [], outcome="done")
    assert validate({f"{G}/02-qa-to-gameplay-engineer.md": good}) == []
    bad_cases = [
        {
            f"{G}/02-qa-to-gameplay-engineer.md": good,
            f"{G}/goal.md": goal([]),
        },  # routing
        {
            f"{G}/02-qa-to-gameplay-engineer.md": good,
            "design/combat.md": "x",
        },  # spec change
        {
            f"{G}/02-qa-to-gameplay-engineer.md": good,
            "../studio/roles/qa.md": "x",
        },  # escape
        {
            f"{G}/02-qa-to-gameplay-engineer.md": good.replace(
                "from: qa", "from: game-designer"
            )
        },
        {
            f"{G}/03-qa-to-gameplay-engineer.md": good.replace("seq: 2", "seq: 3")
        },  # wrong seq
    ]
    for files in bad_cases:
        assert validate(files), files


def test_text_outside_file_blocks_is_discarded():
    out = "thinking SECRET\n" + block("a.md", "kept\n") + "more SECRET\n"
    assert sr.parse_output(out) == {"a.md": "kept\n"}


# --- Route sees artifacts only and is reproducible from them -----------------------------------


def test_route_packet_is_built_from_artifacts_only(ws, monkeypatch):
    write(
        ws,
        f"{G}/goal.md",
        goal([(1, "Observe", "qa", "reproduce-defect", "open", "01-studio-to-qa.md")]),
    )
    write(ws, f"{G}/01-studio-to-qa.md", handoff(1, "studio", "qa", "Observe", QA_LOAD))
    raw = "hidden CANARY-STEP-CONVERSATION\n" + block(
        f"{G}/02-qa-to-gameplay-engineer.md",
        handoff(2, "qa", "gameplay-engineer", "Build", [], outcome="done"),
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", fake([raw], []))
    sr.do_step(ws, args())
    project = ws / "project"
    first, _ = sr.build_route(project, project / G)
    second, _ = sr.build_route(project, project / G)
    assert first.render() == second.render()
    names = labels(first)
    assert f"{G}/goal.md" in names and f"{G}/02-qa-to-gameplay-engineer.md" in names
    assert f"{G}/01-studio-to-qa.md" not in names
    assert not any("records" in n for n in names)
    assert "CANARY-STEP-CONVERSATION" not in first.render()


def test_route_rejects_an_open_step_that_breaks_recipient_policy(ws):
    write(
        ws,
        f"{G}/goal.md",
        goal([(1, "Verify", "qa", "verify-change", "done", "01-studio-to-qa.md")]),
    )
    write(ws, f"{G}/01-studio-to-qa.md", handoff(1, "studio", "qa", "Verify", QA_LOAD))
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="pass"),
    )
    project = ws / "project"
    _, validate = sr.build_route(project, project / G)
    leaky = handoff(
        3, "studio", "playtester", "Play", PLAYTESTER_LOAD + ["sim/repo-notes.md"]
    )
    rows = [
        (1, "Verify", "qa", "verify-change", "done", "01-studio-to-qa.md"),
        (
            2,
            "Play",
            "playtester",
            "playtest-session",
            "open",
            "03-studio-to-playtester.md",
        ),
    ]
    errors = validate(
        {f"{G}/goal.md": goal(rows), f"{G}/03-studio-to-playtester.md": leaky}
    )
    assert any("may not load sim/repo-notes.md" in e for e in errors)
    clean = handoff(3, "studio", "playtester", "Play", PLAYTESTER_LOAD)
    assert (
        validate({f"{G}/goal.md": goal(rows), f"{G}/03-studio-to-playtester.md": clean})
        == []
    )


# --- Owner escalation -> Decision -> fresh resume ----------------------------------------------


def test_owner_decision_resumes_in_a_fresh_executor(ws, monkeypatch):
    escalation = (
        "---\nkind: escalation\ngoal: G-001\nseq: 1\nfrom: game-director\nto: owner\nstatus: open\ndecision: none\n---\n"
        "# 01: Owner decision needed\n\n## Question\n\nA or B?\n\n## Why this needs the Owner\n\nx\n\n"
        "## Options\n\n### Option A\n\nx\n\n### Option B\n\nx\n\n## Studio recommendation\n\nA\n\n"
        "## Reasoning\n\nx\n\n## Owner decision required\n\nA / B\n"
    )
    write(ws, f"{G}/01-game-director-to-owner.md", escalation)
    write(
        ws,
        f"{G}/goal.md",
        goal(
            [(1, "Decide", "owner", "—", "open", "01-game-director-to-owner.md")],
            status="blocked-on-owner",
        ),
    )
    sessions = []
    decision = (
        "---\nkind: decision\nid: D-002\nstatus: accepted\ndecided_by: owner\ngoal: G-001\ndate: 2026-10-10\nsupersedes: none\n---\n"
        "# D-002: A\n\n## Decision\n\nA. Owner's words: Aで。\n\n## Rationale\n\nx\n\n## Alternatives considered\n\nB\n\n## Revisit when\n\nx\n"
    )
    designer = handoff(
        2,
        "studio",
        "game-designer",
        "Design",
        [
            "studio/roles/game-designer.md",
            "studio/skills/write-design-spec.md",
            "decisions/D-002-a.md",
        ],
    )
    rows = [
        (1, "Decide", "owner", "—", "done (D-002)", "01-game-director-to-owner.md"),
        (
            2,
            "Design",
            "game-designer",
            "write-design-spec",
            "open",
            "02-studio-to-game-designer.md",
        ),
    ]
    resolved = (
        escalation.replace("status: open", "status: resolved").replace(
            "decision: none", "decision: D-002"
        )
        + "\n**Owner response (2026-10-10):** Aで。\n"
    )
    out = (
        block("decisions/D-002-a.md", decision)
        + block(f"{G}/01-game-director-to-owner.md", resolved)
        + block(f"{G}/goal.md", goal(rows))
        + block(f"{G}/02-studio-to-game-designer.md", designer)
    )
    dropped = out.replace(
        "Owner's words: Aで。", ""
    )  # a Decision that loses the Owner's words
    monkeypatch.setitem(sr.RUNTIMES, "fake", fake([dropped, out], sessions))
    sr.do_decide(ws, args(text="Aで。", retries=1))
    assert len(sessions) == 2  # first attempt rejected
    assert (
        "Owner response" in sessions[0] and "Aで。" in sessions[0]
    )  # resume packet carries the words
    project = ws / "project"
    packet, _ = sr.build_step(
        project, project / G, project / G / "02-studio-to-game-designer.md"
    )
    assert "decisions/D-002-a.md" in labels(packet)  # next fresh step gets the Decision
    record = json.loads(next((ws / "records").glob("*-resume/record.json")).read_text())
    assert record["status"] == "ok" and record["decision"]["open"] == [
        ["game-designer", "Design"]
    ]


# --- Runtime isolation -------------------------------------------------------------------------


def test_claude_runtime_starts_isolated_and_refuses_tools(monkeypatch):
    calls = []

    def fake_run(cmd, **kw):
        calls.append((cmd, kw))
        init = {
            "type": "system",
            "subtype": "init",
            "tools": fake_run.tools,
            "mcp_servers": [],
            "model": "m",
            "session_id": "s",
        }
        result = {
            "type": "result",
            "result": "ok",
            "session_id": "s",
            "usage": {},
            "total_cost_usd": 0,
        }
        return subprocess.CompletedProcess(
            cmd, 0, json.dumps(init) + "\n" + json.dumps(result) + "\n", ""
        )

    fake_run.tools = []
    monkeypatch.setattr(sr.subprocess, "run", fake_run)
    sr.run_claude("packet")
    cmd, kw = calls[0]
    for flag in (
        "--tools",
        "--setting-sources",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--no-session-persistence",
    ):
        assert flag in cmd
    assert (
        cmd[cmd.index("--tools") + 1] == ""
        and cmd[cmd.index("--setting-sources") + 1] == "project"
    )
    assert (
        kw["env"]["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] == "1"
        and "--resume" not in cmd
        and "--continue" not in cmd
    )
    assert "gamewright" not in kw["cwd"].lower()
    fake_run.tools = ["Read"]
    with pytest.raises(sr.Rejected, match="isolation"):
        sr.run_claude("packet")


# --- Recorded live runs ------------------------------------------------------------------------


def run_records():
    return sorted(RUNS.glob("*/records/*/record.json")) if RUNS.is_dir() else []


@pytest.mark.skipif(not run_records(), reason="no recorded runs")
def test_recorded_packets_match_their_manifests_and_load_lists():
    for path in run_records():
        record, rec = json.loads(path.read_text()), path.parent
        if not (rec / "packet.md").exists():
            continue
        packet = (rec / "packet.md").read_text()
        manifest = json.loads((rec / "manifest.json").read_text())
        found = re.findall(r"^<<<FILE (\S+)\n(.*?)>>>END$", packet, re.M | re.S)
        assert [l for l, _ in found] == [m["path"] for m in manifest], rec
        assert [sr.sha(c) for _, c in found] == [m["sha256"] for m in manifest], rec
        if record["op"] == "Step":
            project = rec.parent.parent / "project"
            incoming = re.search(r"^incoming_handoff: (\S+)$", packet, re.M).group(1)
            loads = sr.load_entries((project / incoming).read_text())
            expected = {"studio/execution.md#executor-instructions", incoming, *loads}
            assert expected <= {m["path"] for m in manifest}, rec
            extra = {m["path"] for m in manifest} - expected
            assert all(p.startswith("studio/templates/") for p in extra), (rec, extra)


@pytest.mark.skipif(not run_records(), reason="no recorded runs")
def test_recorded_runs_use_a_fresh_isolated_executor_per_operation():
    sessions = {}  # per run: a run continued from a copy of another repeats its records
    for path in run_records():
        record = json.loads(path.read_text())
        run = sessions.setdefault(path.parent.parent.parent.name, [])
        for attempt in record.get("attempts", []):
            run.append(attempt["session_id"])
            assert attempt["tool_uses"] == [] and attempt["mcp_servers"] == []
            if attempt["runtime"] == "claude":
                assert attempt["tools"] == []
        if "of" in record:
            run.append(record["session_id"])
    for name, run in sessions.items():
        assert len(run) == len(set(run)), f"{name}: a session identity was reused"


@pytest.mark.skipif(not run_records(), reason="no recorded runs")
def test_recorded_isolation_canaries():
    for path in run_records():
        record, rec = json.loads(path.read_text()), path.parent
        packet = (rec / "packet.md").read_text() if (rec / "packet.md").exists() else ""
        if record.get("role") == "playtester":
            assert "ZX-DESIGN-4420" not in packet and "ZX-IMPL-7731" not in packet, rec
        if record.get("role") in (
            "qa",
            "playtester",
        ):  # no sender self-assessment outside templates
            for label, content in re.findall(
                r"^<<<FILE (\S+)\n(.*?)>>>END$", packet, re.M | re.S
            ):
                if not label.startswith("studio/"):
                    assert not re.search(r"^## Sender assessment\s*$", content, re.M), (
                        rec,
                        label,
                    )
        if (
            record.get("op") == "Route"
        ):  # only the step artifacts its header names; no records
            header = re.search(r"^step_artifacts?: (.+)$", packet, re.M).group(1)
            listed = {a.strip() for a in header.split(",")}
            shown = set(re.findall(r"^<<<FILE (goals/\S+/\d\d-\S+)$", packet, re.M))
            assert shown == listed, rec
            assert "records/" not in packet, rec


@pytest.mark.skipif(not RUNS.is_dir(), reason="no recorded runs")
def test_recorded_run_artifacts_follow_the_studio_rules():
    for project in RUNS.glob("*/project"):
        for gdir in (project / "goals").glob("G-*"):
            text = (gdir / "goal.md").read_text()
            assert sr.check_goal(text) == [], gdir
            request = sr.owner_request(gdir)
            for artifact, meta in sr.goal_artifacts(gdir):
                errors = sr.check_artifact(
                    project,
                    str(artifact.relative_to(project)),
                    artifact.read_text(),
                    request,
                    full=meta.get("from") == "studio",
                )
                assert errors == [], errors


# --- Cross-runtime artifact formats ------------------------------------------------------------


def test_route_handoff_cells_accept_name_link_or_path():
    table = (
        "## Route\n\n| # | Stage | Role | Skills | Status | Handoff |\n|---|---|---|---|---|---|\n"
        "| 1 | Observe | qa | reproduce-defect | open | 01-studio-to-qa.md |\n"
        "| 2 | Build | qa | x | open | [02-a-to-qa.md](02-a-to-qa.md) |\n"
        "| 3 | Verify | qa | x | open | goals/G-001-x/03-b-to-qa.md |\n"
    )
    assert [r["handoff"] for r in sr.route_rows(table)] == [
        "01-studio-to-qa.md",
        "02-a-to-qa.md",
        "03-b-to-qa.md",
    ]


def test_load_anchors_are_normalized_to_heading_slugs():
    text = handoff(
        1,
        "studio",
        "qa",
        "Observe",
        ["project.md#Constraints", "project.md#current-state", "design/combat.md"],
    )
    assert sr.load_entries(text) == [
        "project.md#constraints",
        "project.md#current-state",
        "design/combat.md",
    ]
