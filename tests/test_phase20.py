"""Phase 20: a much larger game from a concept. Studio operations know which Role can run what."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase18 import ember_ws  # noqa: E402
from test_phase2 import sr  # noqa: E402


def test_studio_operations_know_which_role_can_take_screenshots(tmp_path, monkeypatch):
    monkeypatch.setattr(sr, "browser_tools", lambda: (Path("/x/chrome"), Path("/x/nm")))
    project = ember_ws(tmp_path) / "project"
    line = sr.runs_by_role(project)
    assert "qa (tests, play, trace, shot)" in line
    assert (
        "art-director (shot)" in line
        and "gameplay-engineer (tests, trace)" in line
    )
    packet, _ = sr.build_intake(project, "make it")
    assert packet.header["runs_by_role"] == line
    monkeypatch.setattr(sr, "browser_tools", lambda: None)
    assert "shot" not in sr.runs_by_role(project)


def test_a_project_without_a_build_gets_no_runs_line(tmp_path):
    workspace = tmp_path / "ws"
    fixture = (
        Path(__file__).resolve().parent.parent
        / "examples"
        / "fixtures"
        / "lantern-depths"
    )
    sr.main(["init", str(workspace), "--from", str(fixture)])
    assert sr.runs_by_role(workspace / "project") is None


def test_executors_are_told_their_limits_are_their_own():
    text = (sr.STUDIO / "execution.md").read_text()
    assert "not what no step can" in text and "runs_by_role" in text
