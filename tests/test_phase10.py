"""Phase 10: Close keeps project.md's Current state up to date; the oracle also measures new rooms.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import G, args, block, goal, handoff, sr, write, ws  # noqa: E402,F401
from test_phase3 import QA_LOAD, QA_OPEN, runtime, start  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COMBAT = ROOT / "examples" / "fixtures" / "lantern-depths-combat"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")
DONE_ROW = (1, "Observe", "qa", "reproduce-defect", "done", QA_OPEN[0])
NEXT = ("03-studio-to-qa.md", handoff(3, "studio", "qa", "Verify", QA_LOAD))


def route(ws, monkeypatch, project_text, close=True):
    start(ws, QA_OPEN, [(*DONE_ROW[:4], "open", QA_OPEN[0])])
    write(ws, f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Observe", []))
    if close:
        answer = block(f"{G}/goal.md", goal([DONE_ROW], status="done"))
    else:
        rows = [DONE_ROW, (2, "Verify", "qa", "verify-change", "open", NEXT[0])]
        answer = block(f"{G}/goal.md", goal(rows)) + block(f"{G}/{NEXT[0]}", NEXT[1])
    answer += block("project.md", project_text)
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    sr.do_route(ws, args(goal="G-001", since=1))


def project_with_text(text, current_state):
    return text.replace(sr.section(text, "Current state").strip(), current_state)


def route_errors(ws):
    rec = next((ws / "records").glob("*-route"))
    return json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]


def test_close_updates_the_current_state(ws, monkeypatch):
    before = (ws / "project" / "project.md").read_text()
    new = project_with_text(
        before, "Build 0.5: 6 rooms, a boss in room 6, 3 enemy types."
    )
    route(ws, monkeypatch, new)
    assert (ws / "project" / "project.md").read_text() == new


@pytest.mark.parametrize(
    "change,close,why",
    [
        (lambda t: project_with_text(t, "Build 0.5."), False, "only at Close"),
        (lambda t: t.replace("One-button combat", "Two-button combat"), True, "Vision"),
        (
            lambda t: t.replace("owner_language: ja", "owner_language: en"),
            True,
            "frontmatter",
        ),
        (lambda t: project_with_text(t, "x" * 1501), True, "1,500"),
    ],
)
def test_other_project_changes_are_rejected(ws, monkeypatch, change, close, why):
    before = (ws / "project" / "project.md").read_text()
    with pytest.raises(sr.Rejected):
        route(ws, monkeypatch, change(before), close=close)
    assert any(why in e for e in route_errors(ws)), route_errors(ws)
    assert (ws / "project" / "project.md").read_text() == before


@needs_sandbox
def test_the_oracle_measures_new_rooms_and_only_them(tmp_path):
    import test_phase6 as t6

    repo = tmp_path / "repo"
    shutil.copytree(COMBAT / "repo", repo)
    with open(repo / "game.py", "a") as f:
        f.write('\nROOMS["boss"] = ROOMS["5"]\nROOMS["boss-practice"] = ROOMS["1"]\n')
    m = t6.measure(repo, tmp_path)
    assert m["rooms"] == ["1", "2", "3", "4", "5"] and m["extra_rooms"] == ["boss"]
    for fps, bots in m["extra"].items():
        assert [r["room"] for r in bots["simple"]] == ["boss"]
        assert m["fps"][fps]["simple"][4] == {**bots["simple"][0], "room": "5"}
    plain = t6.measure(COMBAT / "repo", tmp_path / "plain")
    assert "extra_rooms" not in plain  # older builds measure exactly as before
