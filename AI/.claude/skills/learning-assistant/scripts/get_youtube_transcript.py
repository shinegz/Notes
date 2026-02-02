#!/usr/bin/env python3
"""
Fetch transcript/captions from a YouTube video for use with learning-assistant.
Requires: pip install youtube-transcript-api
Usage: python get_youtube_transcript.py <youtube_url_or_video_id>
Output: Plain text transcript to stdout; errors to stderr.
"""

import re
import sys


def extract_video_id(url_or_id: str) -> str | None:
    """Extract YouTube video ID from URL or return as-is if already an ID."""
    # Standard watch URL
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url_or_id)
    if m:
        return m.group(1)
    # Assume 11-char alphanumeric is video ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id.strip()):
        return url_or_id.strip()
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: get_youtube_transcript.py <youtube_url_or_video_id>", file=sys.stderr)
        return 1

    video_id = extract_video_id(sys.argv[1])
    if not video_id:
        print("Error: could not parse YouTube URL or video ID", file=sys.stderr)
        return 1

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Error: youtube-transcript-api not installed. Run: pip install youtube-transcript-api", file=sys.stderr)
        return 1

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        return 1

    for entry in transcript_list:
        text = entry.get("text", "").strip()
        if text:
            print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
