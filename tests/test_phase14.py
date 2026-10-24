"""Phase 14: a new Goal budgeted from Intake, run to Close (recorded run only).

Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import sr  # noqa: E402

RUN = sr.ROOT / "examples" / "runs" / "p14-budget-run"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 14 run")
def test_recorded_goal_was_budgeted_at_intake_and_closed():
    gdir = sr.goal_dir(RUN / "project", "G-003")
    meta = sr.parse((gdir / "goal.md").read_text())[0]
    assert meta["status"] == "done" and meta["budget"].isdigit()
    intake = json.loads(
        next((RUN / "records").glob("*-intake/record.json")).read_text()
    )
    written = (
        RUN / "project" / next(p for p in intake["written"] if p.endswith("goal.md"))
    )
    assert "budget:" in written.read_text()  # still the budget Intake wrote
    used = sr.goal_ops(RUN / "records", "G-003")
    assert used <= 2 * int(meta["budget"])  # closed within twice the estimate
    before = (
        sr.ROOT / "examples" / "runs" / "p13-boss-run" / "project" / "project.md"
    ).read_text()
    after = (RUN / "project" / "project.md").read_text()
    assert sr.check_project_update(before, after, closing=True) == []
    assert "G-003" in sr.section(after, "Current state")


@needs_sandbox
@pytest.mark.skipif(
    not (RUN / "measurement.json").is_file(), reason="no recorded Phase 14 run"
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
