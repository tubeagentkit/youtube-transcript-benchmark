import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))

import adapters  # noqa: E402
import analyze  # noqa: E402


@pytest.mark.parametrize(
    "stderr,expected",
    [
        ("ERROR: [youtube] abc: Sign in to confirm you’re not a bot. Use --cookies", "bot_check"),
        ("ERROR: [youtube] abc: Sign in to confirm your age. Use --cookies-from-browser", "age_restricted"),
        ("ERROR: [youtube] abc: This video is unavailable", "unavailable"),
        ("ERROR: [youtube] abc: This video is not available", "unavailable"),
        ("ERROR: Unable to download: HTTP Error 429: Too Many Requests", "http_429"),
        ("ERROR: There are no subtitles for the requested languages", "no_subtitles"),
        ("something nobody has seen before", "other"),
    ],
)
def test_ytdlp_error_classification(stderr, expected):
    assert adapters.classify_ytdlp_error(stderr) == expected


def test_vtt_text_strips_headers_timings_and_tags():
    raw = "WEBVTT\nKind: captions\nLanguage: en\n\n00:00:01.000 --> 00:00:02.000\nHello <c>world</c>\n\n00:00:02.000 --> 00:00:03.000\nsecond line\n"
    assert adapters.vtt_text(raw) == "Hello world second line"


def test_block_errors_cover_the_blocks_of_both_tools():
    assert {"RequestBlocked", "IpBlocked", "bot_check", "http_429"} <= adapters.BLOCK_ERRORS


def test_percentile_nearest_rank():
    assert analyze.percentile([], 50) is None
    assert analyze.percentile([100], 95) == 100
    assert analyze.percentile([10, 20, 30, 40], 50) == 20
    assert analyze.percentile([10, 20, 30, 40], 95) == 40


def row(method, cell="en_manual_short", ok=True, attempted=True, error="", ms=100, caption_kind="manual", **extra):
    return {"date": "2026-10-17", "env": "test", "method": method, "video_id": "x", "cell": cell, "language": "en",
            "caption_kind": caption_kind, "attempted": attempted, "ok": ok, "error": error, "ms": ms, "versions": {}, **extra}


def test_skipped_requests_are_not_counted_as_failures_or_successes():
    rows = [row("ytapi", ok=True), row("ytapi", ok=False, error="RequestBlocked"),
            row("ytapi", attempted=False, ok=False, error="not_attempted_after_blocks")]
    table = analyze.headline_table(rows)
    assert "50% (1/2)" in table  # 1 success of 2 attempted
    assert "| 1 |" in table  # one not attempted


def test_edge_cases_do_not_enter_the_success_rate():
    rows = [row("ytapi", ok=True), row("ytapi", cell="no_captions", ok=False, error="TranscriptsDisabled", caption_kind="none")]
    assert "100% (1/1)" in analyze.headline_table(rows)
    assert "TranscriptsDisabled: 1" in analyze.edge_table(rows)


def test_cached_responses_are_left_out_of_latency_and_reported():
    rows = [row("gyt", ms=4, cached=True), row("gyt", ms=800, cached=False), row("gyt", ms=900, cached=False)]
    table = analyze.headline_table(rows)
    assert "800 ms" in table and "1 of 3 successes were served from cache" in table


def test_every_results_file_is_valid_json_lines():
    for path in (ROOT / "results").glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                json.loads(line)


def test_superseded_runs_get_their_own_section(tmp_path):
    current = {**row("ytapi"), "_file": "2026-10-18-home", "_superseded": False}
    old = {**row("ytapi", ok=False, error="NoTranscriptFound"), "_file": "2026-10-17-home-run1-superseded", "_superseded": True}
    text = analyze.block([current, old])
    assert "## Earlier runs, superseded" in text
    assert text.index("2026-10-18-home") < text.index("## Earlier runs, superseded") < text.index("run1-superseded")


class FakeTrack:
    def __init__(self, code, generated):
        self.language_code, self.is_generated = code, generated


def test_pick_track_matches_regional_variants_and_prefers_manual():
    tracks = [FakeTrack("bn", True), FakeTrack("en-US", True), FakeTrack("en-GB", False)]
    assert adapters.pick_track(tracks, "en").language_code == "en-GB"
    assert adapters.pick_track([FakeTrack("en-US", True)], "en").language_code == "en-US"
    assert adapters.pick_track(tracks, "es") is None


def test_ytdlp_command_enables_node_when_available(monkeypatch):
    monkeypatch.setattr(adapters.shutil, "which", lambda name: "/usr/bin/node" if name == "node" else None)
    cmd = adapters.ytdlp_command("abc", "en", "/tmp/%(id)s.%(ext)s")
    assert cmd[:3] == ["yt-dlp", "--js-runtimes", "node"]
    assert cmd[-1].endswith("watch?v=abc") and "--write-auto-subs" in cmd


def test_ytdlp_command_without_node_has_no_runtime_flag(monkeypatch):
    monkeypatch.setattr(adapters.shutil, "which", lambda name: None)
    assert "--js-runtimes" not in adapters.ytdlp_command("abc", "en", "/tmp/x")
