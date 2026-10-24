"""Phase 9: the answer's shape at the end of a Step packet; output-format lines kept out of files.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import G, args, block, goal, handoff, sr, write, ws  # noqa: E402,F401
from test_phase3 import runtime, start  # noqa: E402
from test_phase8 import (
    COMBAT,
    DESIGNER,
    DONE,
    designer_step,
    edit,
    errors_of,
)  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")


def answer_shape(packet):
    tail = packet[packet.rindex("\n## Your answer\n") :]
    assert "\n<<<FILE " not in tail  # no input comes after it
    return tail


def test_a_step_packet_ends_with_the_answer_shape(ws, monkeypatch):
    sessions = []
    row = (1, "Design", "game-designer", "write-design-spec", "open", DESIGNER[0])
    start(ws, DESIGNER, [row])
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([DONE], sessions))
    sr.do_step(ws, args(goal="G-001"))
    tail = answer_shape(sessions[0])
    assert f"{G}/02-game-designer-to-<recipient>.md" in tail
    assert ", ".join(sr.REQUIRED["handoff"]) in tail
    assert "the recipient the incoming Handoff's Expected output names" in tail
    assert "<<<EDIT" in tail


def engineer_ws(tmp_path):
    workspace = tmp_path / "ws"
    sr.main(["init", str(workspace), "--from", str(COMBAT)])
    name = "01-studio-to-gameplay-engineer.md"
    row = (1, "Build", "gameplay-engineer", "x", "open", name)
    write(workspace, f"{G}/goal.md", goal([row]))
    loads = ["studio/roles/gameplay-engineer.md", "repo/game.py"]
    write(
        workspace,
        f"{G}/{name}",
        handoff(1, "studio", "gameplay-engineer", "Build", loads),
    )
    return workspace


ENGINEER_DONE = block(
    f"{G}/02-gameplay-engineer-to-studio.md",
    handoff(2, "gameplay-engineer", "studio", "Build", [], outcome="done"),
)


@needs_sandbox
def test_after_a_run_round_the_answer_shape_still_comes_last(tmp_path, monkeypatch):
    workspace = engineer_ws(tmp_path)
    sessions = []
    outputs = [block("@run/tests", ""), ENGINEER_DONE]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_step(workspace, args(goal="G-001"))
    second = sessions[1]
    assert second.index("<<<FILE @run-results") < second.rindex("\n## Your answer\n")
    assert answer_shape(second) == answer_shape(sessions[0])


@pytest.mark.parametrize(
    "answer",
    [
        block("design/combat.md", "intro\n</parameter>\n"),  # a whole file
        edit("design/combat.md", ("intro\n", 'intro\n<parameter name="content">\n')),
        edit("design/combat.md", ("intro\n", "intro\n>>>REPLACE_PLACEHOLDER\n")),
        block("design/new.md", "notes\n</invoke>\n"),  # a new file
    ],
)
def test_output_format_lines_are_kept_out_of_files(ws, monkeypatch, answer):
    write(ws, "design/combat.md", "intro\n")
    with pytest.raises(sr.Rejected):
        designer_step(ws, monkeypatch, DONE + answer)
    assert any("looks like a marker" in e for e in errors_of(ws, "game-designer"))
    assert (ws / "project" / "design" / "combat.md").read_text() == "intro\n"
    assert not (ws / "project" / "design" / "new.md").exists()


def test_a_line_the_file_already_has_may_stay_or_go(ws, monkeypatch):
    write(ws, "design/combat.md", "intro\n</parameter>\nend\n")
    answer = DONE + edit("design/combat.md", ("end\n", "the end\n"))
    designer_step(ws, monkeypatch, answer)
    assert (ws / "project" / "design" / "combat.md").read_text() == (
        "intro\n</parameter>\nthe end\n"
    )
    assert (
        sr.stray_lines(ws / "project", {"design/combat.md": "intro\nthe end\n"}) == []
    )


@needs_sandbox
def test_a_run_round_proposal_with_such_a_line_is_rejected(tmp_path, monkeypatch):
    workspace = engineer_ws(tmp_path)
    speed = "GRUB_HP, GRUB_SPEED, GRUB_REACH = 2, 1.0, 0.6\n"
    proposal = edit("repo/game.py", (speed, speed + "</invoke>\n"))
    monkeypatch.setitem(
        sr.RUNTIMES, "fake", runtime([block("@run/tests", "") + proposal], [])
    )
    with pytest.raises(sr.Rejected):
        sr.do_step(workspace, args(goal="G-001"))
    rec = next((workspace / "records").glob("*-step-gameplay-engineer"))
    assert not list(rec.glob("runs-round*.json"))  # it never reached the sandbox
    errors = json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]
    assert any("looks like a marker" in e for e in errors), errors


RECORDED = ROOT / "examples" / "runs" / "p7-combat-run" / "records"


@pytest.mark.skipif(not RECORDED.is_dir(), reason="no recorded Phase 7 run")
def test_the_recorded_leak_into_a_decision_is_now_rejected(tmp_path):
    text = (RECORDED / "043-step-game-designer" / "output-attempt1.txt").read_text()
    errors = sr.stray_lines(tmp_path, sr.parse_output(text))  # D-007 was a new file
    assert any(e.startswith("decisions/D-007-") and "</parameter>" in e for e in errors)
