"""Compare the Studio's ground truth (truth.jsonl) with what the office showed (screen.jsonl).

    python3 scripts/office/measure/analyze.py <dir> [t_start]

- Lag: from an operation starting or ending (its record folder, its record.json) to the screen
  showing it (the Role's working picture; the Studio label for Route, Intake and Resume).
- Agreement: on a 1 s grid, the share of time the set of working Roles on screen equals the set of
  Roles really running (raw, and leaving out the 5 s after each change, the page's polling time).
- Owner waits: the Goal going blocked-on-owner, and the screen's Goal pill following.
- Console errors other than the page's expected probe for timeline.json.
"""

import json
import statistics
import sys
from pathlib import Path

POLL = 1.2  # the truth recorder looks once a second, so the screen can be up to ~1 s ahead of it
STUDIO_OPS = {"Route", "Intake", "Resume"}

d = Path(sys.argv[1])
t_start = float(sys.argv[2]) if len(sys.argv) > 2 else 0
truth = [json.loads(line) for line in (d / "truth.jsonl").open()]
screen = [json.loads(line) for line in (d / "screen.jsonl").open()]
truth = [e for e in truth if e["t"] >= t_start]
screen_ev = [e for e in screen if e["ev"] == "screen"]
t0 = max(t_start, screen_ev[0]["t"]) if screen_ev else t_start
t1 = max(e["t"] for e in truth + screen)

ops = {}  # name -> op, role, start, end
for e in truth:
    if e["ev"] == "running" and e["name"] not in ops:
        ops[e["name"]] = {"op": e.get("op"), "role": e.get("role"), "start": e["t"], "end": None}
    elif e["ev"] == "done" and e["name"] in ops and ops[e["name"]]["end"] is None:
        ops[e["name"]].update(end=e["t"], status=e.get("status"), op=e.get("op") or ops[e["name"]]["op"])


def screen_at(t):
    last = None
    for e in screen_ev:
        if e["t"] > t:
            break
        last = e
    return last


def first_screen_after(t, pred):
    """Seconds from the event to the first screen showing it (negative: shown before the truth
    recorder noticed). Only screens after the last one well before the event count."""
    before = [e for e in screen_ev if e["t"] < t - POLL]
    for e in screen_ev[len(before) :]:
        if pred(e):
            return e["t"] - t
    return None


def studio_busy(e):
    return bool(e.get("studio")) and "見守り中" not in e["studio"]


lags, rows = {"start": [], "end": []}, []
for name, o in ops.items():
    if o["op"] in STUDIO_OPS:
        start = first_screen_after(o["start"], studio_busy)
        end = first_screen_after(o["end"], lambda e: not studio_busy(e)) if o["end"] else None
    elif o["role"]:
        r = o["role"]
        start = first_screen_after(o["start"], lambda e: r in e["busy"])
        end = first_screen_after(o["end"], lambda e: r not in e["busy"]) if o["end"] else None
    else:
        continue
    rows.append((name, o["op"], o["role"], start, end, o.get("status")))
    lags["start"] += [start] if start is not None else []
    lags["end"] += [end] if end is not None else []


def truth_busy(t):
    return sorted(
        {
            o["role"]
            for o in ops.values()
            if o["role"] and o["op"] not in STUDIO_OPS and o["start"] <= t and (o["end"] is None or t < o["end"])
        }
    )


changes = sorted([o["start"] for o in ops.values()] + [o["end"] for o in ops.values() if o["end"]])
agree = agree_settled = total = settled = 0
mismatches = []
t = t0
while t <= t1:
    s = screen_at(t)
    ok = (s["busy"] if s else []) == truth_busy(t)
    total += 1
    agree += ok
    if not any(c <= t < c + 5 for c in changes):
        settled += 1
        agree_settled += ok
        if not ok:
            mismatches.append((round(t), truth_busy(t), s["busy"] if s else []))
    t += 1

owner = [e for e in truth if e["ev"] == "goal"]
owner_lags = [
    first_screen_after(e["t"], lambda s: bool(s.get("goal")) and "Owner" in s["goal"])
    for e in owner
    if e["status"] == "blocked-on-owner"
]
errors = [e for e in screen if e["ev"] in ("console", "pageerror", "observer-error") and "404" not in e.get("text", "")]
probes = [e for e in screen if e["ev"] == "console" and "404" in e.get("text", "")]


def stats(xs):
    xs = [x for x in xs if x is not None]
    return f"n={len(xs)} median={statistics.median(xs):.1f}s max={max(xs):.1f}s" if xs else "—"


print(f"window {t0:.0f}..{t1:.0f} ({(t1 - t0) / 60:.1f} min), operations {len(rows)}")
for name, op, role, start, end, status in rows:
    fmt = lambda x: None if x is None else round(x, 1)  # noqa: E731
    print("  ", name, op, role or "studio", "start", fmt(start), "end", fmt(end), status)
print("lag start:", stats(lags["start"]))
print("lag end:  ", stats(lags["end"]))
print(f"agreement raw {100 * agree / max(1, total):.1f}% ({total} s), settled {100 * agree_settled / max(1, settled):.1f}% ({settled} s)")
print("settled mismatches (first 10):", mismatches[:10])
print("owner waits:", [e["status"] for e in owner], "screen lag:", [None if x is None else round(x, 1) for x in owner_lags])
print("console errors (not the timeline probe):", len(errors), errors[:5], "| timeline probes:", len(probes))
