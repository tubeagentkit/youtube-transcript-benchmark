# Methodology

This was written, and the video list frozen, before the first result was recorded. The first commit contains `videos.csv`, `selection/` and this file; results come in later commits. Changing the sample later means a new version, not an edit.

## What is measured

For each combination of video and method: did the method return a transcript (at least 20 characters), how long did it take, and if it failed, which error class. Nothing else. Transcript text is never stored or published; only its length is kept.

## Methods

| Id | Method | Notes |
|---|---|---|
| `ytapi` | [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api), latest release; picks the track with `list()` by language prefix, then fetches it | Free library. Fetches directly from YouTube. |
| `ytdlp` | [yt-dlp](https://github.com/yt-dlp/yt-dlp), latest release, installed as `yt-dlp[default]` with node enabled (`--js-runtimes node`), `--skip-download --write-subs --write-auto-subs --sub-langs <lang>` | Free command line tool. Latency includes starting the process. |
| `gyt` | GetYouTubeTranscript hosted API, documented `GET /api/v1/transcript` | Run by the maintainers of this repository, so read its numbers with that in mind. It is used as a black box, through its public documentation only. |

Other hosted services are welcome by pull request (see `CONTRIBUTING.md`). A method is only added with an adapter that uses what the service documents publicly.

Versions of the free tools are recorded in every result line. They are the latest release at run time, not pinned, because most users install the latest.

## How each method is set up

Each method runs the way its own documentation recommends, and all three answer the same question: does this video have a transcript in this language?

- **Language matching.** `en` matches `en`, `en-US`, `en-GB` and so on, manual tracks before automatic ones. youtube-transcript-api's own `fetch(languages=["en"])` and yt-dlp's `--sub-langs en` both match codes exactly, so a video whose only Spanish track is `es-ES` is missed by a request for `es`. The harness therefore lists the tracks and picks by prefix for the library, and gives yt-dlp a regular expression that accepts regional variants (`es(-[A-Z0-9]+)?`). The hosted API takes a language and is used as documented.
- **yt-dlp.** Installed as `yt-dlp[default]`, which includes the JavaScript challenge solver, with a JavaScript runtime enabled. yt-dlp only enables deno by default and warns that YouTube extraction without a runtime is deprecated, so when node is present the harness passes `--js-runtimes node`. The tool versions, the solver package version and the runtime are recorded in every result line.

## Changes after the first run

Written on 2026-10-17, after the first runs, and kept here on purpose. The first two runs exposed three setup mistakes in the harness. All three were found by looking at failures, not by choosing a setup that favours one method, but a reader should know the order of events:

1. **yt-dlp had no JavaScript runtime.** The first run used a bare `pip install yt-dlp`. Three of its 44 failures on caption videos were `This video is not available`, and yt-dlp printed a warning recommending a JavaScript runtime. Two of those videos, re-tested by hand, succeeded with `yt-dlp[default]` and `--js-runtimes node`. Fixed as described above. (Seven further failures were HTTP 429 on the subtitle download. One of them was repeated on the same video and did not go away with the runtime, so it is a property of the tool and network, not of the setup.)
2. **The library was called with exact language codes.** Three of its 44 failures were `NoTranscriptFound` on videos whose only track in that language is a regional variant (`en-US`, `es-ES`). Fixed by language-prefix matching, as described above. The exact-matching behaviour is a real gotcha for library users and is written up in the [errors reference](https://github.com/tubeagentkit/youtube-transcript-errors/blob/main/errors/notranscriptfound.md).

3. **yt-dlp also matches language codes exactly, and the methodology said it did not.** The second run still showed one `no_subtitles` on a video whose only Spanish track is `es-ES` (`yt-dlp --list-subs` shows only that track). This file originally claimed yt-dlp already matched by language; that was an assumption I had not tested, and it was wrong. Fixed with the regular expression above, checked by hand on that video (`es-ES.vtt` is now written).

A check we did on the 429s: yt-dlp's HTTP 429 errors on subtitle downloads were not caused by running right after the library on the same IP. In the second run they happened for 6 of 22 videos when yt-dlp ran first and 2 of 22 when it ran after the library. The numbers are small, so this is weak evidence, but it points to the tool's own subtitle requests. The methods do share one IP, which is a limit of this design.

The earlier-run files are kept as `results/*-run1-superseded.jsonl` and `results/*-run2-superseded.jsonl` and shown under "Earlier runs, superseded". They are not comparable with later runs. Unchanged: the 54 videos (tag `sample-v1`), the success definition, and the request rules. Treat the third run as the first clean measurement. The sample's caption labels still come from one tool (the library), which is a limit already stated above.

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
