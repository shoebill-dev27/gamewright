#!/usr/bin/env python3
"""Virtual office: watch the Studio's Roles at work, live or replayed (docs/phase19.md).

Read-only: it derives everything from a workspace's files and never writes to it.

  studio_office.py serve  <ws> [--port 8765]          # live view on http://127.0.0.1:<port>/
  studio_office.py export <ws> <out-dir>               # replay: office.html + timeline.json
  studio_office.py state  <ws> [--at ISO-TIME]         # one snapshot as JSON (for checks)
"""

import argparse
import datetime
import http.server
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_run as sr  # noqa: E402

PAGE = Path(__file__).resolve().parent / "office" / "office.html"
ASSETS = PAGE.parent / "assets"
ASSET_TYPES = {".webp": "image/webp", ".png": "image/png", ".json": "application/json"}


def asset(path):
    """The asset file a request path names (/assets/<name>), or None: only plain file names in the
    assets directory, never anything outside it."""
    name = path[len("/assets/") :] if path.startswith("/assets/") else ""
    if not re.fullmatch(r"[a-z0-9-]+\.(webp|png|json)", name):
        return None
    f = ASSETS / name
    return f if f.is_file() else None


STUDIO_OPS = ("Intake", "Route", "Resume")
ROLES = [
    "game-director",
    "game-designer",
    "technical-director",
    "art-director",
    "gameplay-engineer",
    "qa",
    "playtester",
]
SHORT = {
    "game-director": "Director",
    "game-designer": "Designer",
    "technical-director": "Technical Director",
    "art-director": "Art Director",
    "gameplay-engineer": "Engineer",
    "qa": "QA",
    "playtester": "Playtester",
    "studio": "Studio",
    "owner": "Owner",
}
BUSY = {"qa": "テスト中", "playtester": "プレイ中", "game-director": "レビュー中"}


def parse_time(text):
    return datetime.datetime.fromisoformat(text)


def fmt(t):
    return t.isoformat(timespec="seconds") if t else None


# --- Records -----------------------------------------------------------------------------------


def load_records(ws):
    """One entry per operation: when it ran, what it did, and whether it is still running."""
    out = []
    root = ws / "records"
    if not root.is_dir():
        return out
    for rec in sorted(p for p in root.iterdir() if p.is_dir() and p.name[:3].isdigit()):
        packet = rec / "packet.md"
        head = (
            packet.read_text(encoding="utf-8", errors="replace")[:3000]
            if packet.is_file()
            else ""
        )
        header = dict(
            re.findall(r"^(\w+): (.+)$", head.split("## You may write")[0], re.M)
        )
        entry = {
            "name": rec.name,
            "op": header.get("operation", rec.name.split("-")[1].capitalize()),
            "role": header.get("role"),
            "goal": (
                (header.get("goal") or "").split()[0] if header.get("goal") else None
            ),
            "incoming": header.get("incoming_handoff"),
            "attempts": [],
            "rounds": [],
            "status": None,
            "written": {},
            "running": False,
            "start": None,
            "end": None,
        }
        path = rec / "record.json"
        if path.is_file():
            record = json.loads(path.read_text(encoding="utf-8"))
            if record.get("op") == "Run" or "attempts" not in record:
                continue  # a continuous run's summary, not an operation
            entry.update(
                op=record.get("op", entry["op"]),
                role=record.get("role") or entry["role"],
                goal=record.get("goal") or entry["goal"],
                status=record.get("status"),
                written=record.get("written", {}),
            )
            for a in record.get("attempts", []):
                start = parse_time(a["started"])
                entry["attempts"].append(
                    {
                        "start": start,
                        "end": start
                        + datetime.timedelta(seconds=float(a.get("seconds") or 0)),
                        "errors": a.get("errors") or [],
                        "runs": a.get("runs") or [],
                        "need": a.get("need"),
                    }
                )
        else:
            if not packet.is_file():
                continue
            entry["running"] = True
            entry["start"] = datetime.datetime.fromtimestamp(
                packet.stat().st_mtime
            ).replace(microsecond=0)
        for n in range(1, 4):
            rp = rec / f"runs-round{n}.json"
            if rp.is_file():
                entry["rounds"].append(
                    [
                        {
                            "run": r["run"],
                            "exit": r["exit"],
                            "images": len(r.get("images") or []),
                        }
                        for r in json.loads(rp.read_text(encoding="utf-8"))
                    ]
                )
        check = rec / "build-check.json"
        entry["check"] = (
            json.loads(check.read_text())["exit"] if check.is_file() else None
        )
        if entry["attempts"]:
            entry["start"] = entry["attempts"][0]["start"]
            entry["end"] = entry["attempts"][-1]["end"]
        if entry["start"] is None:
            continue
        entry["actor"] = entry["role"] if entry["op"] == "Step" else "studio"
        entry["dir"] = rec
        out.append(entry)
    return out


