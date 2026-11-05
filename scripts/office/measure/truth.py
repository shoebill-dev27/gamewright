"""Ground truth for measuring the virtual office: what the Studio is really doing, from its records.

    python3 scripts/office/measure/truth.py <workspace> <out.jsonl>

Every second: which operations are running (a record folder with a packet but no record.json yet),
which finished and how, and the Goal's status. One JSON line per change. A restart logs the state
of every record again; the analysis keeps the first end it saw for each operation.
"""

import json
import re
import sys
import time
from pathlib import Path

ws, out = Path(sys.argv[1]), Path(sys.argv[2])
seen, goal_status = {}, None


def header(packet):
    head = packet.read_text(encoding="utf-8", errors="replace")[:3000]
    return dict(re.findall(r"^(\w+): (.+)$", head.split("## You may write")[0], re.M))


def log(**kv):
    kv["t"] = time.time()
    with out.open("a") as f:
        f.write(json.dumps(kv, ensure_ascii=False) + "\n")


while True:
    for rec in sorted(p for p in (ws / "records").iterdir() if p.is_dir() and p.name[:3].isdigit()):
        packet, record = rec / "packet.md", rec / "record.json"
        state = "done" if record.is_file() else "running" if packet.is_file() else "new"
        if seen.get(rec.name) == state:
            continue
        info = {}
        if packet.is_file():
            h = header(packet)
            info = {"role": h.get("role"), "op": h.get("operation")}
        if record.is_file():
            try:
                r = json.loads(record.read_text())
                info.update(op=r.get("op", info.get("op")), status=r.get("status"))
            except (OSError, ValueError):
                pass
        log(ev=state, name=rec.name, **info)
        seen[rec.name] = state
    goal = next((ws / "project" / "goals").glob("G-*/goal.md"), None)
    if goal:
        m = re.search(r"^status: (.+)$", goal.read_text(), re.M)
        status = m.group(1).strip() if m else None
        if status != goal_status:
            log(ev="goal", status=status)
            goal_status = status
    time.sleep(1)
