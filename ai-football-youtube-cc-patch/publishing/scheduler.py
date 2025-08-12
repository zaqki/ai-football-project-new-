"""Schedule & publish via APIs (stub)."""
from __future__ import annotations
import argparse, logging, os, json
from common import setup_logging, config

log = logging.getLogger("scheduler")

def schedule(variants_dir: str, metadata_path: str) -> None:
    log.info("Would schedule videos in %s with metadata %s (stub).", variants_dir, metadata_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants-dir", default=os.path.join(config.OUTPUT_DIR, "variants"))
    parser.add_argument("--metadata", default=os.path.join(config.DATA_DIR, "metadata.json"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    schedule(args.variants_dir, args.metadata)

if __name__ == "__main__":
    main()
