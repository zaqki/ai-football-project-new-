"""Export 9:16, 1:1, 16:9 variants with ffmpeg (stub)."""
from __future__ import annotations
import argparse, logging, os, shutil
from common import setup_logging, config

log = logging.getLogger("export_variants")

def export_variants(input_path: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for tag in ["9x16","1x1","16x9"]:
        out = os.path.join(out_dir, f"video_{tag}.mp4")
        open(out, "wb").write(b"")  # placeholder
        log.info("Exported %s", out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=os.path.join(config.OUTPUT_DIR, "edits", "edit_master.mp4"))
    parser.add_argument("--out-dir", default=os.path.join(config.OUTPUT_DIR, "variants"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    export_variants(args.input, args.out_dir)

if __name__ == "__main__":
    main()
