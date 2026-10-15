"""Phase 5: Build runs — Steps run a real build through declared commands in a sandbox.

Deterministic — a fake runtime stands in for executors; build commands really run (bubblewrap).
The oracle below never enters a packet: it judges a build from outside the Studio.
Run with `python3 -m pytest tests/`.
"""

import json
import math
import re
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import args, block, goal, handoff, sr, write  # noqa: E402
from test_phase3 import runtime  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "examples" / "fixtures" / "lantern-depths-real"
RUN = ROOT / "examples" / "runs" / "p5-bug-run"
G = "goals/G-001-test"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")

ENGINEER_LOAD = [
    "studio/roles/gameplay-engineer.md",
    "studio/skills/implement-change.md",
    "design/combat.md",
    "repo/game.py",
]
PLAYTESTER_LOAD = [
    "studio/roles/playtester.md",
    "studio/skills/playtest-session.md",
    "project.md#player-profile",
    "manual.md",
]


@pytest.fixture
def ws(tmp_path):
    workspace = tmp_path / "ws"
    assert sr.main(["init", str(workspace), "--from", str(FIXTURE)]) == 0
    return workspace


def open_step(ws, role, loads):
    first = f"01-studio-to-{role}.md"
    write(ws, f"{G}/goal.md", goal([(1, "Build", role, "x", "open", first)]))
    write(ws, f"{G}/{first}", handoff(1, "studio", role, "Build", loads))


# --- Oracle: the design's damage rules, checked from the player view -----------------------

SCENARIOS = {
    "hit-then-dash": "room empty\nplayer 4 4\nspawn grub 4.5 4\nspawn grub 9.5 4\n0.62 dash right\nend 2\n",
    "dash-in-hurt-window": "room empty\nplayer 4 4\nspawn grub 4.5 4\nspawn grub 8.6 4\n0.35 dash right\nend 2\n",
}
EVENT = re.compile(r"^\s*(\d+\.\d+)\s+(YOU ARE HIT|you dash)", re.M)


def oracle(repo):
    """Rule violations of design/combat.md: no damage during a dash, none within 0.8 s of a hit."""
    problems = []
    for name, script in SCENARIOS.items():
        for fps in (30, 60):
            work = repo.parent / f"oracle-{name}-{fps}"
            shutil.copytree(repo, work)
            (work / "s.txt").write_text(f"fps {fps}\n{script}")
            code, out, _ = sr.sandboxed(
                work, ["python3", "play.py", "--view", "player", "s.txt"]
            )
            shutil.rmtree(work)
            events = [(float(t), kind) for t, kind in EVENT.findall(out)]
            hits = [t for t, kind in events if kind == "YOU ARE HIT"]
            dash_frames = math.ceil(0.25 * fps - 1e-9)
            for d in (t for t, kind in events if kind == "you dash"):
                last = d + (dash_frames - 1) / fps + 1e-3  # the dash's last full frame
                problems += [
                    f"{name}@{fps}: hit at {h} during the dash from {d}"
                    for h in hits
                    if d < h <= last
                ]
            problems += [
                f"{name}@{fps}: hit at {b} only {b - a:.3f} s after the hit at {a}"
                for a, b in zip(hits, hits[1:])
                if b - a < 0.8 - 1e-3
            ]
            if code != 0 or len(hits) < 2:
                problems.append(
                    f"{name}@{fps}: expected two hits and exit 0, got {hits} exit {code}"
                )
    return problems


def fixed(repo):
    """A correct fix: invulnerable while either timer runs."""
    path = repo / "game.py"
    text = path.read_text()
    text = text.replace(
        'self._set_invulnerable(False, "hurt timer ended")',
        'self._set_invulnerable(self.dash_left > 0, "hurt timer ended")',
    ).replace(
        'self._set_invulnerable(False, "dash timer ended")',
        'self._set_invulnerable(self.hurt_left > 0, "dash timer ended")',
    )
    path.write_text(text)


