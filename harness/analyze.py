#!/usr/bin/env python3
"""Turn results/*.jsonl into tables and write them into README.md between the markers.

    python harness/analyze.py

Rules that keep the numbers honest:
- Success rate is computed only over videos that have captions (caption_kind not "none"), and only over
  attempted requests. Requests skipped after repeated blocks are counted separately, never as failures
  and never as successes.
- Latency is reported for successful requests only. For hosted APIs that return a `cached` flag, latency
  is reported for uncached responses only, and the share of cached responses is shown next to it.
- Edge cases (no captions, age-restricted, unavailable) are shown as outcome counts, not as a score.
"""
import collections
import glob
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from adapters import LABELS  # noqa: E402

START, END = "<!-- results:start -->", "<!-- results:end -->"
EDGE_CELLS = {"no_captions", "age_restricted", "unavailable"}


def load(pattern: str = "results/*.jsonl") -> list:
    """Every result line, tagged with the file it came from. A file name containing "superseded" marks a run
    made with an earlier version of the harness; it is kept and shown, but in its own section."""
    rows = []
    for path in sorted(glob.glob(str(ROOT / pattern))):
        name = pathlib.Path(path).stem
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line:
                row = json.loads(line)
                row["_file"] = name
                row["_superseded"] = "superseded" in name
                rows.append(row)
    return rows


def percentile(values, q):
    if not values:
        return None
    ordered = sorted(values)
    k = max(0, min(len(ordered) - 1, math.ceil(q / 100 * len(ordered)) - 1))
    return ordered[k]


def pct(n, d):
    return "n/a" if d == 0 else f"{100 * n / d:.0f}% ({n}/{d})"


def ms(v):
    return "n/a" if v is None else (f"{v} ms" if v < 10000 else f"{v / 1000:.1f} s")


def run_key(row):
    return (row["date"], row["env"], row["_file"])


def headline_table(rows) -> str:
    out = ["| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |", "|---|---|---|---|---|"]
    for method in sorted({r["method"] for r in rows}):
        mine = [r for r in rows if r["method"] == method]
        scored = [r for r in mine if r["attempted"] and r["cell"] not in EDGE_CELLS and r["caption_kind"] != "none"]
        ok = [r for r in scored if r["ok"]]
        uncached = [r for r in ok if not r.get("cached")]
        cached_note = ""
        if any("cached" in r for r in ok):
            cached_note = f" (uncached only; {len(ok) - len(uncached)} of {len(ok)} successes were served from cache)"
        lat = [r["ms"] for r in uncached]
        skipped = sum(1 for r in mine if not r["attempted"])
        out.append(
            f"| {LABELS.get(method, method)} | {pct(len(ok), len(scored))} | {ms(percentile(lat, 50))}{cached_note} | "
            f"{ms(percentile(lat, 95))} | {skipped} |"
        )
    return "\n".join(out)


def category_table(rows) -> str:
    methods = sorted({r["method"] for r in rows})
    cells = sorted({r["cell"] for r in rows if r["cell"] not in EDGE_CELLS})
    out = ["| Category | " + " | ".join(m for m in methods) + " |", "|---|" + "---|" * len(methods)]
    for cell in cells:
        cols = []
        for method in methods:
            scored = [r for r in rows if r["method"] == method and r["cell"] == cell and r["attempted"]]
            cols.append(pct(sum(1 for r in scored if r["ok"]), len(scored)))
        out.append(f"| {cell} | " + " | ".join(cols) + " |")
    return "\n".join(out)


def edge_table(rows) -> str:
    out = ["| Case | Method | Outcomes |", "|---|---|---|"]
    for cell in sorted(EDGE_CELLS):
        for method in sorted({r["method"] for r in rows}):
            mine = [r for r in rows if r["cell"] == cell and r["method"] == method]
            if not mine:
                continue
            counts = collections.Counter(("returned text" if r["ok"] else r["error"]) for r in mine)
            out.append(f"| {cell} | {method} | " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())) + " |")
    return "\n".join(out)


def run_section(env_key, subset) -> list:
    versions = subset[0].get("versions", {})
    ver = ", ".join(f"{k} {v}" for k, v in versions.items())
    n_videos = len({r["video_id"] for r in subset})
    return [f"### {env_key[0]}: {env_key[1]}", "", f"{n_videos} videos. Tools: {ver}. Data: `results/{env_key[2]}.jsonl`.", "",
            headline_table(subset), "", "<details><summary>By category</summary>", "", category_table(subset), "", "</details>", "",
            "<details><summary>Edge cases (outcome counts)</summary>", "", edge_table(subset), "", "</details>", ""]


def block(rows) -> str:
    current = [r for r in rows if not r["_superseded"]]
    earlier = [r for r in rows if r["_superseded"]]
    parts = []
    for env_key in sorted({run_key(r) for r in current}, reverse=True):
        parts += run_section(env_key, [r for r in current if run_key(r) == env_key])
    if earlier:
        parts += ["## Earlier runs, superseded", "",
                  "Kept for transparency. These were made before the harness setup was corrected (see \"Changes after the first run\" "
                  "in [METHODOLOGY.md](METHODOLOGY.md)), so they are not comparable with the runs above.", ""]
        for env_key in sorted({run_key(r) for r in earlier}, reverse=True):
            parts += run_section(env_key, [r for r in earlier if run_key(r) == env_key])
    return "\n".join(parts) if parts else "No results yet."


def main() -> int:
    rows = load()
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("README.md is missing the results markers", file=sys.stderr)
        return 1
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    readme.write_text(f"{head}{START}\n{block(rows)}\n{END}{tail}", encoding="utf-8")
    print(f"summarised {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
