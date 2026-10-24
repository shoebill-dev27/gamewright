"""Phase 4: goal.md holds the current state; the runtime-written Goal log holds the history.

Deterministic — a fake runtime stands in for executors. Run with `python3 -m pytest tests/`.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import (
    G,
    QA_LOAD,
    REQUEST,
    args,
    block,
    goal,
    handoff,
    sr,
    write,
    ws,
)  # noqa: E402,F401
from test_phase3 import (  # noqa: E402
    ESCALATION,
    QA_OPEN,
    route_out,
    runtime,
    start,
    summary,
)

QA_ROW = (1, "Observe", "qa", "reproduce-defect", "open", QA_OPEN[0])
QA_RESULT = block(
    f"{G}/02-qa-to-studio.md", handoff(2, "qa", "studio", "Next", [], outcome="pass")
)


def log(ws):
    return (ws / "project" / G / "log.md").read_text(encoding="utf-8")


def entries(text):
    return [name for name, _, _ in sr._sections(text)]


def test_every_studio_operation_appends_one_entry_and_keeps_the_rest(ws, monkeypatch):
    project = ws / "project"
    gdir2 = "goals/G-002-dash"
    intake = block(
        f"{gdir2}/goal.md",
        goal([(1, "Observe", "qa", "reproduce-defect", "open", "01-studio-to-qa.md")]),
    ) + block(
        f"{gdir2}/01-studio-to-qa.md",
        handoff(1, "studio", "qa", "Observe", QA_LOAD),
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([intake], []))
    sr.execute(ws, *sr.build_intake(project, REQUEST), args())
    first = (project / gdir2 / "log.md").read_text(encoding="utf-8")
    assert entries(first) == ["001-intake · " + entries(first)[0].split(" · ")[1]]
    assert "Open: 01-studio-to-qa.md." in first

    start(ws, QA_OPEN, [QA_ROW])
    outputs = [
        QA_RESULT,
        route_out([(*QA_ROW[:4], "done", QA_OPEN[0])], status="done"),
    ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, []))
    sr.do_step(ws, args(goal="G-001"))
    assert not (project / G / "log.md").exists()  # a Step adds nothing to the log
    sr.do_route(ws, args(goal="G-001", since=None))
    text = log(ws)
    assert [e.split(" · ")[0] for e in entries(text)] == [
        "Before the log",
        "003-route",
    ]
    assert "Status: done. Open: none." in text

    write(ws, f"{G}/goal.md", goal([QA_ROW]))  # reopen and route again
    monkeypatch.setitem(
        sr.RUNTIMES,
        "fake",
        runtime([route_out([(*QA_ROW[:4], "done", QA_OPEN[0])], status="done")], []),
    )
    sr.do_route(ws, args(goal="G-001", since=1))
    assert log(ws).startswith(text) and len(entries(log(ws))) == 3


def test_resume_appends_and_a_goal_from_before_the_log_keeps_its_history(
    ws, monkeypatch
):
    write(ws, f"{G}/02-game-director-to-owner.md", ESCALATION)
    old = goal(
        [(1, "Decide", "owner", "—", "open", "02-game-director-to-owner.md")],
        status="blocked-on-owner",
    ).replace("## Route changes\n\nNone.", "## Route changes\n\nAfter 1: escalated.")
    write(ws, f"{G}/goal.md", old)
    decision = (
        "---\nkind: decision\nid: D-002\nstatus: accepted\ndecided_by: owner\ngoal: G-001\ndate: 2026-10-12\n"
        "supersedes: none\n---\n# D-002: A\n\n## Decision\n\nA. Owner's words: Aで。\n\n## Rationale\n\nx\n\n"
        "## Alternatives considered\n\nB\n\n## Revisit when\n\nx\n"
    )
    resolved = ESCALATION.replace("status: open", "status: resolved").replace(
        "decision: none", "decision: D-002"
    ) + ("\n**Owner response (2026-10-12):** Aで。\n")
    rows = [
        (1, "Decide", "owner", "—", "done (D-002)", "02-game-director-to-owner.md"),
        (2, "Observe", "qa", "reproduce-defect", "open", "03-studio-to-qa.md"),
    ]
    reinterpreted = goal(rows).replace(
        "## Interpretation\n\nx", "## Interpretation\n\nA, per D-002."
    )
    out = (
        block("decisions/D-002-a.md", decision)
        + block(f"{G}/02-game-director-to-owner.md", resolved)
        + block(f"{G}/goal.md", reinterpreted)
        + block(
            f"{G}/03-studio-to-qa.md", handoff(3, "studio", "qa", "Observe", QA_LOAD)
        )
    )
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([out], []))
    sr.do_decide(ws, args(text="Aで。"))  # Resume may change the Interpretation
    text = log(ws)
    assert [e.split(" · ")[0] for e in entries(text)] == [
        "Before the log",
        "001-resume",
    ]
    assert "After 1: escalated." in sr.section(text, "Before the log")
    assert "Status: active. Open: 03-studio-to-qa.md." in text


@pytest.mark.parametrize("op", ["step", "route"])
def test_no_executor_may_write_the_log(ws, monkeypatch, op):
    start(ws, QA_OPEN, [QA_ROW])
    forged = block(f"{G}/log.md", "# Goal log\n\n## forged\n\nnothing happened\n")
    if op == "step":
        outputs = [QA_RESULT + forged]
    else:
        write(
            ws,
            f"{G}/02-qa-to-studio.md",
            sr.parse_output(QA_RESULT)[f"{G}/02-qa-to-studio.md"],
        )
        outputs = [
            route_out([(*QA_ROW[:4], "done", QA_OPEN[0])], status="done") + forged
        ]
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime(outputs, []))
    with pytest.raises(sr.Rejected):
        (
            sr.do_step(ws, args())
            if op == "step"
            else sr.do_route(ws, args(goal="G-001", since=None))
        )
    assert not (ws / "project" / G / "log.md").exists()


def test_route_packet_carries_the_last_five_entries_only(ws):
    start(ws, QA_OPEN, [QA_ROW])
    write(
        ws,
        f"{G}/log.md",
        sr.LOG_HEAD
        + "".join(f"\n## 00{n}-route · d\n\nentry {n}\n" for n in range(1, 8)),
    )
    project = ws / "project"
    packet, _ = sr.build_route(project, project / G)
    recent = dict(packet.inputs)["@log-recent"]
    assert [f"entry {n}" in recent for n in range(1, 8)] == [False] * 2 + [True] * 5
    assert packet.header["log"].startswith("last 5 of 7 entries")
    assert f"{G}/log.md" not in [label for label, _ in packet.inputs]


def test_first_route_of_a_goal_run_by_hand_sees_every_unrouted_artifact(ws):
    rows = [
        (2, "Diagnose", "qa", "reproduce-defect", "open", QA_OPEN[0]),
        ("2b", "Diagnose", "qa", "reproduce-defect", "open", "02-studio-to-qa.md"),
    ]
    start(ws, QA_OPEN, rows)
    write(
        ws, f"{G}/02-studio-to-qa.md", handoff(2, "studio", "qa", "Diagnose", QA_LOAD)
    )
    for seq in (3, 4):
        write(
            ws, f"{G}/0{seq}-qa-to-studio.md", handoff(seq, "qa", "studio", "Next", [])
        )
    project = ws / "project"
    packet, _ = sr.build_route(project, project / G, ws / "records")  # no records yet
    assert sr.unrouted(
        ws / "records", project / G
    )  # `run` routes them before stepping again
    assert (
        packet.header["step_artifacts"]
        == f"{G}/03-qa-to-studio.md, {G}/04-qa-to-studio.md"
    )


def test_goal_size_limits():
    text = goal([QA_ROW])
    assert sr.check_goal_size(text) == []
    long_changes = text.replace(
        "## Route changes\n\nNone.", "## Route changes\n\n" + "x" * 601
    )
    long_cell = goal(
        [(1, "Observe", "qa", "reproduce-defect", "open " + "y" * 80, QA_OPEN[0])]
    )
    big = text.replace("## Unknowns\n\nx", "## Unknowns\n\n" + "z" * 20_000)
    big_outcome = text.replace("## Outcome\n\n—", "## Outcome\n\n" + "z" * 30_000)
    assert "Route changes has 601 characters" in " ".join(
        sr.check_goal_size(long_changes)
    )
    assert "status cell has 85 characters" in " ".join(sr.check_goal_size(long_cell))
    assert "bytes without its Outcome" in " ".join(sr.check_goal_size(big))
    assert sr.check_goal_size(big_outcome) == []
    long_unknowns = text.replace("## Unknowns\n\nx", "## Unknowns\n\n" + "u" * 3001)
    assert "Unknowns has 3001 characters" in " ".join(sr.check_goal_size(long_unknowns))


def test_route_keeps_the_owner_request_and_interpretation(ws):
    start(ws, QA_OPEN, [QA_ROW])
    project = ws / "project"
    write(
        ws,
        f"{G}/02-qa-to-studio.md",
        sr.parse_output(QA_RESULT)[f"{G}/02-qa-to-studio.md"],
    )
    _, validate = sr.build_route(project, project / G)
    done = goal([(*QA_ROW[:4], "done", QA_OPEN[0])], status="done")

    def errors(text):
        return " ".join(validate({f"{G}/goal.md": text}))

    assert "keep ##" not in errors(done)
    assert "keep ## Interpretation" in errors(
        done.replace("## Interpretation\n\nx", "## Interpretation\n\ny")
    )
    assert "keep ## Owner request" in errors(
        done.replace("ダッシュ中なのに", "ダッシュ中に")
    )
    assert "keep ##" not in errors(
        done.replace("> ダッシュ", ">  ダッシュ")
    )  # whitespace


def test_a_runtime_that_cannot_start_stops_the_run_with_a_record(ws, monkeypatch):
    start(ws, QA_OPEN, [QA_ROW])
    missing = FileNotFoundError(2, "No such file or directory", "claude")
    monkeypatch.setitem(sr.RUNTIMES, "fake", runtime([missing], []))
    assert sr.do_run(ws, args(max_ops=25)) == 3
    assert summary(ws)["stop_reason"].startswith(
        "runtime error: runtime could not start"
    )
    record = sr.json.loads((ws / "records" / "001-step-qa" / "record.json").read_text())
    assert record["status"] == "error"
