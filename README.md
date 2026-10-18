# YouTube transcript benchmark

An open, reproducible benchmark of ways to get a YouTube transcript: how often each method works, how fast it is, and how it fails, measured from different networks. The sample was frozen before the first result and everything, including the raw data, is in this repository.

The short version, which the tables below generate from the raw results: **where you run matters at least as much as which method you pick.** A method that works from a home connection can fail on its first request from a cloud server. Each result states the network it came from.

## Results

<!-- results:start -->
### 2026-10-18: home network, India (residential)

11 videos. Tools: youtube-transcript-api 1.2.4, harness 84eba34, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-18-home.jsonl` (and `2026-10-18-home-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| youtube-transcript-api (library) | 100% (11/11) | 1348 ms | 4646 ms | 0 |
| yt-dlp (command line) | 100% (11/11) | 3581 ms | 4771 ms | 0 |

<details><summary>By category</summary>

| Category | ytapi | ytdlp |
|---|---|---|
| en_manual_medium | 100% (5/5) | 100% (5/5) |
| en_manual_short | 100% (6/6) | 100% (6/6) |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|

</details>

### 2026-10-18: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, harness 3b3f8e3, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-18-actions.jsonl` (and `2026-10-18-actions-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| GetYouTubeTranscript (hosted API, run by this repo's maintainers) | 98% (43/44) | 929 ms (uncached only; 8 of 43 successes were served from cache) | 11.0 s | 0 |

<details><summary>By category</summary>

| Category | gyt |
|---|---|
| de_any | 100% (3/3) |
| en_auto_only | 100% (8/8) |
| en_auto_only_long | 100% (4/4) |
| en_manual_long | 100% (4/4) |
| en_manual_medium | 100% (6/6) |
| en_manual_short | 83% (5/6) |
| es_any | 100% (3/3) |
| hi_any | 100% (3/3) |
| ja_any | 100% (3/3) |
| short_video | 100% (4/4) |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | gyt | http_404: 3 |
| no_captions | gyt | http_404: 4 |
| unavailable | gyt | http_404: 3 |

</details>

### 2026-10-17: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-17-actions.jsonl` (and `2026-10-17-actions-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| youtube-transcript-api (library) | 0% (0/5) | n/a | n/a | 49 |
| yt-dlp (command line) | 0% (0/5) | n/a | n/a | 49 |

<details><summary>By category</summary>

| Category | ytapi | ytdlp |
|---|---|---|
| de_any | n/a | n/a |
| en_auto_only | n/a | n/a |
| en_auto_only_long | n/a | n/a |
| en_manual_long | n/a | n/a |
| en_manual_medium | n/a | n/a |
| en_manual_short | 0% (0/5) | 0% (0/5) |
| es_any | n/a | n/a |
| hi_any | n/a | n/a |
| ja_any | n/a | n/a |
| short_video | n/a | n/a |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | ytapi | not_attempted_after_blocks: 3 |
| age_restricted | ytdlp | not_attempted_after_blocks: 3 |
| no_captions | ytapi | not_attempted_after_blocks: 4 |
| no_captions | ytdlp | not_attempted_after_blocks: 4 |
| unavailable | ytapi | not_attempted_after_blocks: 3 |
| unavailable | ytdlp | not_attempted_after_blocks: 3 |

</details>

## Earlier runs, superseded

Kept for transparency. These were made before the harness setup was corrected (see "Changes after the first run" in [METHODOLOGY.md](METHODOLOGY.md)), so they are not comparable with the runs above.

### 2026-10-17: home network, India (residential)

54 videos. Tools: youtube-transcript-api 1.2.4, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-17-home-run2-superseded.jsonl` (and `2026-10-17-home-run2-superseded-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| youtube-transcript-api (library) | 100% (44/44) | 1505 ms | 5945 ms | 0 |
| yt-dlp (command line) | 80% (35/44) | 3030 ms | 12.6 s | 0 |

<details><summary>By category</summary>

| Category | ytapi | ytdlp |
|---|---|---|
| de_any | 100% (3/3) | 100% (3/3) |
| en_auto_only | 100% (8/8) | 88% (7/8) |
| en_auto_only_long | 100% (4/4) | 50% (2/4) |
| en_manual_long | 100% (4/4) | 75% (3/4) |
| en_manual_medium | 100% (6/6) | 83% (5/6) |
| en_manual_short | 100% (6/6) | 100% (6/6) |
| es_any | 100% (3/3) | 67% (2/3) |
| hi_any | 100% (3/3) | 100% (3/3) |
| ja_any | 100% (3/3) | 100% (3/3) |
| short_video | 100% (4/4) | 25% (1/4) |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | ytapi | AgeRestricted: 3 |
| age_restricted | ytdlp | age_restricted: 3 |
| no_captions | ytapi | TranscriptsDisabled: 4 |
| no_captions | ytdlp | no_subtitles: 4 |
| unavailable | ytapi | VideoUnavailable: 3 |
| unavailable | ytdlp | unavailable: 3 |

</details>

### 2026-10-17: home network, India (residential)

