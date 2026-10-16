"""Phase 8: EDIT blocks (SEARCH/REPLACE) instead of rewriting whole files; output cut keeps the end.

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
DESIGNER = (
    "01-studio-to-game-designer.md",
    handoff(
        1,
        "studio",
        "game-designer",
        "Design",
        ["studio/roles/game-designer.md", "design/combat.md"],
    ),
)
DONE = block(
    f"{G}/02-game-designer-to-studio.md",
    handoff(2, "game-designer", "studio", "Design", [], outcome="done"),
)
RECOVERY = "- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.\n"


def edit(path, *pairs):
    body = "".join(
        f"<<<<<<< SEARCH\n{s}=======\n{r}>>>>>>> REPLACE\n" for s, r in pairs
    )
    return f"<<<EDIT {path}\n{body}>>>END\n"


def designer_step(ws, monkeypatch, answer):
    row = (1, "Design", "game-designer", "write-design-spec", "open", DESIGNER[0])
    start(ws, DESIGNER, [row])
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    sr.do_step(ws, args(goal="G-001"))


def errors_of(ws, role):
    rec = next((ws / "records").glob(f"*-step-{role}"))
    return json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]


def test_edits_change_only_what_they_name(ws, monkeypatch):
    path = ws / "project" / "design" / "combat.md"
    before = path.read_text()
    answer = DONE + edit(
        "design/combat.md",
        (RECOVERY, RECOVERY.replace("0.35", "0.30")),
        ("## Rooms\n", "## Rooms (draft)\n"),
    )
    designer_step(ws, monkeypatch, answer)
    after = path.read_text()
    expected = before.replace("0.35 s recovery", "0.30 s recovery").replace(
        "## Rooms\n", "## Rooms (draft)\n"
    )
    assert after == expected
    rec = next((ws / "records").glob("*-step-game-designer"))
    written = json.loads((rec / "record.json").read_text())["written"]
    assert written["design/combat.md"] == sr.sha(after)


@pytest.mark.parametrize(
    "answer,why",
    [
        (edit("design/combat.md", ("no such line\n", "x\n")), "occurs 0 times"),
        (edit("design/combat.md", ("same\n", "x\n")), "occurs 2 times"),
        (edit("design/combat.md", ("   \n", "x\n")), "is empty"),
        (edit("design/new.md", ("a\n", "b\n")), "write a new file as a whole"),
        (
            block("design/combat.md", "whole\n")
            + edit("design/combat.md", ("intro\n", "x\n")),
            "not both",
        ),
        (edit("design/combat.md"), "needs <<<<<<< SEARCH"),
        (
            edit("design/combat.md", ("intro\n", "x\n"), ("middle", "y")),
            "on a line of its own",
        ),  # one good pair and one whose marker follows the text: nothing may be dropped silently
        (
            edit("design/combat.md", ("intro\n", "x\n>>>REPLACE\n")),
            "looks like a marker",
        ),  # a misspelt closing marker read as the forgotten one: it must not land in the file
    ],
)
def test_bad_edits_are_rejected_and_say_how_to_fix_them(ws, monkeypatch, answer, why):
    write(ws, "design/combat.md", "intro\nsame\nmiddle\nsame\n")
    before = (ws / "project" / "design" / "combat.md").read_text()
    with pytest.raises(sr.Rejected):
        designer_step(ws, monkeypatch, DONE + answer)
    errors = errors_of(ws, "game-designer")
    assert any(why in e for e in errors), errors
    assert (ws / "project" / "design" / "combat.md").read_text() == before


def test_several_edit_blocks_for_one_file_apply_in_order(ws, monkeypatch):
    path = ws / "project" / "design" / "combat.md"
    before = path.read_text()
    answer = (
        DONE
        + edit("design/combat.md", (RECOVERY, RECOVERY.replace("0.35", "0.30")))
        + edit("design/combat.md", ("## Rooms\n", "## Rooms (draft)\n"))
    )
    designer_step(ws, monkeypatch, answer)
    assert path.read_text() == before.replace(
        "0.35 s recovery", "0.30 s recovery"
    ).replace("## Rooms\n", "## Rooms (draft)\n")


def test_common_slips_are_read_as_meant(ws, monkeypatch):
    path = ws / "project" / "design" / "combat.md"
    before = path.read_text()
    partial = "- **Attack** (one button): a short swipe"  # the start of a line
    answer = (
        DONE
        + f"<<<FILE design/combat.md\n"  # wrapped in a FILE block
        + "<<<EDIT design/combat.md\n<<<<<<< SEARCH\n"
        + partial
        + "\n=======\n- **Attack** (one button): a quick swipe\n>>>END\n"  # no REPLACE marker
    )
    designer_step(ws, monkeypatch, answer)
    assert path.read_text() == before.replace("a short swipe", "a quick swipe")


def test_a_new_edit_block_ends_one_left_open(ws, monkeypatch):
    path = ws / "project" / "design" / "combat.md"
    write(ws, "design/notes.md", "alpha\n")
    before = path.read_text()
    first = edit("design/combat.md", ("## Rooms\n", "## Rooms (draft)\n"))
    answer = (
        DONE
        + first.replace(">>>END\n", "")  # no >>>END before the next block
        + edit("design/notes.md", ("alpha\n", "beta\n"))
    )
    designer_step(ws, monkeypatch, answer)
    assert path.read_text() == before.replace("## Rooms\n", "## Rooms (draft)\n")
    assert (ws / "project" / "design" / "notes.md").read_text() == "beta\n"


def test_an_edit_is_checked_against_the_write_list(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    answer = block(
        f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Next", [])
    ) + edit("design/combat.md", ("## Rooms\n", "## Rooms (draft)\n"))
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    with pytest.raises(sr.Rejected):
        sr.do_step(ws, args(goal="G-001"))
    assert any("not on the write list" in e for e in errors_of(ws, "qa"))


def test_a_route_may_edit_goal_md(ws, monkeypatch):
    start(ws, QA_OPEN, [(1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])])
    write(ws, f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Next", []))
    row = "| 1 | Observe | qa | reproduce-defect | open | 01-studio-to-qa.md |\n"
    answer = edit(
        f"{G}/goal.md",
        ("status: active\n", "status: done\n"),
        (row, row.replace("| open |", "| done |")),
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    sr.do_route(ws, args(goal="G-001", since=1))
    text = (ws / "project" / G / "goal.md").read_text()
    assert "status: done" in text and "| done | 01-studio-to-qa.md |" in text


def test_handoff_numbers_go_past_99(ws, monkeypatch):
    first = ("98-studio-to-qa.md", handoff(98, "studio", "qa", "Observe", QA_LOAD))
    start(ws, first, [(1, "Observe", "qa", "reproduce-defect", "open", first[0])])
    write(ws, f"{G}/99-qa-to-studio.md", handoff(99, "qa", "studio", "Observe", []))
    rows = [
        (1, "Observe", "qa", "reproduce-defect", "done", first[0]),
        (2, "Verify", "qa", "verify-build", "open", "100-studio-to-qa.md"),
    ]
    answer = block(f"{G}/goal.md", goal(rows)) + block(
        f"{G}/100-studio-to-qa.md", handoff(100, "studio", "qa", "Verify", QA_LOAD)
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], []))
    sr.do_route(ws, args(goal="G-001", since=98))
    gdir = ws / "project" / G
    assert [sr.seq_of(p) for p, _ in sr.goal_artifacts(gdir)] == [98, 99, 100]
    assert sr.next_seq(gdir) == 101
    assert [p.name for p, _ in sr.unseen(gdir, 99)] == ["100-studio-to-qa.md"]


@needs_sandbox
def test_edits_in_run_rounds_and_final_answers_apply_to_the_project_file(
    tmp_path, monkeypatch
):
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
    speed = "GRUB_HP, GRUB_SPEED, GRUB_REACH = 2, 1.0, 0.6\n"
    shot = "SHOT_SPEED, SHOT_REACH = 1.6, 0.4\n"
    first = edit("repo/game.py", (speed, speed.replace("1.0", "0.9")))
    both = edit(
        "repo/game.py",
        (speed, speed.replace("1.0", "0.9")),
        (shot, shot.replace("1.6", "1.5")),
    )
    final = block(
        f"{G}/02-gameplay-engineer-to-studio.md",
        handoff(2, "gameplay-engineer", "studio", "Build", [], outcome="done"),
    )
    sessions = []
    outputs = [
        block("@run/tests", "") + first,
        final + both,
    ]  # the final answer carries every change
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_step(workspace, args(goal="G-001"))
    assert (
        "GRUB_SPEED, GRUB_REACH = 2, 0.9" in sessions[1]
    )  # the proposal is in the next packet
    built = (workspace / "project" / "repo" / "game.py").read_text()
    assert "GRUB_SPEED, GRUB_REACH = 2, 0.9" in built and "SHOT_REACH = 1.5" in built


@needs_sandbox
def test_a_long_output_keeps_its_end(tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    (work / "p.py").write_text("print('x' * 30000)\nprint('THE END')\n")
    code, out, _ = sr.sandboxed(work, ["python3", "p.py"])
    assert code == 0 and out.rstrip().endswith("THE END") and "characters cut" in out
    assert len(out) < sr.RUN_OUTPUT_MAX + 100


@needs_sandbox
def test_an_edit_against_a_proposal_is_rejected_with_the_rule(tmp_path, monkeypatch):
    workspace = tmp_path / "ws"
    sr.main(["init", str(workspace), "--from", str(COMBAT)])
    name = "01-studio-to-gameplay-engineer.md"
    write(
        workspace,
        f"{G}/goal.md",
        goal([(1, "Build", "gameplay-engineer", "x", "open", name)]),
    )
    loads = ["studio/roles/gameplay-engineer.md", "repo/game.py"]
    write(
        workspace,
        f"{G}/{name}",
        handoff(1, "studio", "gameplay-engineer", "Build", loads),
    )
    speed = "GRUB_HP, GRUB_SPEED, GRUB_REACH = 2, 1.0, 0.6\n"
    proposed = speed.replace("1.0", "0.9")
    final = block(
        f"{G}/02-gameplay-engineer-to-studio.md",
        handoff(2, "gameplay-engineer", "studio", "Build", [], outcome="done"),
    )
    outputs = [
        block("@run/tests", "") + edit("repo/game.py", (speed, proposed)),
        final + edit("repo/game.py", (proposed, proposed.replace("0.9", "0.8"))),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, []))
    with pytest.raises(sr.Rejected):
        sr.do_step(workspace, args(goal="G-001"))
    rec = next((workspace / "records").glob("*-step-gameplay-engineer"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][1]["errors"]
    assert any("not from a run-round proposal" in e for e in errors), errors
