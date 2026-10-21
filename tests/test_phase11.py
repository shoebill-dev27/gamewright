"""Phase 11: `partial` is not `question`; the runtime tests the build a Step wrote; TD may run.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import G, args, block, goal, handoff, sr, write, ws  # noqa: E402,F401
from test_phase3 import runtime  # noqa: E402
from test_phase8 import DONE, designer_step, edit  # noqa: E402
from test_phase9 import ENGINEER_DONE, engineer_ws  # noqa: E402

needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")
SPEED = "GRUB_HP, GRUB_SPEED, GRUB_REACH = 2, 1.0, 0.6\n"
FAILING = (
    "import unittest\n\n\nclass Boom(unittest.TestCase):\n"
    "    def test_boom(self):\n        self.fail('boom from the saved build')\n"
)


def engineer_answer(tmp_path, monkeypatch, answer):
    workspace = engineer_ws(tmp_path)
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    sr.do_step(workspace, args(goal="G-001"))
    out = workspace / "project" / G / "02-gameplay-engineer-to-studio.md"
    rec = next((workspace / "records").glob("*-step-gameplay-engineer"))
    return workspace, out.read_text(), rec


@needs_sandbox
def test_the_runtime_tests_the_build_a_step_wrote(tmp_path, monkeypatch):
    change = edit("repo/game.py", (SPEED, SPEED.replace("1.0", "0.9")))
    workspace, text, rec = engineer_answer(
        tmp_path, monkeypatch, ENGINEER_DONE + change
    )
    body = sr.parse(text)[1]
    check = sr.section(body, "Build check")
    assert "exit 0" in check and "python3 -m unittest discover -s tests" in check
    assert text.index("## Build check") < text.index("## Load")
    saved = json.loads((rec / "build-check.json").read_text())
    assert saved["exit"] == 0
    written = json.loads((rec / "record.json").read_text())["written"]
    assert written[f"{G}/02-gameplay-engineer-to-studio.md"] == sr.sha(text)


@needs_sandbox
def test_a_failing_build_is_written_with_the_failure_on_record(tmp_path, monkeypatch):
    answer = ENGINEER_DONE + block("repo/tests/test_boom.py", FAILING)
    workspace, text, _ = engineer_answer(tmp_path, monkeypatch, answer)
    check = sr.section(sr.parse(text)[1], "Build check")
    assert "exit 1" in check and "boom from the saved build" in check
    assert (workspace / "project" / "repo" / "tests" / "test_boom.py").is_file()


@needs_sandbox
def test_a_step_that_writes_no_build_file_gets_no_check(tmp_path, monkeypatch):
    _, text, rec = engineer_answer(tmp_path, monkeypatch, ENGINEER_DONE)
    assert "## Build check" not in text and not (rec / "build-check.json").exists()


def test_a_project_without_run_tests_gets_no_check(ws, monkeypatch):
    designer_step(
        ws, monkeypatch, DONE
    )  # the dry-run fixture declares no build commands
    text = (ws / "project" / G / "02-game-designer-to-studio.md").read_text()
    assert "## Build check" not in text


def test_partial_is_not_counted_as_question():
    opened = {"gameplay-engineer": 2}
    partial = {"gameplay-engineer": ["partial", "partial"]}
    question = {"gameplay-engineer": ["question", "question"]}
    assert sr.no_progress("gameplay-engineer", partial, opened) is None
    assert "question" in sr.no_progress("gameplay-engineer", question, opened)
    assert "4th time" in sr.no_progress(
        "gameplay-engineer", partial, {"gameplay-engineer": 3}
    )


@needs_sandbox
def test_the_technical_director_may_test_and_trace(tmp_path):
    workspace = tmp_path / "ws"
    sr.main(
        [
            "init",
            str(workspace),
            "--from",
            str(sr.ROOT / "examples" / "fixtures" / "lantern-depths-combat"),
        ]
    )
    name = "01-studio-to-technical-director.md"
    write(
        workspace,
        f"{G}/goal.md",
        goal([(1, "Plan", "technical-director", "x", "open", name)]),
    )
    write(
        workspace,
        f"{G}/{name}",
        handoff(
            1,
            "studio",
            "technical-director",
            "Plan",
            ["studio/roles/technical-director.md"],
        ),
    )
    project = workspace / "project"
    packet, _ = sr.build_step(project, project / G, project / G / name)
    assert packet.runs == ["tests", "trace"]


def test_the_answer_shape_says_the_runtime_tests_what_is_written():
    assert "tests the build as you write it" in sr.answer_shape(
        "goals/G/02-x-to-*.md", False, True
    )
    assert "tests the build" not in sr.answer_shape(
        "goals/G/02-x-to-*.md", False, False
    )
