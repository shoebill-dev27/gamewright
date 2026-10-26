"""Phase 13: a Goal's operation budget — set at Intake, shown to Routes, and no new stages past it.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import (
    G,
    REQUEST,
    args,
    block,
    goal,
    handoff,
    sr,
    write,
    ws,
)  # noqa: E402,F401
from test_phase3 import QA_LOAD, QA_OPEN, runtime, start  # noqa: E402

DONE_ROW = (1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])
NEXT = ("03-studio-to-qa.md", handoff(3, "studio", "qa", "Verify", QA_LOAD))
VERIFY = (2, "Verify", "qa", "verify-change", "open", NEXT[0])
EXTRA = (3, "Play", "playtester", "playtest-session", "planned", "—")


def intake(ws, monkeypatch, budget):
    gdir = "goals/G-002-dash"
    text = goal(
        [(1, "Observe", "qa", "reproduce-defect", "open", "01-studio-to-qa.md")],
        budget=budget,
    )
    out = block(f"{gdir}/goal.md", text) + block(
        f"{gdir}/01-studio-to-qa.md", handoff(1, "studio", "qa", "Observe", QA_LOAD)
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([out], []))
    sr.execute(ws, *sr.build_intake(ws / "project", REQUEST), args())


def test_intake_sets_a_budget(ws, monkeypatch):
    intake(ws, monkeypatch, budget=12)
    assert "budget: 12" in (ws / "project" / "goals/G-002-dash/goal.md").read_text()


@pytest.mark.parametrize("budget", [None, "lots"])
def test_intake_without_a_whole_budget_is_rejected(ws, monkeypatch, budget):
    with pytest.raises(sr.Rejected):
        intake(ws, monkeypatch, budget=budget)
    rec = next((ws / "records").glob("*-intake"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]
    assert any("budget" in e for e in errors), errors


def route(ws, monkeypatch, rows, used, budget_out=30):
    planned = (*VERIFY[:4], "planned", "—")
    start(ws, QA_OPEN, [(*DONE_ROW[:4], "open", QA_OPEN[0]), planned])
    write(ws, f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Observe", []))
    monkeypatch.setattr(sr, "goal_ops", lambda records, gid: used)
    sessions = []
    answer = block(f"{G}/goal.md", goal(rows, budget=budget_out)) + block(
        f"{G}/{NEXT[0]}", NEXT[1]
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], sessions))
    sr.do_route(ws, args(goal="G-001", since=1))
    return sessions


def route_errors(ws):
    rec = next((ws / "records").glob("*-route"))
    return json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]


def test_the_route_sees_the_budget(ws, monkeypatch):
    sessions = route(ws, monkeypatch, [DONE_ROW, VERIFY, EXTRA], used=4)
    assert "goal_budget: 4 of 30 operations used\n" in sessions[0]


def test_over_budget_a_route_adds_no_stages(ws, monkeypatch):
    with pytest.raises(sr.Rejected):
        route(ws, monkeypatch, [DONE_ROW, VERIFY, EXTRA], used=30)
    assert any("add no stages but one" in e for e in route_errors(ws)), route_errors(ws)


def test_over_budget_a_route_may_still_route_planned_work(ws, monkeypatch):
    sessions = route(ws, monkeypatch, [DONE_ROW, VERIFY], used=31)
    assert "31 of 30 operations used — over budget" in sessions[0]
    assert (ws / "project" / G / NEXT[0]).is_file()


def test_a_route_keeps_the_budget(ws, monkeypatch):
    with pytest.raises(sr.Rejected):
        route(ws, monkeypatch, [DONE_ROW, VERIFY], used=4, budget_out=60)
    assert any("keep budget" in e for e in route_errors(ws)), route_errors(ws)


def test_a_goal_without_a_budget_gets_the_default():
    text = goal([], budget=None)
    assert sr.check_goal(text) == [] and sr.goal_budget(text) == sr.DEFAULT_BUDGET


def test_operations_are_counted_per_goal(tmp_path):
    records = tmp_path / "records"
    for name, op, gid in [
        ("001-intake", "Intake", "G-001 (new)"),
        ("002-step-qa", "Step", "G-001"),
        ("003-route", "Route", "G-001"),
        ("004-run", "Run", "G-001"),
        ("005-route", "Route", "G-002"),
    ]:
        (records / name).mkdir(parents=True)
        record = {"op": op, "goal": gid, "attempts": [{}] if op != "Run" else []}
        (records / name / "record.json").write_text(json.dumps(record))
    assert sr.goal_ops(records, "G-001") == 3


def test_over_budget_a_route_may_add_a_scope_decision(ws, monkeypatch):
    scope = (3, "Decide", "game-director", "make-decision", "planned", "—")
    route(ws, monkeypatch, [DONE_ROW, VERIFY, scope], used=31)
    assert "| Decide | game-director |" in (ws / "project" / G / "goal.md").read_text()


def test_writing_the_budget_a_goal_already_has_is_no_change(ws, monkeypatch):
    start(ws, QA_OPEN, [(*DONE_ROW[:4], "open", QA_OPEN[0])])
    write(ws, f"{G}/goal.md", goal([(*DONE_ROW[:4], "open", QA_OPEN[0])], budget=None))
    write(ws, f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Observe", []))
    answer = block(
        f"{G}/goal.md", goal([DONE_ROW], status="done", budget=sr.DEFAULT_BUDGET)
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    sr.do_route(ws, args(goal="G-001", since=1))


ESCALATION = (
    "---\nkind: escalation\ngoal: G-001\nseq: 1\nfrom: game-director\nto: owner\nstatus: open\n"
    "decision: none\n---\n# 01: Owner decision needed\n\n## Question\n\nGo on or stop?\n\n"
    "## Why this needs the Owner\n\nx\n\n## Options\n\n### Option A\n\nx\n\n### Option B\n\nx\n\n"
    "## Studio recommendation\n\nA\n\n## Reasoning\n\nx\n\n## Owner decision required\n\nA / B\n"
)
STOP = (
    "---\nkind: decision\nid: D-002\nstatus: accepted\ndecided_by: owner\ngoal: G-001\n"
    "date: 2026-10-23\nsupersedes: none\n---\n# D-002: stop\n\n## Decision\n\nB. Owner's words: "
    "Bで止める。\n\n## Rationale\n\nx\n\n## Alternatives considered\n\nA\n\n## Revisit when\n\nx\n"
)


def resume(ws, monkeypatch, status, outcome, project_text=None):
    write(ws, f"{G}/01-game-director-to-owner.md", ESCALATION)
    row = (1, "Decide", "owner", "—", "open", "01-game-director-to-owner.md")
    write(ws, f"{G}/goal.md", goal([row], status="blocked-on-owner"))
    resolved = (
        ESCALATION.replace("status: open", "status: resolved").replace(
            "decision: none", "decision: D-002"
        )
        + "\n**Owner response (2026-10-23):** Bで止める。\n"
    )
    closed = goal([(*row[:4], "done (D-002)", row[5])], status=status).replace(
        "## Outcome\n\n—\n", f"## Outcome\n\n{outcome}\n"
    )
    out = (
        block("decisions/D-002-stop.md", STOP)
        + block(f"{G}/01-game-director-to-owner.md", resolved)
        + block(f"{G}/goal.md", closed)
        + (block("project.md", project_text) if project_text else "")
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([out], []))
    sr.execute(ws, *sr.build_resume(ws / "project", ws / "project" / G), args())


def test_a_resume_may_close_the_goal_when_the_owner_stops_it(ws, monkeypatch):
    before = (ws / "project" / "project.md").read_text()
    state = sr.section(before, "Current state").strip()
    after = before.replace(state, state + " G-001 stopped unfinished.")
    resume(ws, monkeypatch, "abandoned", "Stopped by the Owner: not achieved.", after)
    text = (ws / "project" / G / "goal.md").read_text()
    assert "status: abandoned" in text and "not achieved" in text
    assert "G-001 stopped unfinished." in (ws / "project" / "project.md").read_text()


def test_a_closing_resume_needs_an_outcome(ws, monkeypatch):
    with pytest.raises(sr.Rejected):
        resume(ws, monkeypatch, "abandoned", "—")
    rec = next((ws / "records").glob("*-resume"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]
    assert any("Outcome" in e for e in errors), errors


def test_deciding_again_after_a_rejected_resume_records_the_answer_once(
    ws, monkeypatch
):
    write(ws, f"{G}/01-game-director-to-owner.md", ESCALATION)
    row = (1, "Decide", "owner", "—", "open", "01-game-director-to-owner.md")
    write(ws, f"{G}/goal.md", goal([row], status="blocked-on-owner"))
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(["nothing", "nothing"], []))
    for _ in range(2):
        with pytest.raises(sr.Rejected):
            sr.do_decide(ws, args(goal="G-001", text="Bで止める。"))
    text = (ws / "project" / G / "01-game-director-to-owner.md").read_text()
    assert text.count("**Owner response") == 1


# --- Recorded live run ---------------------------------------------------------------------

RUN = sr.ROOT / "examples" / "runs" / "p13-boss-run"


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 13 run")
def test_recorded_budget_led_to_a_scope_cut_and_an_owner_stop():
    gdir = sr.goal_dir(RUN / "project", "G-002")
    meta = sr.parse((gdir / "goal.md").read_text())[0]
    assert meta["status"] == "abandoned" and meta["budget"] == "123"
    decisions = {
        p.name[:5]: sr.parse(p.read_text())[0]
        for p in (RUN / "project" / "decisions").glob("D-02[5-7]-*.md")
    }
    assert decisions["D-025"]["decided_by"] == "game-director"  # the scope cut
    assert (
        decisions["D-026"]["decided_by"] == decisions["D-027"]["decided_by"] == "owner"
    )
    fixture = (
        sr.ROOT / "examples" / "runs" / "p12-boss-run" / "project" / "project.md"
    ).read_text()
    closed = (RUN / "project" / "project.md").read_text()
    assert sr.check_project_update(fixture, closed, closing=True) == []
    assert "G-002" in sr.section(closed, "Current state")


@pytest.mark.skipif(
    not (RUN / "measurement.json").is_file(), reason="no recorded Phase 13 run"
)
@pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")
def test_recorded_measurement_reproduces(tmp_path):
    import test_phase6 as t6
    import test_phase10 as t10

    repo = RUN / "project" / "repo"
    code, _, _ = t6.sandboxed_copy(
        repo, tmp_path, "t", ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    recorded = json.loads((RUN / "measurement.json").read_text())
    m = t6.measure(repo, tmp_path)
    assert m == recorded["measurement"] and code == recorded["tests_exit"]
    assert t10.boss_verdict(m) == recorded["boss_verdict"]


def test_over_budget_a_route_may_renumber_planned_rows_around_a_scope_step(
    ws, monkeypatch
):
    scope = (2, "Decide", "game-director", "make-decision", "planned", "—")
    moved = (3, "Verify", "qa", "verify-change", "open", NEXT[0])  # was row 2
    route(ws, monkeypatch, [DONE_ROW, scope, moved], used=31)
    text = (ws / "project" / G / "goal.md").read_text()
    assert "| 2 | Decide | game-director |" in text and "| 3 | Verify | qa |" in text
