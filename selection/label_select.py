#!/usr/bin/env python3
"""Pick the benchmark videos from pool.json and label them with an independent tool.

Walks the pool in its stored order (no shuffling) and, for each candidate that fits an open
category, asks youtube-transcript-api which caption tracks exist. A video is accepted when that
label matches the category. Categories and quotas are fixed below and were written down before
the first benchmark run.

    python label_select.py pool.json videos.csv selection-log.json state.json

Requests are made one at a time with a pause. On an IP block the script waits and retries the same
candidate a few times, then stops. Progress is saved in state.json, so a stopped run can be resumed
and gives the same result as an uninterrupted one (the pool order is fixed).
"""
import csv
import json
import sys
import time

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import _errors as errors

PAUSE = 15
BLOCK_WAIT_S = 1200  # on a block, wait this long and retry the same candidate
MAX_BLOCK_WAITS = 4

# name, quota, test(meta) -> bool, wanted label: "manual:<lang>" | "generated:<lang>" | "any:<lang>" | error class name
CELLS = [
    ("en_manual_short",  6, lambda m: m["audio_lang"].startswith("en") and 0 < m["duration_s"] <= 240 and m["source_label"] == "en_short", "manual:en"),
    ("en_manual_medium", 6, lambda m: m["audio_lang"].startswith("en") and 240 < m["duration_s"] <= 1200 and m["source_label"] == "en_medium", "manual:en"),
    ("en_manual_long",   4, lambda m: m["audio_lang"].startswith("en") and m["duration_s"] >= 3600 and m["source_label"] == "en_long", "manual:en"),
    ("en_auto_only",     8, lambda m: m["audio_lang"].startswith("en") and 60 < m["duration_s"] < 3600 and m["source_label"] in ("en_short", "en_medium"), "autoonly:en"),
    ("en_auto_only_long", 4, lambda m: m["audio_lang"].startswith("en") and m["duration_s"] >= 3600 and m["source_label"] == "en_long", "autoonly:en"),
    ("es_any",           3, lambda m: m["audio_lang"].startswith("es") and 60 < m["duration_s"] < 3600, "any:es"),
    ("hi_any",           3, lambda m: m["audio_lang"].startswith("hi") and 60 < m["duration_s"] < 3600, "any:hi"),
    ("ja_any",           3, lambda m: m["audio_lang"].startswith("ja") and 60 < m["duration_s"] < 3600, "any:ja"),
    ("de_any",           3, lambda m: m["audio_lang"].startswith("de") and 60 < m["duration_s"] < 3600, "any:de"),
    ("short_video",      4, lambda m: 0 < m["duration_s"] <= 60 and m["source_label"] == "shorts", "any:en"),
    ("no_captions",      4, lambda m: m["source_label"] in ("nocap", "en_short", "en_medium"), "TranscriptsDisabled"),
    ("age_restricted",   3, lambda m: m["age_restricted"], "AgeRestricted"),
]
FAKE_IDS = ["aaaaaaaaaaa", "zzzzzzzzzzz", "q1w2e3r4t5y"]  # negative controls, not in the pool


def label(api, vid):
    """Return (kind, manual_langs, generated_langs) or (error class name, [], [])."""
    try:
        tracks = list(api.list(vid))
    except errors.RequestBlocked:
        raise
    except Exception as exc:
        return type(exc).__name__, [], []
    manual = sorted({t.language_code for t in tracks if not t.is_generated})
    generated = sorted({t.language_code for t in tracks if t.is_generated})
    return "tracks", manual, generated


def matches(want, kind, manual, generated):
    if want in ("TranscriptsDisabled", "AgeRestricted"):
        return kind == want
    if kind != "tracks":
        return False
    how, lang = want.split(":")
    has_manual = any(c.split("-")[0] == lang for c in manual)
    has_generated = any(c.split("-")[0] == lang for c in generated)
    if how == "manual":
        return has_manual
    if how == "autoonly":
        return has_generated and not has_manual
    return has_manual or has_generated  # any


def caption_kind(manual, generated, lang):
    m = any(c.split("-")[0] == lang for c in manual)
    g = any(c.split("-")[0] == lang for c in generated)
    return "manual" if m else ("generated" if g else "none")


def main(pool_path, out_csv, log_path, state_path):
    pool = json.load(open(pool_path))["videos"]
    api = YouTubeTranscriptApi()
    try:
        state = json.load(open(state_path))
    except FileNotFoundError:
        state = {"filled": {name: [] for name, *_ in CELLS}, "considered_ids": [], "rejected": 0, "block_waits": 0}
    filled = state["filled"]
    done = set(state["considered_ids"])
    log = {"stopped": None}
    for meta in pool:
        if meta["id"] in done:
            continue
        open_cells = [c for c in CELLS if len(filled[c[0]]) < c[1] and c[2](meta)]
        if not open_cells:
            continue
        waits = 0
        while True:
            try:
                kind, manual, generated = label(api, meta["id"])
                break
            except errors.RequestBlocked as exc:
                waits += 1
                state["block_waits"] += 1
                if waits > MAX_BLOCK_WAITS:
                    log["stopped"] = f"{type(exc).__name__}, gave up after {MAX_BLOCK_WAITS} waits"
                    break
                print(f"blocked, waiting {BLOCK_WAIT_S}s (wait {waits}/{MAX_BLOCK_WAITS})", flush=True)
                time.sleep(BLOCK_WAIT_S)
        if log["stopped"]:
            break
        placed = False
        for name, quota, _test, want in open_cells:
            if matches(want, kind, manual, generated):
                lang = want.split(":")[1] if ":" in want else "en"
                filled[name].append({**meta, "cell": name, "expected_language": lang,
                                     "caption_kind": caption_kind(manual, generated, lang) if ":" in want else "none"})
                placed = True
                break
        if not placed:
            state["rejected"] += 1
        state["considered_ids"].append(meta["id"])
        done.add(meta["id"])
        json.dump(state, open(state_path, "w"))
        print(f"{len(done)} considered; " + ", ".join(f"{n}:{len(filled[n])}/{q}" for n, q, *_ in CELLS), flush=True)
        time.sleep(PAUSE)
        if all(len(filled[n]) >= q for n, q, *_ in CELLS):
            break
    rows = [r for name, *_ in CELLS for r in filled[name]]
    for fid in FAKE_IDS:
        rows.append({"id": fid, "cell": "unavailable", "expected_language": "en", "duration_s": 0,
                     "caption_kind": "none", "published": "", "query": "", "source_label": "control"})
    cols = ["id", "cell", "expected_language", "caption_kind", "duration_s", "published", "query"]
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    log.update(considered=len(done), rejected=state["rejected"], block_waits=state["block_waits"],
               filled={n: len(v) for n, v in filled.items()},
               complete=all(len(filled[n]) >= q for n, q, *_ in CELLS))
    json.dump(log, open(log_path, "w"), indent=2)
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:5])
