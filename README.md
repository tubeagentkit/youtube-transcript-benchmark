# YouTube transcript benchmark

An open, reproducible benchmark of ways to get a YouTube transcript: how often each method works, how fast it is, and how it fails, measured from different networks. The sample was frozen before the first result and everything, including the raw data, is in this repository.

The short version, which the tables below generate from the raw results: **where you run matters at least as much as which method you pick.** A method that works from a home connection can fail on its first request from a cloud server. Each result states the network it came from.

## Results

<!-- results:start -->
### 2026-10-17: GitHub Actions runner (ubuntu-latest, hosted cloud IP)

54 videos. Tools: youtube-transcript-api 1.2.4, yt-dlp 2026.08.19.

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
pip install youtube-transcript-api yt-dlp
python harness/run.py --env "home network, <country>" --env-slug home --methods ytapi,ytdlp
python harness/analyze.py
```

The hosted API method runs only when `GYT_API_KEY` is set. Requests are sequential and gentle; after five blocks in a row a method stops. Send your results file (`results/<date>-<env-slug>.jsonl`) as a pull request to add your network.

## Adding a method

Write an adapter in `harness/adapters.py` using only what the service documents publicly, register it, and open a pull request. Vendors are welcome to add and correct their own adapter. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Who maintains this

The team behind [GetYouTubeTranscript](https://getyoutubetranscript.com), one of the three methods tested. We publish unfavourable results like any other, and the methodology says how we limit our own influence. MIT licensed.
