"""Run from the repository root: python3 examples/runs/p9-answer-shape-replay/replay.py <out-dir>.

Re-send recorded QA packets as they were and with the Phase 9 answer shape; count missing sections."""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "scripts")
import studio_run as sr  # noqa: E402

R = Path("examples/runs/p8-combat-run/records")
OUT = Path(sys.argv[1])
OUT.mkdir(exist_ok=True)
CASES = [("076-step-qa", 3), ("098-step-qa", 4), ("105-step-qa", 2)]
jobs = []
for name, n in CASES:
    packet = (R / name / f"packet-attempt{n}.md").read_text()
    seq = int(re.search(r"^next_seq: (\d+)$", packet, re.M).group(1))
    out = f"goals/G-001-combat-monotony/{seq:02d}-qa-to-*.md"
    shaped = packet + "\n## Your answer\n\n" + sr.answer_shape(out, sr.role_policy("qa")["escalates"])
    for sample in (1, 2):
        jobs += [(name, "old", sample, packet, out), (name, "new", sample, shaped, out)]


def one(job):
    name, variant, sample, text, out = job
    tag = f"{name}-{variant}-{sample}"
    saved = OUT / f"{tag}.txt"
    if saved.is_file():  # done before an interruption
        result = {"text": saved.read_text(), "usage": json.loads((OUT / f"{tag}.usage").read_text()) if (OUT / f"{tag}.usage").is_file() else None}
    else:
        result = sr.run_claude(text, "sonnet")
        saved.write_text(result["text"])
        (OUT / f"{tag}.usage").write_text(json.dumps(result.get("usage")))
    files = sr.parse_output(result["text"])
    handoffs = [p for p in files if re.fullmatch(out.replace("*", r"[\w-]+").replace(".", r"\."), p)]
    runs = [p for p in files if p.startswith("@run/")]
    if handoffs and isinstance(files[handoffs[0]], str):
        missing = sorted(set(sr.REQUIRED["handoff"]) - sr.headings(sr.parse(files[handoffs[0]])[1]))
        verdict = "complete" if not missing else "missing"
    else:
        missing, verdict = [], "runs" if runs else "no-handoff"
    row = {"case": name, "variant": variant, "sample": sample, "verdict": verdict, "missing": missing,
           "output_tokens": (result.get("usage") or {}).get("output_tokens")}
    print(json.dumps(row), flush=True)
    return row


with ThreadPoolExecutor(3) as pool:
    rows = list(pool.map(one, jobs))
(OUT / "results.json").write_text(json.dumps(rows, indent=1))
for variant in ("old", "new"):
    vs = [r for r in rows if r["variant"] == variant]
    print(variant, {v: sum(r["verdict"] == v for r in vs) for v in ("complete", "missing", "runs", "no-handoff")})
