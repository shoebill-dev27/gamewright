"""Phase 16: a first playable built from a concept alone (recorded run only).

Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import sr  # noqa: E402

RUN = sr.ROOT / "examples" / "runs" / "p16-lamplight-run"
FIXTURE = sr.ROOT / "examples" / "fixtures" / "lamplight-keeper"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")


def test_the_fixture_is_a_concept_without_a_build():
    assert [p.name for p in (FIXTURE / "repo").iterdir()] == ["README.md"]
    assert not (FIXTURE / "design").exists() and not (FIXTURE / "decisions").exists()


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 16 run")
def test_recorded_goal_closed_with_only_the_current_state_refreshed():
    gdir = sr.goal_dir(RUN / "project", "G-001")
    meta = sr.parse((gdir / "goal.md").read_text())[0]
    assert meta["status"] == "done" and meta["budget"].isdigit()
    before = (FIXTURE / "project.md").read_text()
    after = (RUN / "project" / "project.md").read_text()
    assert sr.check_project_update(before, after, closing=True) == []
    assert "Concept only" not in sr.section(after, "Current state")


@needs_sandbox
@pytest.mark.skipif(
    not (RUN / "held-out.json").is_file(), reason="no recorded Phase 16 run"
)
def test_recorded_wins_and_losses_replay(tmp_path):
    work = tmp_path / "w"
    shutil.copytree(RUN / "project" / "repo", work)
    code, out, _ = sr.sandboxed(
        work, ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    assert code == 0, out
    nights = json.loads((RUN / "held-out.json").read_text())["N3_choices_matter"]
    for night, seqs in nights.items():
        for seq, verdict in ((seqs["win"], "NIGHT WON"), (seqs["loss"], "NIGHT LOST")):
            (work / "s.txt").write_text(f"night {night}\n{seq}\n")
            code, out, _ = sr.sandboxed(work, ["python3", "play.py", "s.txt"])
            assert code == 0 and verdict in out, (night, seq)
