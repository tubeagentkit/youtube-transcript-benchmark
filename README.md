# YouTube transcript benchmark

An open, reproducible benchmark of ways to get a YouTube transcript: how often each method works, how fast it is, and how it fails, measured from different networks. The sample was frozen before the first result and everything, including the raw data, is in this repository.

The short version, which the tables below generate from the raw results: **where you run matters at least as much as which method you pick.** A method that works from a home connection can fail on its first request from a cloud server. Each result states the network it came from.

## Results

<!-- results:start -->
### 2026-10-19: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, harness bb210db, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-19-actions.jsonl` (and `2026-10-19-actions-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| GetYouTubeTranscript (hosted API, run by this repo's maintainers) | 100% (44/44) | 920 ms (uncached only; 43 of 44 successes were served from cache) | 920 ms | 0 |
| youtube-transcript-api (library) | 0% (0/5) | n/a | n/a | 49 |
| yt-dlp (command line) | 0% (0/5) | n/a | n/a | 49 |

<details><summary>By category</summary>

| Category | gyt | ytapi | ytdlp |
|---|---|---|---|
| de_any | 100% (3/3) | n/a | n/a |
| en_auto_only | 100% (8/8) | n/a | n/a |
| en_auto_only_long | 100% (4/4) | n/a | n/a |
| en_manual_long | 100% (4/4) | n/a | n/a |
| en_manual_medium | 100% (6/6) | n/a | n/a |
| en_manual_short | 100% (6/6) | 0% (0/5) | 0% (0/5) |
| es_any | 100% (3/3) | n/a | n/a |
| hi_any | 100% (3/3) | n/a | n/a |
| ja_any | 100% (3/3) | n/a | n/a |
| short_video | 100% (4/4) | n/a | n/a |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | gyt | http_404: 3 |
| age_restricted | ytapi | not_attempted_after_blocks: 3 |
| age_restricted | ytdlp | not_attempted_after_blocks: 3 |
| no_captions | gyt | http_404: 4 |
| no_captions | ytapi | not_attempted_after_blocks: 4 |
| no_captions | ytdlp | not_attempted_after_blocks: 4 |
| unavailable | gyt | http_404: 3 |
| unavailable | ytapi | not_attempted_after_blocks: 3 |
| unavailable | ytdlp | not_attempted_after_blocks: 3 |

</details>

### 2026-10-18: home network, India (residential)

