"""Phase 19: the virtual office derives what each Role is doing from a workspace, live or replayed.

Deterministic: recorded runs and temporary workspaces only. Run with `python3 -m pytest tests/`.
"""

import datetime
import json
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import studio_office as so  # noqa: E402
import studio_run as sr  # noqa: E402

RUN = ROOT / "examples" / "runs" / "p17-ember-run"
recorded = pytest.mark.skipif(not RUN.is_dir(), reason="no recorded Phase 17 run")


@recorded
def test_the_final_snapshot_matches_the_records():
    s = so.office_state(RUN)
    gdir = sr.goal_dir(RUN / "project", "G-001")
    assert s["goal"]["status"] == "done" and s["goal"]["budget"] == 19
    assert s["latest_seq"] == max(sr.seq_of(p) for p, _ in sr.goal_artifacts(gdir))
    assert {d["id"] for d in s["decisions"]} == {"D-001", "D-002"}
    assert [x["n"] for x in s["stages"]] == [
        r["n"] for r in sr.route_rows((gdir / "goal.md").read_text())
    ]
    assert s["counts"]["busy"] == 0


@recorded
def test_a_moment_shows_who_was_at_work():
    records = so.load_records(RUN)
    for name, role, label in [
        ("006-step-gameplay-engineer", "gameplay-engineer", "作業中"),
        ("014-step-qa", "qa", "テスト中"),
        ("016-step-playtester", "playtester", "プレイ中"),
    ]:
        rec = next(r for r in records if r["name"] == name)
        s = so.office_state(RUN, at=rec["start"] + datetime.timedelta(seconds=1))
        assert (
            s["agents"][role]["state"] == "busy" and s["agents"][role]["label"] == label
        ), name
        assert sum(a["state"] == "busy" for a in s["agents"].values()) == 1
        assert s["agents"][role]["task"]  # the Task of the Handoff it works from


@recorded
def test_a_replayed_moment_sees_only_what_existed_then():
    records = so.load_records(RUN)
    first_route = next(r for r in records if r["op"] == "Route")
    s = so.office_state(RUN, at=first_route["start"])
    assert s["studio"]["state"] == "busy" and s["studio"]["label"] == "段取り中"
    assert s["latest_seq"] <= 2 and s["decisions"] == []
    assert all(x["status"] != "done" or x["n"] == "1" for x in s["stages"])


@recorded
def test_the_timeline_replays_in_order_and_ends_where_the_run_ended():
    tl = so.timeline(RUN)
    assert [x["now"] for x in tl] == sorted(x["now"] for x in tl) and len(tl) > 20
    end = so.office_state(RUN)
    assert tl[-1]["goal"]["status"] == "done"
    assert [(x["n"], x["status"]) for x in tl[-1]["stages"]] == [
        (x["n"], x["status"]) for x in end["stages"]
    ]


@recorded
def test_a_running_operation_shows_its_role_at_work(tmp_path):
    ws = tmp_path / "ws"
    shutil.copytree(RUN, ws)
    rec = ws / "records" / "099-step-qa"
    rec.mkdir()
    (rec / "packet.md").write_text(
        "# Studio operation packet\n\noperation: Step\ngoal: G-001\nrole: qa\n"
        "incoming_handoff: goals/G-001-first-playable-run/12-gameplay-engineer-to-qa.md\n\n## You may write\n"
    )
    s = so.office_state(ws)
    assert s["agents"]["qa"]["state"] == "busy" and s["agents"]["qa"]["task"]
    assert s["agents"]["qa"]["file"] == "12-gameplay-engineer-to-qa.md"
    assert s["log"][-1]["who"] == "qa" and s["log"][-1]["kind"] == "start"


@recorded
def test_the_server_answers_only_its_own_paths_on_localhost():
    server = so.http.server.ThreadingHTTPServer(("127.0.0.1", 0), so.make_handler(RUN))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        assert server.server_address[0] == "127.0.0.1"
        page = urllib.request.urlopen(base + "/").read().decode()
        assert "<b>Gamewright</b>" in page
        state = json.loads(urllib.request.urlopen(base + "/api/state").read())
        assert state["mode"] == "live"
        layout = json.loads(urllib.request.urlopen(base + "/assets/layout.json").read())
        assert set(layout["roles"]) == set(so.ROLES)
        assert (
            urllib.request.urlopen(base + "/assets/office.webp").headers["Content-Type"]
            == "image/webp"
        )
        for path in (
            "/project/project.md",
            "/../../etc/passwd",
            "/scripts/studio_run.py",
            "/timeline.json",
            "/assets/../studio_office.py",
            "/assets/%2e%2e/studio_office.py",
            "/assets/office.html",
            "/assets/nothing.webp",
        ):
            with pytest.raises(urllib.error.HTTPError) as err:
                urllib.request.urlopen(base + path)
            assert err.value.code == 404, path
    finally:
        server.shutdown()


