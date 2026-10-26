"""Phase 18: screenshots of a build's page (`shot`) reach the next executor as images.

Mostly deterministic (a fake runtime stands in for executors); the live screenshot test needs
bubblewrap, node and a local Chromium with Playwright. Run with `python3 -m pytest tests/`.
"""

import json
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_phase2 import G, args, block, goal, handoff, sr, write  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EMBER_FIXTURE = ROOT / "examples" / "fixtures" / "ember-hollow"
EMBER_BUILD = ROOT / "examples" / "runs" / "p17-ember-run" / "project" / "repo"
can_shoot = pytest.mark.skipif(
    not (shutil.which("bwrap") and shutil.which("node") and sr.browser_tools()),
    reason="no bubblewrap, node or local browser",
)


def ember_ws(tmp_path, page=True):
    workspace = tmp_path / "ws"
    sr.main(["init", str(workspace), "--from", str(EMBER_FIXTURE)])
    project = workspace / "project"
    shutil.rmtree(project / "repo")
    shutil.copytree(EMBER_BUILD, project / "repo")
    if page:
        text = (project / "project.md").read_text()
        (project / "project.md").write_text(
            text.replace("build: repo\n", "build: repo\npage: index.html\n")
        )
    return workspace


def test_shot_is_offered_only_with_a_page_and_a_browser(tmp_path, monkeypatch):
    workspace = ember_ws(tmp_path)
    project = workspace / "project"
    monkeypatch.setattr(sr, "browser_tools", lambda: (Path("/x/chrome"), Path("/x/nm")))
    described = sr.run_commands(project)["shot"]
    assert "page index.html#<fragment>" in described and "size <w>x<h>" in described
    monkeypatch.setattr(sr, "browser_tools", lambda: None)
    assert "shot" not in sr.run_commands(project)
    monkeypatch.setattr(sr, "browser_tools", lambda: (Path("/x/chrome"), Path("/x/nm")))
    assert "shot" not in sr.run_commands(
        ember_ws(tmp_path / "b", page=False) / "project"
    )


def test_roles_that_look_at_the_game_may_take_screenshots():
    for role in ("art-director", "playtester", "qa", "game-designer", "game-director"):
        assert "shot" in sr.role_policy(role)["runs"], role
    for role in ("gameplay-engineer", "technical-director"):
        assert "shot" not in sr.role_policy(role)["runs"], role


def test_the_claude_runtime_sends_text_and_images_in_one_message(monkeypatch):
    seen = {}

    def fake_run(cmd, input=None, **kw):
        seen["cmd"], seen["input"] = cmd, input
        events = [
            {
                "type": "system",
                "subtype": "init",
                "tools": [],
                "mcp_servers": [],
                "model": "m",
            },
            {"type": "result", "result": "ok", "session_id": "s", "usage": {}},
        ]
        return SimpleNamespace(
            stdout="\n".join(map(json.dumps, events)), stderr="", returncode=0
        )

    monkeypatch.setattr(sr.subprocess, "run", fake_run)
    sr.run_claude(
        "PACKET",
        None,
        images=[{"label": "@run/shot/a screenshot 1", "data": b"\x89PNG"}],
    )
    message = json.loads(seen["input"])["message"]
    kinds = [c["type"] for c in message["content"]]
    assert "--input-format" in seen["cmd"] and kinds == ["text", "text", "image"]
    assert message["content"][0]["text"] == "PACKET"
    sr.run_claude("PACKET", None)
    assert seen["input"] == "PACKET" and "--input-format" not in seen["cmd"]


def test_the_codex_runtime_refuses_images():
    with pytest.raises(RuntimeError):
        sr.run_codex("PACKET", None, images=[{"label": "x", "data": b""}])


@can_shoot
def test_a_shot_run_attaches_screenshots_to_the_next_executor(tmp_path, monkeypatch):
    workspace = ember_ws(tmp_path)
    name = "01-studio-to-art-director.md"
    write(
        workspace,
        f"{G}/goal.md",
        goal([(1, "Verify", "art-director", "visual-review", "open", name)]),
    )
    write(
        workspace,
        f"{G}/{name}",
        handoff(
            1, "studio", "art-director", "Verify", ["studio/roles/art-director.md"]
        ),
    )
    received = []

    def run(packet_text, model=None, images=None):
        received.append(images or [])
        out = (
            block(
                "@run/shot/start",
                "page index.html#seed-42\nsize 1200x800\nArrowLeft shot dd.s shot\n",
            )
            if len(received) == 1
            else block(
                f"{G}/02-art-director-to-studio.md",
                handoff(2, "art-director", "studio", "Verify", [], outcome="done"),
            )
        )
        return {
            "runtime": "fake",
            "text": out,
            "session_id": f"s{len(received)}",
            "model": "fake",
            "tools": [],
            "mcp_servers": [],
            "tool_uses": [],
            "usage": None,
        }

    monkeypatch.setitem(sr.RUNTIMES, "fake", run)
    sr.do_step(workspace, args(goal="G-001"))
    assert received[0] == [] and len(received[1]) == 2
    assert all(i["data"].startswith(b"\x89PNG") for i in received[1])
    width, height = (
        int.from_bytes(received[1][0]["data"][o : o + 4], "big") for o in (16, 20)
    )
    assert (width, height) == (1200, 800)  # the size line
    rec = next((workspace / "records").glob("*-step-art-director"))
    assert sorted(p.name for p in rec.glob("shot-*.png")) == [
        "shot-round1-1.png",
        "shot-round1-2.png",
    ]
    result = json.loads((rec / "runs-round1.json").read_text())[0]
    assert result["exit"] == 0 and '"console_errors":[]' in result["output"]
    assert '"keys_pressed":5' in result["output"]  # "dd.s" is four presses


# --- Recorded live run ---------------------------------------------------------------------

RUN = ROOT / "examples" / "runs" / "p18-art-run"


@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 18 run")
def test_recorded_studio_looked_at_its_own_pictures():
    gdir = sr.goal_dir(RUN / "project", "G-002")
    assert sr.parse((gdir / "goal.md").read_text())[0]["status"] == "done"
    lookers = set()
    for result in RUN.glob("records/*/runs-round*.json"):
        for r in json.loads(result.read_text()):
            if r["run"].startswith("@run/shot") and r.get("images"):
                lookers.add(result.parent.name.split("-step-")[1])
    assert {"qa", "art-director"} <= lookers


@pytest.mark.skipif(
    not (shutil.which("bwrap") and shutil.which("node")), reason="no bubblewrap or node"
)
@pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 18 run")
def test_recorded_pictures_left_the_rules_alone(tmp_path):
    p17 = ROOT / "examples" / "runs" / "p17-ember-run"
    for name in ("rng", "floorgen", "light", "game", "view"):
        assert (RUN / "project/repo/src" / f"{name}.js").read_bytes() == (
            p17 / "project/repo/src" / f"{name}.js"
        ).read_bytes(), name
    work = tmp_path / "w"
    shutil.copytree(RUN / "project" / "repo", work)
    win = json.loads((p17 / "held-out.json").read_text())["V5_win_and_loss"]["win"]
    (work / "s.txt").write_text(f"seed {win['seed']}\n{win['commands']}\n")
    code, out, _ = sr.sandboxed(work, ["node", "play.js", "s.txt"])
    assert code == 0 and "Result: Victory" in out
