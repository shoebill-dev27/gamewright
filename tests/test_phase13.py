"""Phase 13: a Goal's operation budget — set at Intake, shown to Routes, and no new stages past it.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import json
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