def events(records):
    """What happened, in time order, as lines for the live log."""
    ev = []
    for r in records:
        who = r["actor"]
        if r["op"] == "Step":
            ev.append(
                (
                    r["start"],
                    who,
                    "start",
                    f"作業を始めました（{Path(r['incoming'] or '').name}）",
                )
            )
        else:
            ev.append(
                (
                    r["start"],
                    who,
                    "start",
                    {
                        "Route": "工程の段取りを始めました",
                        "Intake": "Goal を受け付けています",
                        "Resume": "Owner の判断を記録しています",
                    }.get(r["op"], "作業を始めました"),
                )
            )
        rounds = iter(r["rounds"])
        for a in r["attempts"]:
            if a["need"]:
                ev.append(
                    (
                        a["end"],
                        who,
                        "need",
                        f"資料を追加で求めました（{len(a['need'])} 件）",
                    )
                )
            if a["runs"]:
                results = next(rounds, [])
                text = "、".join(
                    f"{x['run']}（exit {x['exit']}"
                    + (f"、画面 {x['images']} 枚" if x["images"] else "")
                    + "）"
                    for x in results
                ) or "、".join(a["runs"])
                ev.append((a["end"], who, "run", f"実行: {text}"))
            if a["errors"]:
                ev.append((a["end"], who, "reject", f"差し戻し: {a['errors'][0][:80]}"))
        if r["end"] and r["status"] == "ok":
            if r["check"] is not None:
                ev.append(
                    (
                        r["end"],
                        who,
                        "check",
                        "ランナーの試験: "
                        + (
                            "合格"
                            if r["check"] == 0
                            else f"不合格（exit {r['check']}）"
                        ),
                    )
                )
            names = [Path(p).name for p in r["written"]]
            ev.append(
                (
                    r["end"],
                    who,
                    "done",
                    "提出: "
                    + "、".join(names[:3])
                    + (f" ほか {len(names) - 3} 件" if len(names) > 3 else ""),
                )
            )
        elif r["end"] and r["status"] in ("rejected", "error"):
            ev.append(
                (
                    r["end"],
                    who,
                    "fail",
                    "この工程は通りませんでした（" + r["status"] + "）",
                )
            )
    return sorted(ev, key=lambda e: (e[0], e[2] != "start"))


# --- goal.md as it was at a moment (replayed from the Studio operations' outputs) -------------


def apply_edits(text, edits):
    for search, replace in edits:
        if (
            text.count(search) != 1
            and search.endswith("\n")
            and text.count(search[:-1]) == 1
        ):
            search, replace = search[:-1], (
                replace[:-1] if replace.endswith("\n") else replace
            )
        if text.count(search) != 1:
            return None
        text = text.replace(search, replace, 1)
    return text


def goal_history(records, gdir_rel):
    """[(time, goal.md text)] after each Studio operation that wrote it."""
    history, text = [], None
    target = f"{gdir_rel}/goal.md"
    for r in records:
        if (
            r["op"] not in STUDIO_OPS
            or r["status"] != "ok"
            or target not in r["written"]
        ):
            continue
        outs = sorted(
            r["dir"].glob("output-attempt*.txt"),
            key=lambda p: int(re.findall(r"\d+", p.stem)[-1]),
        )
        if not outs:
            continue
        files = sr.parse_output(outs[-1].read_text(encoding="utf-8"))
        got = files.get(target)
        if isinstance(got, str):
            text = got
        elif got is not None and text is not None:
            text = apply_edits(text, got)
        if text is not None:
            history.append((r["end"], text))
    return history


# --- The snapshot --------------------------------------------------------------------------------


def first_line(text, limit=90):
    line = " ".join(text.split())
    return line if len(line) <= limit else line[: limit - 1] + "…"


