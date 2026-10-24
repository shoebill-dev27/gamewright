"""Phase 3: continuous execution until the Owner is needed. Deterministic — a fake runtime stands in.

Run with `python3 -m pytest tests/`.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import (
    G,
    QA_LOAD,
    args,
    block,
    goal,
    handoff,
    sr,
    write,
    ws,
)  # noqa: E402,F401

DIRECTOR_LOAD = ["studio/roles/game-director.md", "studio/skills/make-decision.md"]
ART_LOAD = ["studio/roles/art-director.md", "studio/skills/visual-review.md"]
ESCALATION = (
    "---\nkind: escalation\ngoal: G-001\nseq: 2\nfrom: game-director\nto: owner\nstatus: open\ndecision: none\n---\n"
    "# 02: Owner decision needed\n\n## Question\n\nA or B?\n\n## Why this needs the Owner\n\nx\n\n"
    "## Options\n\n### Option A\n\nx\n\n### Option B\n\nx\n\n## Studio recommendation\n\nA\n\n"
    "## Reasoning\n\nx\n\n## Owner decision required\n\nA / B\n"
)


def runtime(outputs, sessions):
    """Fake runtime: returns outputs in order; an Exception instance is raised instead."""

    def run(packet_text, model=None):
        sessions.append(packet_text)
        out = outputs.pop(0)
        if isinstance(out, Exception):
            raise out
        return {
            "runtime": "fake",
            "text": out,
            "session_id": f"fake-{len(sessions)}",
            "model": "fake",
            "tools": [],
            "mcp_servers": [],
            "tool_uses": [],
            "usage": None,
            "cost_usd": None,
        }

    return run


def route_out(rows, status="active", new=()):
    return block(f"{G}/goal.md", goal(rows, status=status)) + "".join(
        block(f"{G}/{n}", t) for n, t in new
    )


def summary(ws):
    return json.loads(
        sorted((ws / "records").glob("*-run/record.json"))[-1].read_text()
    )


def start(ws, first, rows):
    write(ws, f"{G}/goal.md", goal(rows))
    write(ws, f"{G}/{first[0]}", first[1])


QA_OPEN = ("01-studio-to-qa.md", handoff(1, "studio", "qa", "Observe", QA_LOAD))


def test_run_continues_until_the_goal_is_done(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    sessions = []
    outputs = [
        block(
            f"{G}/02-qa-to-studio.md",
            handoff(2, "qa", "studio", "Next", [], outcome="pass"),
        ),
        route_out(
            [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])],
            status="done",
        ),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    assert sr.do_run(ws, args(max_ops=25)) == 0
    s = summary(ws)
    assert (
        s["stop_reason"] == "done"
        and len(sessions) == 2
        and s["owner_reads"].endswith("goal.md#outcome")
    )
    assert s["next"] is None


def test_run_stops_at_an_owner_escalation(ws, monkeypatch):
    first = (
        "01-studio-to-game-director.md",
        handoff(1, "studio", "game-director", "Decide", DIRECTOR_LOAD),
    )
    start(
        ws, first, [(1, "Decide", "game-director", "make-decision", "open", first[0])]
    )
    sessions = []
    outputs = [
        block(f"{G}/02-game-director-to-owner.md", ESCALATION),
        route_out(
            [
                (1, "Decide", "game-director", "make-decision", "done", first[0]),
                (2, "Decide", "owner", "—", "open", "02-game-director-to-owner.md"),
            ],
            status="blocked-on-owner",
        ),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    assert sr.do_run(ws, args(max_ops=25)) == 0
    s = summary(ws)
    assert s["stop_reason"] == "blocked-on-owner" and len(sessions) == 2
    assert s["owner_reads"] == f"{G}/02-game-director-to-owner.md" and s[
        "next"
    ].startswith("decide")


def cycle_outputs(cycles, outcome):
    """Each cycle: QA reports to the Studio, the Route reopens QA with a new Studio handoff."""
    outputs, seq = [], 2
    for _ in range(cycles):
        outputs.append(
            block(
                f"{G}/{seq:02d}-qa-to-studio.md",
                handoff(seq, "qa", "studio", "Route", [], outcome=outcome),
            )
        )
        nxt = f"{seq + 1:02d}-studio-to-qa.md"
        outputs.append(
            route_out(
                [(1, "Observe", "qa", "reproduce-defect", "open", nxt)],
                new=[(nxt, handoff(seq + 1, "studio", "qa", "Observe", QA_LOAD))],
            )
        )
        seq += 2
    return outputs


def test_run_respects_its_operation_budget(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    sessions = []
    monkeypatch.setitem(
        sr.RUNTIMES, "fake", runtime(cycle_outputs(5, "done"), sessions)
    )
    sr.do_run(ws, args(max_ops=4))
    assert len(sessions) == 4 and "budget" in summary(ws)["stop_reason"]


def test_run_stops_when_a_role_keeps_handing_back_questions(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    sessions = []
    monkeypatch.setitem(
        sr.RUNTIMES, "fake", runtime(cycle_outputs(5, "question"), sessions)
    )
    sr.do_run(ws, args(max_ops=25))
    assert len(sessions) == 4 and summary(ws)["stop_reason"].startswith(
        "no progress: qa handed back"
    )


def test_run_stops_on_a_runtime_error_without_writing(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    before = (ws / "project" / G / "goal.md").read_text()
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([RuntimeError("usage limit")], []))
    assert sr.do_run(ws, args(max_ops=25)) == 3
    assert summary(ws)["stop_reason"].startswith("runtime error") and summary(ws)[
        "next"
    ].startswith("run")
    assert (ws / "project" / G / "goal.md").read_text() == before


def test_parallel_steps_run_before_one_route_that_sees_both(ws, monkeypatch):
    art = (
        "02-studio-to-art-director.md",
        handoff(2, "studio", "art-director", "Verify", ART_LOAD),
    )
    start(
        ws,
        QA_OPEN,
        [
            (1, "Verify", "qa", "verify-change", "open", QA_OPEN[0]),
            ("1b", "Verify", "art-director", "visual-review", "open", art[0]),
        ],
    )
    write(ws, f"{G}/{art[0]}", art[1])
    (ws / "records" / "001-route").mkdir()
    (ws / "records" / "001-route" / "record.json").write_text(
        json.dumps(
            {"op": "Route", "goal": "G-001", "status": "ok", "seen_through_seq": 2}
        )
    )
    sessions = []
    outputs = [
        block(
            f"{G}/03-qa-to-studio.md",
            handoff(3, "qa", "studio", "Route", [], outcome="pass"),
        ),
        block(
            f"{G}/04-art-director-to-studio.md",
            handoff(4, "art-director", "studio", "Route", [], outcome="pass"),
        ),
        route_out(
            [(1, "Verify", "qa", "verify-change", "done", QA_OPEN[0])], status="done"
        ),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_run(ws, args(max_ops=25))
    route_packet = sessions[2]
    assert (
        f"<<<FILE {G}/03-qa-to-studio.md" in route_packet
        and f"<<<FILE {G}/04-art-director-to-studio.md" in route_packet
    )
    assert (
        f"<<<FILE {G}/01-studio-to-qa.md" not in route_packet
    )  # already seen by the previous Route
    assert summary(ws)["stop_reason"] == "done"


def test_route_may_request_more_context_once(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])])
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="done"),
    )
    sessions = []
    need = block("@need", f"design/combat.md\n{G}/01-studio-to-qa.md\n")
    done = route_out(
        [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])], status="done"
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([need, done], sessions))
    sr.do_route(ws, args())
    assert (
        "<<<FILE design/combat.md" not in sessions[0]
        and "<<<FILE design/combat.md" in sessions[1]
    )
    assert "@need" not in sessions[1].split("## Inputs")[0]  # no second request offered
    record = json.loads(next((ws / "records").glob("*-route/record.json")).read_text())
    assert (
        record["attempts"][0]["need"] == ["design/combat.md", f"{G}/01-studio-to-qa.md"]
        and record["status"] == "ok"
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([need, need], []))
    write(
        ws,
        f"{G}/goal.md",
        goal([(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])]),
    )
    with pytest.raises(sr.Rejected):
        sr.do_route(ws, args())


def test_context_requests_stay_inside_the_project_and_studio(ws):
    project = ws / "project"
    assert (
        sr.check_need(
            project,
            ["design/combat.md", "studio/roles/qa.md", "project.md#constraints"],
        )
        == []
    )
    for bad in (
        ["records/001-intake/packet.md"],
        ["../AGENTS.md"],
        ["/etc/passwd"],
        ["nope.md"],
        ["project.md#nope"],
        [f"design/combat.md"] * 9,
        [],
    ):
        assert sr.check_need(project, bad), bad


def test_route_may_open_several_steps_with_consecutive_handoffs(ws):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])])
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="done"),
    )
    project = ws / "project"
    _, validate = sr.build_route(project, project / G, ws / "records")
    qa3, art4 = handoff(3, "studio", "qa", "Verify", QA_LOAD), handoff(
        4, "studio", "art-director", "Verify", ART_LOAD
    )
    rows = [
        ("2a", "Verify", "qa", "verify-change", "open", "03-studio-to-qa.md"),
        (
            "2b",
            "Verify",
            "art-director",
            "visual-review",
            "open",
            "04-studio-to-art-director.md",
        ),
    ]
    assert (
        validate(
            {
                f"{G}/goal.md": goal(rows),
                f"{G}/03-studio-to-qa.md": qa3,
                f"{G}/04-studio-to-art-director.md": art4,
            }
        )
        == []
    )
    gap = {
        f"{G}/goal.md": goal(rows[:1]),
        f"{G}/03-studio-to-qa.md": qa3,
        f"{G}/05-studio-to-art-director.md": art4.replace("seq: 4", "seq: 5"),
    }
    assert any("consecutive" in e for e in validate(gap))


def test_route_cells_keep_only_the_handoff_file_name():
    table = (
        "## Route\n\n| # | Stage | Role | Skills | Status | Handoff |\n|---|---|---|---|---|---|\n"
        "| 4a | Verify | qa | x | open | [12-studio-to-qa.md](12-studio-to-qa.md) (earlier: 09-studio-to-qa.md) |\n"
    )
    assert sr.route_rows(table)[0]["handoff"] == "12-studio-to-qa.md"
    primed = table.replace("| 4a |", "| 4a′ |")
    assert [r["n"] for r in sr.route_rows(primed)] == [
        "4a′"
    ]  # row labels may carry primes


def test_run_routes_unrouted_artifacts_before_stepping_again(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="pass"),
    )  # Route failed after this
    (ws / "records" / "001-intake").mkdir()
    (ws / "records" / "001-intake" / "record.json").write_text(
        json.dumps(
            {
                "op": "Intake",
                "goal": "G-001 (new)",
                "status": "ok",
                "seen_through_seq": 1,
            }
        )
    )
    sessions = []
    done = route_out(
        [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])], status="done"
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([done], sessions))
    sr.do_run(ws, args(max_ops=25))
    assert len(sessions) == 1 and "operation: Route" in sessions[0]  # no second QA Step
    assert summary(ws)["stop_reason"] == "done"


def test_route_packets_name_the_current_simulated_build(ws):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])])
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="done"),
    )
    write(ws, "sim/build-0.10.md", "# newer\n")  # numeric, not lexical, order
    project = ws / "project"
    packet, _ = sr.build_route(project, project / G, ws / "records")
    assert packet.header["current_build"].startswith("sim/build-0.10.md")


def test_an_unwrapped_context_request_is_still_understood():
    assert sr.parse_output("@need\ndesign/combat.md\nproject.md\n") == {
        "@need": "design/combat.md\nproject.md\n"
    }
    assert sr.parse_output("thinking\n" + block("a.md", "x\n")) == {"a.md": "x\n"}


def test_blocked_on_owner_needs_an_open_escalation(ws):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])])
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="question"),
    )
    project = ws / "project"
    _, validate = sr.build_route(project, project / G, ws / "records")
    td = handoff(
        3,
        "studio",
        "technical-director",
        "Decide",
        ["studio/roles/technical-director.md"],
    )
    rows = [
        (
            2,
            "Decide",
            "technical-director",
            "prepare-owner-escalation",
            "open",
            "03-studio-to-technical-director.md",
        )
    ]
    premature = {
        f"{G}/goal.md": goal(rows, status="blocked-on-owner"),
        f"{G}/03-studio-to-technical-director.md": td,
    }
    assert any("needs an open Escalation" in e for e in validate(premature))
    assert (
        validate(
            {f"{G}/goal.md": goal(rows), f"{G}/03-studio-to-technical-director.md": td}
        )
        == []
    )


def test_route_since_re_routes_earlier_artifacts(ws):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])])
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        handoff(2, "qa", "studio", "Route", [], outcome="question"),
    )
    write(ws, f"{G}/03-studio-to-qa.md", handoff(3, "studio", "qa", "Observe", QA_LOAD))
    project = ws / "project"
    packet, _ = sr.build_route(project, project / G, ws / "records", since=1)
    assert (
        packet.header["step_artifacts"]
        == f"{G}/02-qa-to-studio.md, {G}/03-studio-to-qa.md"
    )