54 videos. Tools: youtube-transcript-api 1.2.4, harness 3b3f8e3, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-18-home.jsonl` (and `2026-10-18-home-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| GetYouTubeTranscript (hosted API, run by this repo's maintainers) | 100% (44/44) | 1380 ms (uncached only; 16 of 44 successes were served from cache) | 11.8 s | 0 |
| youtube-transcript-api (library) | 100% (44/44) | 1550 ms | 2085 ms | 0 |
| yt-dlp (command line) | 89% (39/44) | 3760 ms | 6313 ms | 0 |

<details><summary>By category</summary>

| Category | gyt | ytapi | ytdlp |
|---|---|---|---|
| de_any | 100% (3/3) | 100% (3/3) | 100% (3/3) |
| en_auto_only | 100% (8/8) | 100% (8/8) | 88% (7/8) |
| en_auto_only_long | 100% (4/4) | 100% (4/4) | 50% (2/4) |
| en_manual_long | 100% (4/4) | 100% (4/4) | 100% (4/4) |
| en_manual_medium | 100% (6/6) | 100% (6/6) | 100% (6/6) |
| en_manual_short | 100% (6/6) | 100% (6/6) | 100% (6/6) |
| es_any | 100% (3/3) | 100% (3/3) | 100% (3/3) |
| hi_any | 100% (3/3) | 100% (3/3) | 100% (3/3) |
| ja_any | 100% (3/3) | 100% (3/3) | 100% (3/3) |
| short_video | 100% (4/4) | 100% (4/4) | 50% (2/4) |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | gyt | http_404: 3 |
| age_restricted | ytapi | AgeRestricted: 3 |
| age_restricted | ytdlp | age_restricted: 3 |
| no_captions | gyt | http_404: 4 |
| no_captions | ytapi | TranscriptsDisabled: 4 |
| no_captions | ytdlp | no_subtitles: 4 |
| unavailable | gyt | http_404: 3 |
| unavailable | ytapi | VideoUnavailable: 3 |
| unavailable | ytdlp | unavailable: 3 |

</details>

### 2026-10-18: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, harness 3b3f8e3, yt-dlp 2026.08.19, yt-dlp-ejs 0.8.0, js-runtime node. Data: `results/2026-10-18-actions.jsonl` (and `2026-10-18-actions-hosted.jsonl` when present).

| Method | Success on videos with captions | p50 latency | p95 latency | Not attempted (blocked) |
|---|---|---|---|---|
| GetYouTubeTranscript (hosted API, run by this repo's maintainers) | 98% (43/44) | 929 ms (uncached only; 8 of 43 successes were served from cache) | 11.0 s | 0 |
| youtube-transcript-api (library) | 0% (0/5) | n/a | n/a | 49 |
| yt-dlp (command line) | 0% (0/5) | n/a | n/a | 49 |

<details><summary>By category</summary>

| Category | gyt | ytapi | ytdlp |
|---|---|---|---|
| de_any | 100% (3/3) | n/a | n/a |
| en_auto_only | 100% (8/8) | n/a | n/a |
| en_auto_only_long | 100% (4/4) | n/a | n/a |
| en_manual_long | 100% (4/4) | n/a | n/a |
| en_manual_medium | 100% (6/6) | n/a | n/a |
| en_manual_short | 83% (5/6) | 0% (0/5) | 0% (0/5) |
| es_any | 100% (3/3) | n/a | n/a |
| hi_any | 100% (3/3) | n/a | n/a |
| ja_any | 100% (3/3) | n/a | n/a |
| short_video | 100% (4/4) | n/a | n/a |

</details>

<details><summary>Edge cases (outcome counts)</summary>

| Case | Method | Outcomes |
|---|---|---|
| age_restricted | gyt | http_404: 3 |
| age_restricted | ytapi | not_attempted_after_blocks: 3 |
| age_restricted | ytdlp | not_attempted_after_blocks: 3 |
| no_captions | gyt | http_404: 4 |
| no_captions | ytapi | not_attempted_after_blocks: 4 |
| no_captions | ytdlp | not_attempted_after_blocks: 4 |
| unavailable | gyt | http_404: 3 |
| unavailable | ytapi | not_attempted_after_blocks: 3 |
| unavailable | ytdlp | not_attempted_after_blocks: 3 |

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

## What these runs show

Written by hand on 2026-10-18 from the tables above. One day, two networks, 54 videos: patterns, not rankings.

- **From a residential connection, all three methods mostly work.** The hosted API and the library each returned a transcript for 44 of 44 videos with captions. yt-dlp returned 39 of 44: five HTTP 429 errors on subtitle downloads, concentrated in Shorts and long videos with automatic captions. Read the library's 44 of 44 with the caveat below.
- **From a cloud runner, the free tools were blocked at once.** On a GitHub-hosted runner both youtube-transcript-api (`RequestBlocked`) and yt-dlp (bot check) failed all of their first 5 attempts and stopped, with 49 videos not attempted. The hosted API returned 43 of 44 from the same runner and failed once, with an HTTP 504 after 25 seconds. That failure is ours and is counted.
- **Speed is similar for the median and not for the tail.** Median latency for successful, uncached requests: hosted API 0.9 s from the cloud runner and 1.4 s from India (distance counts), library 1.6 s, yt-dlp 3.8 s (it starts a process each time). The hosted API's slow tail is real: its 95th percentile is 11 to 12 seconds, against about 2 s for the library, and it is not explained by video length (a 42-second video took 12 s). We do not know why from outside and will look at it.
- **Edge cases agree.** Every method reports videos with captions disabled, age-restricted videos and unavailable videos as failures, never as transcripts. The library and yt-dlp name them differently; the hosted API answers all three with the same HTTP 404.

**Caveats that change how to read this**

- **The library's score is partly circular.** The caption labels used to build the sample came from youtube-transcript-api, from a home connection. A video was only accepted into a "has captions" category if the library could list its tracks. That favours the library and says nothing for or against the other two methods.
- **One network per type, one day.** A different home connection, country or week can give different results. Cloud addresses are not all treated alike either.
- **Each method ran the way its documentation recommends, after we corrected our own setup three times.** The corrections and why are in [METHODOLOGY.md](METHODOLOGY.md). The earlier runs are in the results folder, marked superseded.

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
