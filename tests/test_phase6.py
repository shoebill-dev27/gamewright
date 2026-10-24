"""Phase 6: an experience Goal on the playable build, measured from outside the Studio.

The held-out bots (`oracle_bots.py`) and the success criteria below never enter a packet. They
were fixed before the live run (docs/phase6.md §3.3). Run with `python3 -m pytest tests/`.
"""

import json
import re
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import goal, handoff, sr, write  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "examples" / "fixtures" / "lantern-depths-combat"
RUN = ROOT / "examples" / "runs" / "p6-combat-run"
ORACLE = Path(__file__).resolve().parent / "oracle_bots.py"
G = "goals/G-001-test"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")


def sandboxed_copy(repo, tmp_path, name, argv, extra=None):
    work = tmp_path / name
    shutil.copytree(repo, work)
    for path in extra or []:
        shutil.copy(path, work / path.name)
    return sr.sandboxed(work, argv)


def measure(repo, tmp_path):
    code, out, _ = sandboxed_copy(
        repo, tmp_path, "measure", ["python3", "oracle_bots.py"], [ORACLE]
    )
    assert code == 0, out
    return json.loads(out.strip().splitlines()[-1])


def totals(rows):
    return sum(r["cleared"] for r in rows), sum(r["lost"] for r in rows)


def verdict(measurement, tests_pass, decisions):
    """The success criteria S1-S3, fixed before the run; each must hold at 30 and 60 FPS."""
    s1 = s2 = True
    for bots in measurement["fps"].values():
        simple, skilled = bots["simple"], bots["skilled"]
        punished = sum(1 for r in simple if not r["cleared"] or r["lost"] >= 2)
        s1 = s1 and punished >= 2
        cleared, lost = totals(skilled)
        s2 = s2 and cleared >= 4 and totals(simple)[1] - lost >= 3
    approved = any(
        re.search(r"^supersedes:.*D-001", d.read_text(), re.M)
        and re.search(r"^decided_by: owner", d.read_text(), re.M)
        for d in decisions.glob("D-*.md")
    )
    s3 = tests_pass and (not measurement["new_inputs"] or approved)
    return {"S1": s1, "S2": s2, "S3": s3}


@needs_sandbox
def test_the_starting_build_is_monotone(tmp_path):
    m = measure(FIXTURE / "repo", tmp_path)
    assert m["rooms"] == ["1", "2", "3", "4", "5"] and m["new_inputs"] == []
    for fps, bots in m["fps"].items():
        simple, skilled = totals(bots["simple"]), totals(bots["skilled"])
        assert simple[0] == 5 and simple[1] <= 2, (
            fps,
            simple,
        )  # the simple pattern wins everywhere
        assert skilled[1] >= simple[1] - 1, (
            fps,
            simple,
            skilled,
        )  # and dashing does not pay
    assert verdict(m, True, FIXTURE / "decisions") == {
        "S1": False,
        "S2": False,
        "S3": True,
    }


@needs_sandbox
def test_the_starting_build_runs_its_tests_and_bots(tmp_path):
    repo = FIXTURE / "repo"
    code, out, _ = sandboxed_copy(
        repo, tmp_path, "t", ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    assert code == 0 and "OK" in out, out
    script = tmp_path / "bots.txt"
    script.write_text("bots walker,dodger\nrooms 1-2\nfps 30\n")
    code, out, _ = sandboxed_copy(
        repo, tmp_path, "b", ["python3", "bots.py", "bots.txt"], [script]
    )
    assert (
        code == 0
        and "walker  total: cleared" in out
        and "dodger  total: cleared" in out
    ), out


def test_designer_and_director_may_play_and_run_bots_the_playtester_only_plays(
    tmp_path,
):
    workspace = tmp_path / "ws"
    sr.main(["init", str(workspace), "--from", str(FIXTURE)])
    project = workspace / "project"
    for role, runs in [
        ("game-designer", ["play", "bots"]),
        ("game-director", ["play", "bots"]),
        ("qa", ["tests", "play", "trace", "bots"]),
        ("gameplay-engineer", ["tests", "trace", "bots"]),
        ("playtester", ["play"]),
    ]:
        name = f"01-studio-to-{role}.md"
        write(workspace, f"{G}/goal.md", goal([(1, "Play", role, "x", "open", name)]))
        write(
            workspace,
            f"{G}/{name}",
            handoff(1, "studio", role, "Play", [f"studio/roles/{role}.md"]),
        )
        packet, _ = sr.build_step(project, project / G, project / G / name)
        assert packet.runs == runs, role
        (project / G / name).unlink()


# --- Recorded live run ---------------------------------------------------------------------


@needs_sandbox
@pytest.mark.skipif(
    not (RUN / "measurement.json").is_file(), reason="no recorded Phase 6 run"
)
def test_recorded_measurement_reproduces(tmp_path):
    repo = RUN / "project" / "repo"
    code, out, _ = sandboxed_copy(
        repo, tmp_path, "t", ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    recorded = json.loads((RUN / "measurement.json").read_text())
    m = measure(repo, tmp_path)
    assert m == recorded["measurement"]
    assert verdict(m, code == 0, RUN / "project" / "decisions") == recorded["verdict"]


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 6 run")
def test_recorded_playtesters_saw_only_the_player_view():
    steps = sorted((RUN / "records").glob("*-step-playtester"))
    assert steps, "the run had no Playtester step"
    for rec in steps:
        labels = [m["path"] for m in json.loads((rec / "manifest.json").read_text())]
        assert not any(
            label.startswith(("repo/", "design/", "decisions/")) for label in labels
        ), rec
        packets = [p.read_text() for p in rec.glob("packet*.md")]
        assert not any("ZX-" in p for p in packets), rec
        for result in rec.glob("runs-round*.json"):
            assert all(
                r["run"].startswith("@run/play") for r in json.loads(result.read_text())
            ), rec
