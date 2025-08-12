"""Download Creative Commons candidates with yt-dlp, limit duration, and save to out/clips."""
from __future__ import annotations
import argparse, logging, json, os, subprocess, sys, re
from typing import Dict, Any, List
from common import setup_logging, config

log = logging.getLogger("download")

YOUTUBE_URL = "https://www.youtube.com/watch?v={id}"


def iso8601_to_seconds(iso: str) -> int:
    """Convert ISO 8601 duration (e.g., PT2M10S) to seconds."""
    if not iso:
        return 0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return 0
    hours = int(m.group(1) or 0)
    minutes = int(m.group(2) or 0)
    seconds = int(m.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def download_video(video_id: str, out_dir: str) -> str:
    url = YOUTUBE_URL.format(id=video_id)
    os.makedirs(out_dir, exist_ok=True)
    # Use yt-dlp to download best video+audio merged mp4
    out_tmpl = os.path.join(out_dir, f"{video_id}.%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bv*+ba/b",
        "-o", out_tmpl,
        "--merge-output-format", "mp4",
        url,
    ]
    subprocess.run(cmd, check=True)
    path = os.path.join(out_dir, f"{video_id}.mp4")
    if not os.path.exists(path):
        # Fallback: find any produced file
        for f in os.listdir(out_dir):
            if f.startswith(video_id + "."):
                path = os.path.join(out_dir, f)
                break
    log.info("Downloaded %s", path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default=os.path.join(config.DATA_DIR, "clip_candidates.json"))
    parser.add_argument("--out-dir", default=os.path.join(config.OUTPUT_DIR, "clips"))
    parser.add_argument("--max-duration", type=int, default=120, help="Skip clips longer than this (seconds)")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of downloads")
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)

    items: List[Dict[str, Any]] = json.load(open(args.candidates)) if os.path.exists(args.candidates) else []
    os.makedirs(args.out_dir, exist_ok=True)
    downloaded = 0
    for it in items:
        if downloaded >= args.limit:
            break
        vid = it.get("video_id")
        dur = iso8601_to_seconds(it.get("duration_iso8601"))
        if dur == 0 or dur > args.max_duration:
            continue
        try:
            download_video(vid, args.out_dir)
            downloaded += 1
        except subprocess.CalledProcessError as e:
            log.warning("yt-dlp failed for %s: %s", vid, e)
    log.info("Downloaded %d videos into %s", downloaded, args.out_dir)


if __name__ == "__main__":
    main()