@needs_sandbox
def test_the_build_has_the_reported_defect_and_the_oracle_sees_a_fix(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(FIXTURE / "repo", repo)
    problems = oracle(repo)
    assert any("during the dash" in p for p in problems)
    assert any("after the hit" in p for p in problems)
    fixed(repo)
    assert oracle(repo) == []


@needs_sandbox
def test_the_build_tests_pass_and_the_player_view_hides_internals(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(FIXTURE / "repo", repo)
    code, out, _ = sr.sandboxed(
        repo, ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    assert code == 0 and "OK" in out
    (repo / "s.txt").write_text(SCENARIOS["hit-then-dash"])
    code, out, _ = sr.sandboxed(
        repo, ["python3", "play.py", "--view", "player", "s.txt"]
    )
    assert code == 0 and "YOU ARE HIT" in out
    assert not any(
        word in out for word in ("ZX-", "invulnerable", "hurt_left", "dash_left")
    )


# --- Sandbox -------------------------------------------------------------------------------


@needs_sandbox
def test_sandbox_is_offline_confined_and_time_limited(tmp_path, monkeypatch):
    work = tmp_path / "work"
    work.mkdir()
    (work / "p.py").write_text(
        "import os, socket\n"
        "for target in ('/tmp/x', os.path.expanduser('~/x'), 'inside.txt'):\n"
        "    open(target, 'w').write('x')\n"
        "print('home', os.path.exists('/home'), 'mnt', os.path.exists('/mnt'))\n"
        "socket.create_connection(('1.1.1.1', 80), timeout=3)\n"
    )
    code, out, _ = sr.sandboxed(work, ["python3", "p.py"])
    assert code != 0 and "Network is unreachable" in out
    assert "home False mnt False" in out
    # HOME is /work, so ~/x lands in the build copy; /tmp/x went to a throwaway tmpfs.
    assert sorted(p.name for p in work.iterdir()) == ["inside.txt", "p.py", "x"]
    monkeypatch.setattr(sr, "RUN_TIMEOUT", 1)
    (work / "slow.py").write_text(
        "import time\nprint('start', flush=True)\ntime.sleep(5)\n"
    )
    code, out, _ = sr.sandboxed(work, ["python3", "slow.py"])
    assert code == "timeout" and "stopped after 1 s" in out


def test_without_a_sandbox_nothing_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(sr.shutil, "which", lambda name: None)
    with pytest.raises(RuntimeError, match="never run unsandboxed"):
        sr.sandboxed(tmp_path, ["python3", "-c", "print(1)"])


# --- Run rounds ----------------------------------------------------------------------------


def final_engineer(content):
    return block(
        f"{G}/02-gameplay-engineer-to-studio.md",
        handoff(2, "gameplay-engineer", "studio", "Build", [], outcome="done"),
    ) + block("repo/game.py", content)


@needs_sandbox
def test_engineer_runs_tests_on_a_proposal_then_writes_it(ws, monkeypatch):
    open_step(ws, "gameplay-engineer", ENGINEER_LOAD)
    project = ws / "project"
    proposal = (project / "repo" / "game.py").read_text() + "\n# proposed change\n"
    sessions = []
    outputs = [
        block("@run/tests", "") + block("repo/game.py", proposal),
        final_engineer(proposal),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_step(ws, args(goal="G-001"))
    assert len(sessions) == 2  # a fresh executor after the run
    assert "run_tests: python3 -m unittest" in sessions[0]
    assert (
        "<<<FILE repo/game.py\n" in sessions[0]
    )  # build sources load like any Load entry
    assert "repo/game.py (proposed in a run round; not written)" in sessions[1]
    assert (
        "@run/tests" in sessions[1] and "Exit: 0" in sessions[1] and "OK" in sessions[1]
    )
    assert (
        project / "repo" / "game.py"
    ).read_text() == proposal  # written by the final answer
    rec = next((ws / "records").glob("*-step-gameplay-engineer"))
    assert json.loads((rec / "runs-round1.json").read_text())[0]["exit"] == 0
    assert json.loads((rec / "record.json").read_text())["attempts"][0]["runs"] == [
        "@run/tests"
    ]


@needs_sandbox
def test_a_proposal_is_never_written_unless_the_final_answer_writes_it(ws, monkeypatch):
    open_step(ws, "gameplay-engineer", ENGINEER_LOAD)
    project = ws / "project"
    original = (project / "repo" / "game.py").read_text()
    outputs = [
        block("@run/tests", "") + block("repo/game.py", "broken(\n"),
        block(
            f"{G}/02-gameplay-engineer-to-studio.md",
            handoff(2, "gameplay-engineer", "studio", "Build", [], outcome="question"),
        ),
    ]
    sessions = []
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, sessions))
    sr.do_step(ws, args(goal="G-001"))
    assert "Exit: 1" in sessions[1]  # the broken proposal failed in the sandbox
    assert (project / "repo" / "game.py").read_text() == original


@needs_sandbox
def test_run_rounds_are_limited(ws, monkeypatch):
    open_step(ws, "gameplay-engineer", ENGINEER_LOAD)
    outputs = [block("@run/tests", "")] * (sr.MAX_RUNS + 1)
    sessions = []
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(list(outputs), sessions))
    with pytest.raises(sr.Rejected):
        sr.do_step(ws, args(goal="G-001"))
    assert len(sessions) == sr.MAX_RUNS + 1
    assert "0 rounds left" in sessions[-1] and "@run/<" not in sessions[-1]


@pytest.mark.parametrize(
    "role,loads,answer,why",
    [
        (
            "playtester",
            PLAYTESTER_LOAD,
            block("@run/trace", "0 attack\n"),
            "you may run only play",
        ),
        (
            "playtester",
            PLAYTESTER_LOAD,
            block("@run/play", "") + block("repo/game.py", "x\n"),
            "not a file your Role may write",
        ),
        (
            "qa",
            ["studio/roles/qa.md"],
            block("@run/play", "") + block("repo/game.py", "x\n"),
            "not a file your Role may write",
        ),
        (
            "gameplay-engineer",
            ENGINEER_LOAD,
            block("@run/tests", "") + block("repo/../escape.py", "x\n"),
            "not a file your Role may write",
        ),
        (
            "technical-director",
            ["studio/roles/technical-director.md"],
            block("@run/play", ""),
            "not available here",
        ),
    ],
)
def test_run_requests_follow_the_role_policy(ws, monkeypatch, role, loads, answer, why):
    if role == "playtester":
        write(
            ws,
            f"{G}/goal.md",
            goal([(1, "Play", role, "x", "open", "01-studio-to-playtester.md")]),
        )
        write(
            ws,
            f"{G}/01-studio-to-playtester.md",
            handoff(1, "studio", role, "Play", loads),
        )
    else:
        open_step(ws, role, loads)
    sessions = []
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([answer], sessions))
    with pytest.raises(sr.Rejected):
        sr.do_step(ws, args(goal="G-001"))
    rec = next((ws / "records").glob(f"*-step-{role}"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]
    assert any(why in e for e in errors), errors
    assert not (ws / "project" / "escape.py").exists()


@needs_sandbox
def test_a_run_round_keeps_other_writable_files_for_the_final_answer(ws, monkeypatch):
    open_step(ws, "gameplay-engineer", ENGINEER_LOAD)
    outputs = [block("@run/tests", "") + final_engineer("x\n")]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, []))
    with pytest.raises(sr.Rejected):
        sr.do_step(ws, args(goal="G-001"))
    rec = next((ws / "records").glob("*-step-gameplay-engineer"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]
    assert any("write it in your final answer" in e for e in errors), errors


def test_route_cannot_run_the_build(ws, monkeypatch):
    open_step(ws, "qa", ["studio/roles/qa.md"])
    write(ws, f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Verify", []))
    sessions = []
    monkeypatch.setitem(
        sr.RUNTIMES, "fake", runtime([block("@run/tests", "")], sessions)
    )
    with pytest.raises(sr.Rejected):
        sr.do_route(ws, args(goal="G-001", since=None))
    assert (
        "\nruns:" not in sessions[0].split("## Inputs")[0]
    )  # no build commands offered


def test_dry_run_projects_have_no_build_runs(tmp_path):
    workspace = tmp_path / "ws"
    sr.main(
        [
            "init",
            str(workspace),
            "--from",
            str(ROOT / "examples" / "fixtures" / "lantern-depths"),
        ]
    )
    write(
        workspace,
        f"{G}/goal.md",
        goal(
            [
                (
                    1,
                    "Build",
                    "gameplay-engineer",
                    "x",
                    "open",
                    "01-studio-to-gameplay-engineer.md",
                )
            ]
        ),
    )
    write(
        workspace,
        f"{G}/01-studio-to-gameplay-engineer.md",
        handoff(
            1,
            "studio",
            "gameplay-engineer",
            "Build",
            ["studio/roles/gameplay-engineer.md"],
        ),
    )
    project = workspace / "project"
    packet, _ = sr.build_step(
        project, project / G, project / G / "01-studio-to-gameplay-engineer.md"
    )
    assert not packet.runs and "runs" not in packet.header
    assert not any("@run" in w or "repo/" in w for w in packet.writes)


# --- Recorded live run ---------------------------------------------------------------------


@needs_sandbox
@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 5 run")
def test_recorded_run_fixed_the_build_by_the_oracle(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(RUN / "project" / "repo", repo)
    assert oracle(repo) == []
    code, out, _ = sr.sandboxed(
        repo, ["python3", "-m", "unittest", "discover", "-s", "tests"]
    )
    assert code == 0, out


@needs_sandbox
def test_a_run_cannot_make_the_host_write_through_a_link(ws, monkeypatch, tmp_path):
    open_step(ws, "gameplay-engineer", ENGINEER_LOAD)
    victim = tmp_path / "victim.txt"
    plant = (
        "import os\n"
        "os.remove('/work/input.script')\n"
        f"os.symlink({str(victim)!r}, '/work/input.script')\n"
    )
    outputs = [
        block("@run/tests", "")
        + block("@run/trace/next", "end 1\n")
        + block("repo/tests/test_link.py", plant),
        final_engineer((ws / "project" / "repo" / "game.py").read_text()),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, []))
    sr.do_step(ws, args(goal="G-001"))
    assert (
        not victim.exists()
    )  # the second run's script went to a fresh copy, not the link
