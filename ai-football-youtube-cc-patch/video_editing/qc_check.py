"""Basic QC checks (stub)."""
from __future__ import annotations
import argparse, logging, os, json
from typing import Dict
from common import setup_logging, config

log = logging.getLogger("qc_check")

def qc(directory: str) -> Dict[str, str]:
    results = {}
    for f in os.listdir(directory):
        if f.endswith(".mp4"):
            results[f] = "ok"
    log.info("QC results: %s", results)
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=os.path.join(config.OUTPUT_DIR, "variants"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    qc(args.dir)

if __name__ == "__main__":
    main()
