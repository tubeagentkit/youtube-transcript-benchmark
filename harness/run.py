#!/usr/bin/env python3
"""Run the benchmark and write one JSON line per (video, method) attempt.

    python harness/run.py --env "home network, India" --methods ytapi,ytdlp,gyt

--env is required and describes where the requests come from; results are meaningless without it.
The gyt method needs GYT_API_KEY in the environment and is skipped when it is missing.
Requests are sequential with a pause. After MAX_CONSECUTIVE_BLOCKS blocks in a row a method stops and
the remaining videos are recorded as not attempted, so a blocked network is measured, not hammered.
"""
import argparse
import csv
import datetime
import importlib.metadata
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from adapters import ADAPTERS, BLOCK_ERRORS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAUSE_S = 5
MAX_CONSECUTIVE_BLOCKS = 5


def tool_versions() -> dict:
    versions = {"youtube-transcript-api": importlib.metadata.version("youtube-transcript-api")}
    if shutil.which("yt-dlp"):
        versions["yt-dlp"] = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True).stdout.strip()
    return versions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True, help="where the requests come from, e.g. 'GitHub Actions runner'")
    parser.add_argument("--env-slug", required=True, help="short file-name label, e.g. actions or home")
    parser.add_argument("--methods", default="ytapi,ytdlp,gyt")
    parser.add_argument("--videos", default=str(ROOT / "videos.csv"))
    parser.add_argument("--limit", type=int, default=0, help="only the first N videos (for testing)")
    args = parser.parse_args()

    methods = [m for m in args.methods.split(",") if m]
    if "gyt" in methods and not os.environ.get("GYT_API_KEY"):
        print("GYT_API_KEY not set: skipping gyt", file=sys.stderr)
        methods.remove("gyt")
    videos = list(csv.DictReader(open(args.videos, encoding="utf-8")))
    if args.limit:
        videos = videos[: args.limit]

    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    out_path = ROOT / "results" / f"{today}-{args.env_slug}.jsonl"
    out_path.parent.mkdir(exist_ok=True)
    versions = tool_versions()
    consecutive_blocks = {m: 0 for m in methods}
    stopped = {m: False for m in methods}

    with open(out_path, "w", encoding="utf-8") as out:
        for index, video in enumerate(videos):
            # rotate the order so no method always goes first on a fresh network state
            order = methods[index % len(methods):] + methods[: index % len(methods)]
            for method in order:
                record = {"date": today, "env": args.env, "method": method, "video_id": video["id"],
                          "cell": video["cell"], "language": video["expected_language"], "caption_kind": video["caption_kind"],
                          "versions": versions}
                if stopped[method]:
                    record.update(attempted=False, ok=False, error="not_attempted_after_blocks")
                else:
                    result = ADAPTERS[method](video["id"], video["expected_language"])
                    record.update(attempted=True, ok=result.ok, error=result.error, chars=result.chars, ms=result.ms, **result.extra)
                    consecutive_blocks[method] = consecutive_blocks[method] + 1 if result.error in BLOCK_ERRORS else 0
                    if consecutive_blocks[method] >= MAX_CONSECUTIVE_BLOCKS:
                        stopped[method] = True
                    time.sleep(PAUSE_S)
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
