"""Phase 15: a Role that writes the build always sees the names of the build's files.

Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import G, goal, handoff, sr, write  # noqa: E402

COMBAT = sr.ROOT / "examples" / "fixtures" / "lantern-depths-combat"
RUN = sr.ROOT / "examples" / "runs" / "p15-budget-check-run"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")


def step_packet(tmp_path, role, loads):
    workspace = tmp_path / "ws"
    sr.main(["init", str(workspace), "--from", str(COMBAT)])
    name = f"01-studio-to-{role}.md"
    write(workspace, f"{G}/goal.md", goal([(1, "Build", role, "x", "open", name)]))
    write(workspace, f"{G}/{name}", handoff(1, "studio", role, "Build", loads))
    project = workspace / "project"
    return sr.build_step(project, project / G, project / G / name)[0].render()


def test_the_engineer_sees_the_build_files_without_a_build_entry(tmp_path):
    packet = step_packet(
        tmp_path, "gameplay-engineer", ["studio/roles/gameplay-engineer.md"]
    )
    listing = packet[packet.index("<<<FILE @files/repo\n") :]
    assert "- repo/game.py\n" in listing
    assert packet.count("<<<FILE @files/repo\n") == 1


def test_a_build_named_in_load_is_listed_once(tmp_path):
    loads = ["studio/roles/gameplay-engineer.md", "the build in repo/"]
    packet = step_packet(tmp_path, "gameplay-engineer", loads)
    assert packet.count("<<<FILE @files/repo\n") == 1


def test_a_role_that_does_not_write_the_build_gets_no_listing_unasked(tmp_path):
    packet = step_packet(tmp_path, "game-designer", ["studio/roles/game-designer.md"])
    assert "@files/repo" not in packet


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 15 run")
def test_recorded_goal_closed_near_its_intake_budget():
    gdir = sr.goal_dir(RUN / "project", "G-003")
    meta = sr.parse((gdir / "goal.md").read_text())[0]
    used, budget = sr.goal_ops(RUN / "records", "G-003"), int(meta["budget"])
    assert meta["status"] == "done" and abs(used - budget) <= budget // 4
    runs = sr.ROOT / "examples" / "runs"
    before = (runs / "p13-boss-run" / "project" / "project.md").read_text()
    after = (RUN / "project" / "project.md").read_text()
    assert sr.check_project_update(before, after, closing=True) == []


@needs_sandbox
@pytest.mark.skipif(
    not (RUN / "measurement.json").is_file(), reason="no recorded Phase 15 run"
)
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
