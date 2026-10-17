"""One adapter per method. Each takes a video ID and a language and returns a Result.

To add a method, write a function with the same signature, register it in ADAPTERS, and open a pull
request. An adapter must use only what the method documents publicly, and must classify failures into
the short error names listed in ERROR_NAMES instead of returning free text.
"""
import glob
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

MIN_CHARS = 20  # a result shorter than this does not count as a transcript
TIMEOUT_S = 90

BLOCK_ERRORS = {"RequestBlocked", "IpBlocked", "bot_check", "http_429"}


@dataclass
class Result:
    ok: bool
    error: str = ""
    chars: int = 0
    ms: int = 0
    extra: dict = field(default_factory=dict)


def _timed(fn):
    start = time.perf_counter()
    result = fn()
    result.ms = int((time.perf_counter() - start) * 1000)
    return result


# --- youtube-transcript-api -------------------------------------------------------------------------

def ytapi(video_id: str, language: str) -> Result:
    from youtube_transcript_api import YouTubeTranscriptApi

    def call():
        try:
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=[language])
            text = " ".join(snippet.text for snippet in fetched)
        except Exception as exc:  # classify by class name, never by message
            return Result(False, error=type(exc).__name__)
        return Result(len(text) >= MIN_CHARS, error="" if len(text) >= MIN_CHARS else "empty", chars=len(text))

    return _timed(call)


# --- yt-dlp -----------------------------------------------------------------------------------------

ERROR_PATTERNS = [  # checked in order against yt-dlp's stderr
    (re.compile(r"confirm you.re not a bot", re.I), "bot_check"),
    (re.compile(r"confirm your age", re.I), "age_restricted"),
    (re.compile(r"HTTP Error 429|Too Many Requests", re.I), "http_429"),
    (re.compile(r"Video unavailable|This video is (not available|unavailable)|Private video|has been removed", re.I), "unavailable"),
    (re.compile(r"no subtitles|There are no (automatic )?captions", re.I), "no_subtitles"),
]


def classify_ytdlp_error(stderr: str) -> str:
    for pattern, name in ERROR_PATTERNS:
        if pattern.search(stderr):
            return name
    return "other"


def vtt_text(raw: str) -> str:
    """Cue text from a WebVTT file, without headers, timings or tags."""
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or "-->" in line:
            continue
        lines.append(re.sub(r"<[^>]+>", "", line))
    return " ".join(lines)


def ytdlp(video_id: str, language: str) -> Result:
    def call():
        with tempfile.TemporaryDirectory() as tmp:
            cmd = [
                "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", language,
                "--sub-format", "vtt", "--no-warnings", "--no-progress", "-o", os.path.join(tmp, "%(id)s.%(ext)s"),
                f"https://www.youtube.com/watch?v={video_id}",
            ]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
            except subprocess.TimeoutExpired:
                return Result(False, error="timeout")
            files = glob.glob(os.path.join(tmp, "*.vtt"))
            if files:
                text = vtt_text(open(files[0], encoding="utf-8", errors="replace").read())
                return Result(len(text) >= MIN_CHARS, error="" if len(text) >= MIN_CHARS else "empty", chars=len(text))
            return Result(False, error=classify_ytdlp_error(proc.stderr) if proc.returncode else "no_subtitles")

    return _timed(call)


# --- GetYouTubeTranscript hosted API (documented public endpoint, used as a black box) ---------------

def gyt(video_id: str, language: str) -> Result:
    key = os.environ.get("GYT_API_KEY", "")
    query = urllib.parse.urlencode({"v": video_id, "language": language})
    request = urllib.request.Request(
        f"https://getyoutubetranscript.com/api/v1/transcript?{query}", headers={"x-api-key": key, "user-agent": "transcript-benchmark/1.0"}
    )

    def call():
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_S) as resp:
                body = json.load(resp)
        except urllib.error.HTTPError as exc:
            return Result(False, error=f"http_{exc.code}")
        except Exception as exc:
            return Result(False, error=type(exc).__name__)
        data = body.get("data") or {}
        text = data.get("transcript") or ""
        extra = {"cached": bool(data.get("cached")), "caption_type": data.get("caption_type", "")}
        return Result(len(text) >= MIN_CHARS, error="" if len(text) >= MIN_CHARS else "empty", chars=len(text), extra=extra)

    return _timed(call)


ADAPTERS = {"ytapi": ytapi, "ytdlp": ytdlp, "gyt": gyt}

LABELS = {
    "ytapi": "youtube-transcript-api (library)",
    "ytdlp": "yt-dlp (command line)",
    "gyt": "GetYouTubeTranscript (hosted API, run by this repo's maintainers)",
}
