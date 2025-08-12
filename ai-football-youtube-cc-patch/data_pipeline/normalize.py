"""Normalize raw events & ratings, harmonise IDs."""
from __future__ import annotations
import argparse, logging, json, os
from typing import Dict, Any
from common import setup_logging, config

log = logging.getLogger("normalize")

def normalize(raw_path: str, out_name: str = "normalized") -> str:
    with open(raw_path, "r") as f:
        raw = json.load(f)
    norm = {
        "fixtures": raw.get("fixtures", []),
        "reports": raw.get("reports", []),
        "ids_map": {"example": 1}
    }
    os.makedirs(config.DATA_DIR, exist_ok=True)
    out_path = os.path.join(config.DATA_DIR, f"{out_name}.json")
    with open(out_path, "w") as f:
        json.dump(norm, f, indent=2)
    log.info("Saved %s", out_path)
    return out_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default=os.path.join(config.DATA_DIR, "raw_ingest.json"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    normalize(args.raw)

if __name__ == "__main__":
    main()