54 videos. Tools: youtube-transcript-api 1.2.4, yt-dlp 2026.08.19. Data: `results/2026-10-17-home-run1-superseded.jsonl` (and `2026-10-17-home-run1-superseded-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| youtube-transcript-api (library) | 93% (41/44) | 1430 ms | 2867 ms | 0 |
| yt-dlp (command line) | 75% (33/44) | 2541 ms | 15.3 s | 0 |

<details><summary>By category</summary>

| Category | ytapi | ytdlp |
|---|---|---|
| de_any | 100% (3/3) | 100% (3/3) |
| en_auto_only | 88% (7/8) | 75% (6/8) |
| en_auto_only_long | 100% (4/4) | 50% (2/4) |
| en_manual_long | 100% (4/4) | 75% (3/4) |
| en_manual_medium | 100% (6/6) | 83% (5/6) |
| en_manual_short | 100% (6/6) | 83% (5/6) |
| es_any | 67% (2/3) | 67% (2/3) |
| hi_any | 100% (3/3) | 100% (3/3) |
| ja_any | 100% (3/3) | 100% (3/3) |
| short_video | 75% (3/4) | 25% (1/4) |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | ytapi | AgeRestricted: 3 |
| age_restricted | ytdlp | age_restricted: 3 |
| no_captions | ytapi | TranscriptsDisabled: 4 |
| no_captions | ytdlp | no_subtitles: 4 |
| unavailable | ytapi | VideoUnavailable: 3 |
| unavailable | ytdlp | unavailable: 3 |

</details>

### 2026-10-17: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-17-actions-run2-superseded.jsonl` (and `2026-10-17-actions-run2-superseded-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| youtube-transcript-api (library) | 0% (0/5) | n/a | n/a | 49 |
| yt-dlp (command line) | 0% (0/5) | n/a | n/a | 49 |

<details><summary>By category</summary>

| Category | ytapi | ytdlp |
|---|---|---|
| de_any | n/a | n/a |
| en_auto_only | n/a | n/a |
| en_auto_only_long | n/a | n/a |
| en_manual_long | n/a | n/a |
| en_manual_medium | n/a | n/a |
| en_manual_short | 0% (0/5) | 0% (0/5) |
| es_any | n/a | n/a |
| hi_any | n/a | n/a |
| ja_any | n/a | n/a |
| short_video | n/a | n/a |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | ytapi | not_attempted_after_blocks: 3 |
| age_restricted | ytdlp | not_attempted_after_blocks: 3 |
| no_captions | ytapi | not_attempted_after_blocks: 4 |
| no_captions | ytdlp | not_attempted_after_blocks: 4 |
| unavailable | ytapi | not_attempted_after_blocks: 3 |
| unavailable | ytdlp | not_attempted_after_blocks: 3 |

</details>

### 2026-10-17: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, yt-dlp 2026.08.19. Data: `results/2026-10-17-actions-run1-superseded.jsonl` (and `2026-10-17-actions-run1-superseded-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| youtube-transcript-api (library) | 0% (0/5) | n/a | n/a | 49 |
| yt-dlp (command line) | 0% (0/5) | n/a | n/a | 49 |

<details><summary>By category</summary>

| Category | ytapi | ytdlp |
|---|---|---|
| de_any | n/a | n/a |
| en_auto_only | n/a | n/a |
| en_auto_only_long | n/a | n/a |
| en_manual_long | n/a | n/a |
| en_manual_medium | n/a | n/a |
| en_manual_short | 0% (0/5) | 0% (0/5) |
| es_any | n/a | n/a |
| hi_any | n/a | n/a |
| ja_any | n/a | n/a |
| short_video | n/a | n/a |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | ytapi | not_attempted_after_blocks: 3 |
| age_restricted | ytdlp | not_attempted_after_blocks: 3 |
| no_captions | ytapi | not_attempted_after_blocks: 4 |
| no_captions | ytdlp | not_attempted_after_blocks: 4 |
| unavailable | ytapi | not_attempted_after_blocks: 3 |
| unavailable | ytdlp | not_attempted_after_blocks: 3 |

</details>

<!-- results:end -->

How to read these: success is counted over attempted requests on videos that have captions. Requests a method never attempted because its network was blocked are counted separately, not as failures. Latency is for successes only and, for the hosted API, for uncached responses only. 54 videos support broad patterns, not small differences. Read [METHODOLOGY.md](METHODOLOGY.md) for the details and the limits of the sample before quoting any number.

## Run it yourself

```bash
pip install youtube-transcript-api "yt-dlp[default]"   # plus Node.js, which yt-dlp uses as its JavaScript runtime
python harness/run.py --env "home network, <country>" --env-slug home --methods ytapi,ytdlp
python harness/analyze.py
```

The hosted API method runs only when `GYT_API_KEY` is set. Requests are sequential and gentle; after five blocks in a row a method stops. Send your results file (`results/<date>-<env-slug>.jsonl`) as a pull request to add your network.

## Adding a method

Write an adapter in `harness/adapters.py` using only what the service documents publicly, register it, and open a pull request. Vendors are welcome to add and correct their own adapter. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Who maintains this

The team behind [GetYouTubeTranscript](https://getyoutubetranscript.com), one of the three methods tested. We publish unfavourable results like any other, and the methodology says how we limit our own influence. MIT licensed.
