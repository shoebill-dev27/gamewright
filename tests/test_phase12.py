"""Phase 12: a Load entry naming a directory is rejected; Steps may ask once for more files.

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
from test_phase8 import DESIGNER, DONE  # noqa: E402
from test_phase9 import ENGINEER_DONE, engineer_ws  # noqa: E402

needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")
QA_DONE = block(f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Next", []))


def qa_handoff(ws, extra_load):
    return handoff(1, "studio", "qa", "Observe", QA_LOAD + [extra_load])


def test_a_directory_in_load_brings_the_names_of_its_files(ws, monkeypatch):
    loads = QA_LOAD + [
        "Project: the design in design/ (see below)",
        "Notes: rules and/or tuning",
    ]
    first = ("01-studio-to-qa.md", handoff(1, "studio", "qa", "Observe", loads))
    row = (1, "Observe", "qa", "reproduce-defect", "open", first[0])
    sessions = step(ws, monkeypatch, first, row, [QA_DONE])
    listing = sessions[0][sessions[0].index("<<<FILE @files/design") :]
    assert (
        "- design/combat.md\n" in listing
        and "ask for the ones you need with @need" in listing
    )
    assert "@files/and" not in sessions[0]


def test_a_listing_shows_only_what_the_role_may_load(ws):
    text = handoff(1, "studio", "playtester", "Play", ["the design in design/"])
    assert sr.directory_listings(ws / "project", text, "playtester") == []
    assert sr.directory_listings(ws / "project", text, "qa") != []


def step(ws, monkeypatch, first, row, outputs):
    start(ws, first, [row])
    sessions = []
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_step(ws, args(goal="G-001"))
    return sessions


def test_a_step_may_ask_once_for_more_files(ws, monkeypatch):
    row = (1, "Design", "game-designer", "write-design-spec", "open", DESIGNER[0])
    sessions = step(
        ws, monkeypatch, DESIGNER, row, [block("@need", "project.md\n"), DONE]
    )
    assert (
        "<<<FILE project.md\n" not in sessions[0]
        and "<<<FILE project.md\n" in sessions[1]
    )
    assert "context_request: used" in sessions[1]


def test_a_second_request_is_rejected(ws, monkeypatch):
    row = (1, "Design", "game-designer", "write-design-spec", "open", DESIGNER[0])
    need = block("@need", "project.md\n")
    with pytest.raises(sr.Rejected):
        step(ws, monkeypatch, DESIGNER, row, [need, need])
    rec = next((ws / "records").glob("*-step-game-designer"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][1]["errors"]
    assert any("only once" in e for e in errors), errors


def test_a_request_follows_the_recipient_policy(ws):
    errors = sr.check_need(ws / "project", ["design/combat.md"], role="playtester")
    assert any("playtester may not load design/combat.md" in e for e in errors), errors
    assert sr.check_need(ws / "project", ["design/combat.md"], role="qa") == []


def test_a_requested_handoff_loses_what_the_role_must_not_see(ws, monkeypatch):
    engineer = f"{G}/05-gameplay-engineer-to-studio.md"
    write(
        ws,
        engineer,
        handoff(
            5,
            "gameplay-engineer",
            "studio",
            "Build",
            [],
            extra="## Sender assessment\n\nZZ-SELF\n\n",
        ),
    )
    row = (1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])
    sessions = step(
        ws,
        monkeypatch,
        QA_OPEN,
        row,
        [
            block("@need", engineer + "\n"),
            block(f"{G}/06-qa-to-studio.md", handoff(6, "qa", "studio", "Next", [])),
        ],
    )
    assert f"<<<FILE {engineer}" in sessions[1] and "ZZ-SELF" not in sessions[1]


@needs_sandbox
def test_files_asked_for_after_a_run_round_stay_for_the_next(tmp_path, monkeypatch):
    workspace = engineer_ws(tmp_path)
    sessions = []
    outputs = [
        block("@run/tests", ""),
        block("@need", "design/combat.md\n"),
        block("@run/tests", ""),
        ENGINEER_DONE,
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_step(workspace, args(goal="G-001"))
    assert "<<<FILE design/combat.md\n" in sessions[3]


def test_asking_for_a_directory_names_its_files(ws):
    errors = sr.check_need(ws / "project", ["design/"])
    assert any(
        "is a directory" in e and "design/combat.md" in e for e in errors
    ), errors


# --- Recorded live runs --------------------------------------------------------------------

RUNS = sr.ROOT / "examples" / "runs"
BOSS, CLOSE = RUNS / "p12-boss-run", RUNS / "p12-close-run"


@needs_sandbox
@pytest.mark.skipif(
    not (BOSS / "measurement.json").is_file(), reason="no recorded Phase 12 run"
)
def test_recorded_measurement_reproduces(tmp_path):
    import test_phase6 as t6
    import test_phase10 as t10

    repo = BOSS / "project" / "repo"
    code, _, _ = t6.sandboxed_copy(
        repo, tmp_path, "t", ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    recorded = json.loads((BOSS / "measurement.json").read_text())
    m = t6.measure(repo, tmp_path)
    assert m == recorded["measurement"] and code == recorded["tests_exit"]
    assert t10.boss_verdict(m) == recorded["boss_verdict"]


@pytest.mark.skipif(not CLOSE.is_dir(), reason="no recorded Phase 12 close run")
def test_recorded_close_refreshed_only_the_current_state():
    goal_md = next((CLOSE / "project" / "goals").glob("G-001-*/goal.md")).read_text()
    assert sr.parse(goal_md)[0]["status"] == "done"
    fixture = (
        sr.ROOT / "examples" / "fixtures" / "lantern-depths-real" / "project.md"
    ).read_text()
    closed = (CLOSE / "project" / "project.md").read_text()
    assert sr.section(closed, "Current state") != sr.section(fixture, "Current state")
    assert sr.check_project_update(fixture, closed, closing=True) == []


@pytest.mark.skipif(not CLOSE.is_dir(), reason="no recorded Phase 12 close run")
def test_recorded_failing_build_check_was_sent_back():
    checks = sorted(
        (CLOSE / "records").glob("*-step-gameplay-engineer/build-check.json")
    )
    exits = [json.loads(c.read_text())["exit"] for c in checks]
    assert exits[0] != 0 and exits[-1] == 0  # the failure went back and was fixed
