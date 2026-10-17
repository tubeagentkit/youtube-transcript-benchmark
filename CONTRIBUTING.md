# Contributing

## Add your network

1. `pip install youtube-transcript-api yt-dlp pytest`
2. `python harness/run.py --env "<describe the network>" --env-slug <short-name> --methods ytapi,ytdlp`
3. `python harness/analyze.py` and check `README.md` renders your section.
4. Open a pull request containing only `results/<date>-<short-name>.jsonl` and the regenerated README block.

Results files are append-only. Do not edit anyone else's.

## Add or correct a method

- An adapter must use only what the service publicly documents, return a `Result`, and classify failures into short names (see `harness/adapters.py`). Add a test for any parsing you write.
- If you maintain a service that is tested here and you think its adapter is unfair, open an issue or send a fix with a link to your documentation. We will merge it and re-run.
- Do not add a method that needs a private endpoint, scraping a vendor's website, or paid access we cannot all reproduce.

## Rules that keep the numbers honest

- The video sample is frozen. Changes to `videos.csv` mean a new numbered version of the sample, announced in the pull request, never an edit in place.
- No transcript text is stored or published. Results keep lengths and error classes only.
- Keep the request rate low. Do not add concurrency or remove the pause between requests.
- No instructions for defeating YouTube's protections. The benchmark measures what happens, it does not teach evasion.