def title_of(text):
    """The H1 without its number and, for a Handoff, without its "from → to — " prefix."""
    m = re.search(r"^# (?:[\w-]+: )?(.+)$", sr.parse(text)[1], re.M)
    title = m.group(1).strip() if m else ""
    return (
        title.split(" — ", 1)[1]
        if " → " in title.split(" — ", 1)[0] and " — " in title
        else title
    )


def office_state(ws, at=None):
    project = ws / "project"
    meta = sr.project_meta(project)
    records = load_records(ws)
    live = at is None
    now = at or datetime.datetime.now().replace(microsecond=0)
    try:
        gdir = sr.goal_dir(project)
    except sr.Rejected:
        gdir = None
    gid = gdir.name[:5] if gdir else None
    gdir_rel = str(gdir.relative_to(project)) if gdir else None
    mine = [r for r in records if gid and (r["goal"] or "").startswith(gid)] or records

    def happened(t):
        return t is not None and t <= now

    seen = [r for r in mine if happened(r["start"])]
    running = [r for r in seen if r["running"] or (r["end"] and r["end"] > now)]
    finished = [r for r in seen if r["end"] and r["end"] <= now]
    written_at = {}
    for r in finished:
        for path in r["written"]:
            written_at.setdefault(path, r["end"])

    # goal.md at this moment
    goal_text = (
        (gdir / "goal.md").read_text(encoding="utf-8")
        if gdir and (gdir / "goal.md").is_file()
        else ""
    )
    if not live and gdir:
        past = [t for when, t in goal_history(mine, gdir_rel) if when <= now]
        goal_text = past[-1] if past else ""
    gmeta = sr.parse(goal_text)[0] if goal_text else {}
    rows = sr.route_rows(goal_text) if goal_text else []

    # Handoffs and Decisions that exist at this moment
    handoffs = []
    for path, m in (sr.goal_artifacts(gdir) if gdir else []):
        rel = str(path.relative_to(project))
        when = written_at.get(rel)
        if not live and when is None:
            continue
        text = path.read_text(encoding="utf-8")
        handoffs.append(
            {
                "seq": sr.seq_of(path),
                "file": path.name,
                "kind": m.get("kind"),
                "from": m.get("from"),
                "to": m.get("to"),
                "stage": m.get("stage") or "",
                "outcome": m.get("outcome") or m.get("status") or "",
                "title": first_line(title_of(text), 70),
                "task": first_line(
                    sr.section(sr.parse(text)[1], "Task")
                    or sr.section(sr.parse(text)[1], "Question"),
                    140,
                ),
                "time": fmt(when),
            }
        )
    decisions = []
    for path in sorted((project / "decisions").glob("D-*.md")):
        rel = str(path.relative_to(project))
        when = written_at.get(rel)
        if not live and when is None:
            continue
        m = sr.parse(path.read_text(encoding="utf-8"))[0]
        decisions.append(
            {
                "id": m.get("id") or path.name[:5],
                "title": first_line(title_of(path.read_text(encoding="utf-8")), 70),
                "by": m.get("decided_by") or "",
                "date": m.get("date") or "",
                "time": fmt(when),
            }
        )

    # The seven Roles
    by_file = {h["file"]: h for h in handoffs}
    agents = {}
    for role in ROLES:
        work = next((r for r in running if r["actor"] == role), None)
        open_row = next(
            (
                x
                for x in rows
                if x["role"] == role and x["status"].lower().startswith("open")
            ),
            None,
        )
        task, stage, since, h = "", "", None, None
        if work:
            h = by_file.get(Path(work["incoming"] or "").name)
            task, stage, since = (
                (h or {}).get("task", ""),
                (h or {}).get("stage", ""),
                work["start"],
            )
            state, label = "busy", BUSY.get(role, "作業中")
        elif open_row:
            h = by_file.get(open_row["handoff"])
            task, stage = (h or {}).get("task", ""), open_row["stage"]
            state, label = "waiting", "待機中"
        else:
            state, label = "idle", "手すき"
        mine_done = [r for r in finished if r["actor"] == role]
        agents[role] = {
            "state": state,
            "label": label,
            "task": task,
            "stage": stage,
            "since": fmt(since),
            "file": (h or {}).get("file", ""),
            "steps_done": len(mine_done),
            "last": None,
        }
    studio_busy = next((r for r in running if r["actor"] == "studio"), None)

    log = [e for e in events(mine) if e[0] <= now]
    for role in ROLES + ["studio"]:
        last = next((e for e in reversed(log) if e[1] == role), None)
        if last and role in agents:
            agents[role]["last"] = {"time": fmt(last[0]), "text": last[3]}

    used = len([r for r in mine if happened(r["start"])])
    return {
        "mode": "live" if live else "replay",
        "now": fmt(now),
        "project": {"id": meta.get("id", ""), "name": meta.get("name", "")},
        "goal": {
            "id": gid or "",
            "title": first_line(title_of(goal_text), 60) if goal_text else "",
            "status": gmeta.get("status", ""),
            "request": (
                first_line(
                    sr.section(sr.parse(goal_text)[1], "Owner request")
                    .strip()
                    .lstrip("> "),
                    120,
                )
                if goal_text
                else ""
            ),
            "budget": (
                int(gmeta["budget"]) if str(gmeta.get("budget", "")).isdigit() else None
            ),
            "used": used,
        },
        "stages": [
            {"n": x["n"], "stage": x["stage"], "role": x["role"], "status": x["status"]}
            for x in rows
        ],
        "agents": agents,
        "studio": {
            "state": "busy" if studio_busy else "idle",
            "label": (
                {"Route": "段取り中", "Intake": "受付中", "Resume": "判断を記録中"}.get(
                    studio_busy["op"], "段取り中"
                )
                if studio_busy
                else "見守り中"
            ),
            "since": fmt(studio_busy["start"]) if studio_busy else None,
        },
        "handoffs": sorted(handoffs, key=lambda h: h["seq"], reverse=True)[:8],
        "latest_seq": max([h["seq"] for h in handoffs] or [0]),
        "decisions": decisions[-6:][::-1],
        "log": [
            {"time": fmt(t), "who": who, "kind": kind, "text": text}
            for t, who, kind, text in log[-40:]
        ],
        "queue": [
            {"n": x["n"], "stage": x["stage"], "role": x["role"], "status": x["status"]}
            for x in rows
            if re.match(r"(open|planned|tentative)", x["status"].lower())
        ],
        "counts": {
            "busy": sum(a["state"] == "busy" for a in agents.values()),
            "waiting": sum(a["state"] == "waiting" for a in agents.values()),
            "idle": sum(a["state"] == "idle" for a in agents.values()),
        },
    }


