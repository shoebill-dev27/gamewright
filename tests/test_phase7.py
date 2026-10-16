"""Phase 7: reactive play for Playtesters, the manual inside the build, Owner questions surfaced.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import G, args, block, goal, handoff, sr, write, ws  # noqa: E402,F401
from test_phase3 import ESCALATION, runtime, start, summary  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COMBAT = ROOT / "examples" / "fixtures" / "lantern-depths-combat"
needs_sandbox = pytest.mark.skipif(not shutil.which("bwrap"), reason="no bubblewrap")
DIRECTOR = (
    "01-studio-to-game-director.md",
    handoff(1, "studio", "game-director", "Decide", ["studio/roles/game-director.md"]),
)
DIRECTOR_ROW = (1, "Decide", "game-director", "make-decision", "open", DIRECTOR[0])
STUDIO_ESCALATION = (
    ESCALATION.replace("seq: 2", "seq: 3")
    .replace("from: game-director", "from: studio")
    .replace("# 02:", "# 03:")
)


def test_run_reports_an_owner_question_opened_while_other_steps_go_on(
    ws, monkeypatch, capsys
):
    start(ws, DIRECTOR, [DIRECTOR_ROW])
    designer = (
        "04-studio-to-game-designer.md",
        handoff(
            4, "studio", "game-designer", "Design", ["studio/roles/game-designer.md"]
        ),
    )
    owner_row = (2, "Decide", "owner", "—", "open", "03-studio-to-owner.md")
    meanwhile = [
        (*DIRECTOR_ROW[:4], "done", DIRECTOR[0]),
        owner_row,
        (3, "Design", "game-designer", "write-design-spec", "open", designer[0]),
    ]
    waiting = [meanwhile[0], owner_row, (*meanwhile[2][:4], "done", designer[0])]
    outputs = [
        block(
            f"{G}/02-game-director-to-studio.md",
            handoff(2, "game-director", "studio", "Decide", []),
        ),
        block(f"{G}/goal.md", goal(meanwhile))
        + block(f"{G}/03-studio-to-owner.md", STUDIO_ESCALATION)
        + block(f"{G}/{designer[0]}", designer[1]),
        block(
            f"{G}/05-game-designer-to-studio.md",
            handoff(5, "game-designer", "studio", "Design", []),
        ),
        block(f"{G}/goal.md", goal(waiting, status="blocked-on-owner")),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, []))
    assert sr.do_run(ws, args(max_ops=25)) == 0
    printed = capsys.readouterr().out
    assert (
        printed.count("Owner question open: goals/G-001-test/03-studio-to-owner.md")
        == 1
    )
    assert printed.index("Owner question open") < printed.index(
        "step-game-designer"
    )  # reported at once
    s = summary(ws)
    assert s["owner_reads"] == f"{G}/03-studio-to-owner.md" and s["next"].startswith(
        "decide"
    )


def test_route_cannot_open_a_second_owner_question(ws, monkeypatch):
    start(
        ws,
        DIRECTOR,
        [
            DIRECTOR_ROW,
            (2, "Decide", "owner", "—", "open", "02-game-director-to-owner.md"),
        ],
    )
    write(ws, f"{G}/02-game-director-to-owner.md", ESCALATION)
    write(
        ws,
        f"{G}/03-game-director-to-studio.md",
        handoff(3, "game-director", "studio", "Decide", []),
    )
    second = STUDIO_ESCALATION.replace("seq: 3", "seq: 4").replace("# 03:", "# 04:")
    out = block(
        f"{G}/goal.md", goal([(*DIRECTOR_ROW[:4], "done", DIRECTOR[0])])
    ) + block(f"{G}/04-studio-to-owner.md", second)
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([out], []))
    with pytest.raises(sr.Rejected):
        sr.do_route(ws, args(goal="G-001", since=2))
    rec = next((ws / "records").glob("*-route"))
    errors = json.loads((rec / "record.json").read_text())["attempts"][0]["errors"]
    assert any(
        "an Escalation is already open (02-game-director-to-owner.md)" in e
        for e in errors
    )


def test_the_manual_ships_with_the_build_and_playtesters_may_read_only_it(tmp_path):
    workspace = tmp_path / "ws"
    sr.main(["init", str(workspace), "--from", str(COMBAT)])
    project = workspace / "project"
    assert (project / "repo" / "manual.md").is_file() and not (
        project / "manual.md"
    ).exists()
    base = [
        "studio/roles/playtester.md",
        "studio/skills/playtest-session.md",
        "project.md#player-profile",
    ]
    for loads, allowed in [
        (base + ["repo/manual.md"], True),
        (base + ["repo/game.py"], False),
    ]:
        text = handoff(1, "studio", "playtester", "Play", loads)
        errors = sr.check_artifact(
            project, f"{G}/01-studio-to-playtester.md", text, "x"
        )
        assert (
            not any("playtester may not load" in e for e in errors)
        ) == allowed, errors


@needs_sandbox
def test_reaction_rules_let_a_player_clear_a_room_from_the_player_view(tmp_path):
    work = tmp_path / "work"
    shutil.copytree(COMBAT / "repo", work)
    (work / "s.txt").write_text(
        "room 1\nwhen see g within 1.4 then attack\nwhen see g within 3 then face\n"
    )
    code, out, _ = sr.sandboxed(
        work, ["python3", "play.py", "--view", "player", "s.txt"]
    )
    assert code == 0 and "room cleared" in out, out
    assert not any(word in out for word in ("ZX-", "invulnerable", "(nothing happens)"))
