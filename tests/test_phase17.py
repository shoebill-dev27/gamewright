"""Phase 17: a larger game with a browser page, built from a concept (recorded run only).

Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import sr  # noqa: E402

RUN = sr.ROOT / "examples" / "runs" / "p17-ember-run"
FIXTURE = sr.ROOT / "examples" / "fixtures" / "ember-hollow"
needs_node = pytest.mark.skipif(
    not (shutil.which("bwrap") and shutil.which("node")), reason="no bubblewrap or node"
)


def test_the_fixture_is_a_concept_without_a_build():
    assert [p.name for p in (FIXTURE / "repo").iterdir()] == ["README.md"]
    meta = sr.project_meta(FIXTURE)
    assert meta["run_tests"] == "node --test" and meta["build"] == "repo"


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 17 run")
def test_recorded_goal_closed_within_its_budget():
    gdir = sr.goal_dir(RUN / "project", "G-001")
    meta = sr.parse((gdir / "goal.md").read_text())[0]
    assert meta["status"] == "done"
    assert sr.goal_ops(RUN / "records", "G-001") <= int(meta["budget"])
    before = (FIXTURE / "project.md").read_text()
    after = (RUN / "project" / "project.md").read_text()
    assert sr.check_project_update(before, after, closing=True) == []


@needs_node
@pytest.mark.skipif(
    not (RUN / "held-out.json").is_file(), reason="no recorded Phase 17 run"
)
def test_recorded_win_and_loss_replay_through_play_js(tmp_path):
    work = tmp_path / "w"
    shutil.copytree(RUN / "project" / "repo", work)
    code, out, _ = sr.sandboxed(work, ["node", "--test"])
    assert code == 0, out
    v5 = json.loads((RUN / "held-out.json").read_text())["V5_win_and_loss"]
    for case, result in (("win", "Result: Victory"), ("loss", "Result: Ember out")):
        (work / "s.txt").write_text(
            f"seed {v5[case]['seed']}\n{v5[case]['commands']}\n"
        )
        code, out, _ = sr.sandboxed(work, ["node", "play.js", "s.txt"])
        assert code == 0 and result in out, case
