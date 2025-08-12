"""Download & preprocess with yt-dlp + ffmpeg (stubbed)."""
from __future__ import annotations
import argparse, logging, json, os, pathlib, subprocess
from typing import List, Dict, Any
from common import setup_logging, config

log = logging.getLogger("download")

def preprocess(url: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    # Stub: instead of downloading, create a placeholder file
    out_path = os.path.join(out_dir, "clip_placeholder.mp4")
    with open(out_path, "wb") as f:
        f.write(b"")
    log.info("Pretended to download %s -> %s", url, out_path)
    return out_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default=os.path.join(config.DATA_DIR, "clip_candidates.json"))
    parser.add_argument("--out-dir", default=os.path.join(config.OUTPUT_DIR, "clips"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)

    cands = json.load(open(args.candidates)) if os.path.exists(args.candidates) else []
    for c in cands:
        preprocess(c["url"], args.out_dir)

if __name__ == "__main__":
    main()
