"""Concatenate downloaded clips up to ~60 seconds with simple title card, then auto-open the output folder."""
from __future__ import annotations
import argparse, logging, os, glob, subprocess, sys
from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from common import setup_logging, config

log = logging.getLogger("edit_video")


def _open_folder(path: str) -> None:
    folder = os.path.abspath(os.path.dirname(path))
    try:
        if sys.platform.startswith("darwin"):
            subprocess.Popen(["open", folder])
        elif os.name == "nt":
            os.startfile(folder)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", folder])
        log.info("Opened folder: %s", folder)
    except Exception as e:
        log.warning("Could not open folder automatically: %s", e)


def assemble(clips_dir: str, out_path: str, target_seconds: int = 60) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    files = sorted(glob.glob(os.path.join(clips_dir, "*.mp4")))
    if not files:
        raise SystemExit("No clips found. Run clip_finder/download.py first.")

    chosen: List[VideoFileClip] = []
    total = 0
    for f in files:
        clip = VideoFileClip(f)
        take = min(clip.duration, 12)  # take up to 12s per clip
        sub = clip.subclip(0, take)
        chosen.append(sub)
        total += take
        if total >= target_seconds:
            break

    body = concatenate_videoclips(chosen, method="compose")

    # Simple title card
    title = TextClip("Top Football Highlights", fontsize=70, color="white").set_duration(2)
    title = title.on_color(size=(body.w, body.h), color=(0, 0, 0), pos="center", col_opacity=0.7)
    final = concatenate_videoclips([title, body], method="compose")
    final.write_videofile(out_path, codec="libx264", audio_codec="aac", fps=30, threads=4, verbose=False, logger=None)

    # Close clips to release resources
    for c in chosen:
        c.close()
    body.close()
    final.close()
    log.info("Created edited video at %s", out_path)
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips-dir", default=os.path.join(config.OUTPUT_DIR, "clips"))
    parser.add_argument("--out", default=os.path.join(config.OUTPUT_DIR, "edits", "edit_master.mp4"))
    parser.add_argument("--target-seconds", type=int, default=60)
    parser.add_argument("--open", dest="open_folder", action="store_true", default=True, help="Open output folder when done (default)")
    parser.add_argument("--no-open", dest="open_folder", action="store_false", help="Do not open folder")
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    out_path = assemble(args.clips_dir, args.out, args.target_seconds)
    if args.open_folder:
        _open_folder(out_path)


if __name__ == "__main__":
    main()
