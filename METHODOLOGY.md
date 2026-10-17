# Methodology

This was written, and the video list frozen, before the first result was recorded. The first commit contains `videos.csv`, `selection/` and this file; results come in later commits. Changing the sample later means a new version, not an edit.

## What is measured

For each combination of video and method: did the method return a transcript (at least 20 characters), how long did it take, and if it failed, which error class. Nothing else. Transcript text is never stored or published; only its length is kept.

## Methods

| Id | Method | Notes |
|---|---|---|
| `ytapi` | [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api), latest release, `fetch(video_id, languages=[lang])` | Free library. Fetches directly from YouTube. |
| `ytdlp` | [yt-dlp](https://github.com/yt-dlp/yt-dlp), latest release, `--skip-download --write-subs --write-auto-subs --sub-langs <lang>` | Free command line tool. Latency includes starting the process. |
| `gyt` | GetYouTubeTranscript hosted API, documented `GET /api/v1/transcript` | Run by the maintainers of this repository, so read its numbers with that in mind. It is used as a black box, through its public documentation only. |

Other hosted services are welcome by pull request (see `CONTRIBUTING.md`). A method is only added with an adapter that uses what the service documents publicly.

Versions of the free tools are recorded in every result line. They are the latest release at run time, not pinned, because most users install the latest.

## Videos

54 public videos in `videos.csv`: 6 manual-caption short, 6 medium and 4 long English videos; 8 and 4 English videos with automatic captions only; 3 each in Spanish, Hindi, Japanese and German; 4 Shorts; 4 videos with captions disabled; 3 age-restricted videos; and 3 invalid IDs as negative controls.

How they were chosen, so you can repeat or criticise it:

1. `selection/build_pool.mjs` runs 22 fixed searches on the YouTube Data API v3 (queries and filters are in the file) and keeps video details. The result, 1,049 candidates, is `selection/pool.json`.
2. `selection/label_select.py` walks that pool **in stored order, without shuffling**, asks youtube-transcript-api which caption tracks each candidate has, and accepts a video when the answer fits an open category, until each category's quota is full. Its decisions are in `selection/selection-log.json`. Selection ran on 2026-10-17 in two sittings (the first was cut short when the library hit a bot check, so the script now saves its progress and paces itself at one lookup every 15 seconds); because the pool order is fixed, the result is the same as an uninterrupted run. 143 candidates were looked at, 95 did not fit an open category.

Limits of this sample, stated plainly:

- It is **not a random sample of YouTube**. Search results favour popular and recent videos, and a category like "age-restricted" only contains what search surfaced.
- The captions label (manual, automatic, none) comes from one library at selection time, from one home network. A different tool could label a video differently. A video can also change after selection.
- 54 videos support broad patterns, not small differences. Treat any gap under about 10 percentage points as noise.
- Caption-less and unavailable videos are not scored. They are reported as outcome counts under "Edge cases".

## Environments

A result is only meaningful with the network it came from, so every run records one:

- `actions`: a GitHub-hosted runner (a cloud IP). Weekly, by the workflow in this repository.
- `home`: a residential connection, run by hand and committed with its date.

Anyone can add an environment by running the harness and sending the results file. The file name is `<date>-<env-slug>.jsonl`.

## Request rules

Requests are sequential, with a pause between them. The order of methods rotates from video to video so no method always goes first. After 5 blocks in a row (`RequestBlocked`, `IpBlocked`, a bot check or HTTP 429) a method stops for the rest of that run, and the remaining videos are recorded as **not attempted**. They are reported separately and are neither failures nor successes. This keeps the benchmark gentle on YouTube and on the hosted services, and it measures a blocked network as blocked.

## Metrics

- **Success rate**: successful requests over attempted requests, only for videos that have captions and are not in the edge categories. Not-attempted requests are excluded.
- **Latency p50 and p95**: wall clock from request start to result, successes only. For a hosted API that reports a `cached` flag, latency counts uncached responses only, and the share of cached successes is printed next to it, because a cache hit says nothing about a live fetch.
- **Error classes**: library exception class names; yt-dlp stderr patterns mapped to a short list (`bot_check`, `age_restricted`, `http_429`, `unavailable`, `no_subtitles`, `other`, defined in `harness/adapters.py` and covered by tests); HTTP status for the hosted API.

## What this does not measure

Price, behaviour at volume, rate limits, long-term reliability, proxy setups, accuracy of automatic captions, or any method not listed. It is a snapshot of one week from one or two networks, not a ranking.

## Conflict of interest

The maintainers of this repository run one of the three tested services. To limit the effect: the sample was frozen before any result, the harness and raw data are public, failures are classified instead of hidden, the same rules apply to all methods, and results that are unfavourable to the hosted API are published like any other. If you find a mistake in how any method is run, open an issue.