def test_the_page_never_puts_data_into_html():
    page = so.PAGE.read_text()
    assert (
        "innerHTML" not in page
        and "insertAdjacentHTML" not in page
        and "document.write" not in page
    )
    assert "Content-Security-Policy" in page and "connect-src 'self'" in page


@recorded
def test_export_writes_the_page_and_the_timeline(tmp_path):
    out = so.export(RUN, tmp_path / "replay")
    assert (out / "office.html").read_bytes() == so.PAGE.read_bytes()
    assert (out / "assets" / "layout.json").is_file() and (
        out / "assets" / "office.webp"
    ).is_file()
    assert len(json.loads((out / "timeline.json").read_text())) > 20


def test_every_role_has_a_visible_portrait():
    Image = pytest.importorskip("PIL.Image")
    layout = json.loads((so.ASSETS / "layout.json").read_text())
    for role in layout["roles"]:
        alpha = (
            Image.open(so.ASSETS / f"face-{role}.webp").convert("RGBA").getchannel("A")
        )
        opaque = sum(alpha.point(lambda v: 255 if v > 128 else 0).histogram()[255:])
        assert opaque > alpha.width * alpha.height * 0.5, role


def test_every_role_is_a_whole_character_sprite():
    """Each Role has a working and an idle sprite and a seat mask, and no head is cut off: nothing
    solid on the top edge, or on the sides beside the head (shoulders may reach the sides, and the
    desk hides the bottom)."""
    Image = pytest.importorskip("PIL.Image")
    layout = json.loads((so.ASSETS / "layout.json").read_text())
    for role, entry in layout["roles"].items():
        assert "sprite" in entry and (so.ASSETS / f"mask-{role}.webp").is_file(), role
        for state in ("busy", "idle"):
            alpha = Image.open(so.ASSETS / f"char-{role}-{state}.webp").getchannel("A")
            solid = alpha.point(lambda v: 255 if v > 128 else 0)
            w, h = solid.size
            top = solid.crop((0, 0, w, 1)).histogram()[255]  # a hair strand may touch
            assert top < w * 0.03, (role, state, "top", top)
            for edge in ((0, 0, 1, h // 4), (w - 1, 0, w, h // 4)):
                assert solid.crop(edge).getbbox() is None, (role, state, edge)


CARD_CHECK = """
const { chromium } = require(process.env.PLAYWRIGHT);
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(process.env.URL);
  await page.waitForFunction(() => document.getElementById('dName').textContent !== '\u2014');
  console.log(JSON.stringify(await page.evaluate(() => {
    // each part must show by scrolling the card alone: the panels around it clip and do not scroll
    const card = document.querySelector('.card'), hidden = [];
    for (const id of ['agentSelect', 'dFace', 'dName', 'dState', 'dTask', 'dFile', 'dSince', 'dNext']) {
      const el = document.getElementById(id);
      card.scrollTop = card.contains(el) ? el.offsetTop - card.offsetTop - 4 : 0;
      const r = el.getBoundingClientRect();
      for (let p = el.parentElement; p !== document.body; p = p.parentElement) {
        const c = p.getBoundingClientRect(), s = getComputedStyle(p);
        if (s.overflowY !== 'visible' && (r.top < c.top - 1 || r.bottom > c.bottom + 1)) { hidden.push(id); break; }
      }
    }
    return { hidden, brand: document.querySelector('header .brand b').textContent };
  })));
  await browser.close();
})();
"""


@recorded
@pytest.mark.skipif(
    not (shutil.which("node") and sr.browser_tools()), reason="no node or browser"
)
def test_the_agent_card_shows_everything_at_1280_by_800(tmp_path):
    chrome, modules = sr.browser_tools()
    (tmp_path / "card.js").write_text(CARD_CHECK)
    server = so.http.server.ThreadingHTTPServer(("127.0.0.1", 0), so.make_handler(RUN))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        env = {
            "PATH": "/usr/bin:/bin",
            "HOME": str(Path.home()),
            "CHROME": str(chrome),
            "PLAYWRIGHT": str(modules / "playwright"),
            "URL": f"http://127.0.0.1:{server.server_address[1]}/",
        }
        out = subprocess.run(
            [shutil.which("node"), str(tmp_path / "card.js")],
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
        )
        assert out.returncode == 0, out.stderr
        result = json.loads(out.stdout)
        assert result == {"hidden": [], "brand": "Gamewright"}
    finally:
        server.shutdown()