def timeline(ws):
    """Snapshots after every event, for replay."""
    records = load_records(ws)
    times = sorted({e[0] for e in events(records)})
    return [office_state(ws, at=t) for t in times]


# --- Live server -----------------------------------------------------------------------------------


def make_handler(ws):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            path = self.path.split("?")[0]
            if path in ("/", "/office.html"):
                self.send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
            elif asset(path):
                f = asset(path)
                self.send(200, f.read_bytes(), ASSET_TYPES[f.suffix])
            elif path == "/api/state":
                body = json.dumps(office_state(ws), ensure_ascii=False).encode()
                self.send(200, body, "application/json; charset=utf-8")
            else:
                self.send(404, b"not found", "text/plain; charset=utf-8")

        def send(self, code, body, kind):
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):  # keep the terminal quiet
            pass

    return Handler


def serve(ws, port):
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), make_handler(ws))
    print(
        f"Virtual office for {ws}: http://127.0.0.1:{server.server_address[1]}/  (Ctrl+C to stop)"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def export(ws, out):
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(PAGE, out / "office.html")
    if ASSETS.is_dir():
        shutil.copytree(ASSETS, out / "assets", dirs_exist_ok=True)
    (out / "timeline.json").write_text(
        json.dumps(timeline(ws), ensure_ascii=False), encoding="utf-8"
    )
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("command", choices=["serve", "export", "state"])
    ap.add_argument("workspace", type=Path)
    ap.add_argument("out", type=Path, nargs="?")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--at")
    args = ap.parse_args(argv)
    if args.command == "serve":
        serve(args.workspace, args.port)
    elif args.command == "export":
        if not args.out:
            ap.error("export needs an output directory")
        print(export(args.workspace, args.out))
    else:
        at = parse_time(args.at) if args.at else None
        print(
            json.dumps(office_state(args.workspace, at), ensure_ascii=False, indent=1)
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
