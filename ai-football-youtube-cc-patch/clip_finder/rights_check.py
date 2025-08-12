"""Heuristic rights/risk checks (stub)."""
from __future__ import annotations
import argparse, logging, json, os
from typing import Dict, Any, List
from common import setup_logging, config

log = logging.getLogger("rights_check")

def assess(candidate: Dict[str, Any]) -> str:
    # Very simple heuristic placeholder
    src = candidate.get("url","")
    if "official" in src:
        return "skip_high_risk"
    return "ok"

def run(candidates_path: str) -> List[Dict[str, Any]]:
    cands = json.load(open(candidates_path))
    filtered = [c for c in cands if assess(c) == "ok"]
    log.info("Filtered %d -> %d candidates", len(cands), len(filtered))
    return filtered

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default=os.path.join(config.DATA_DIR, "clip_candidates.json"))
    parser.add_argument("--out", default=os.path.join(config.DATA_DIR, "clip_candidates_ok.json"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)

    filtered = run(args.candidates)
    json.dump(filtered, open(args.out, "w"), indent=2)
    log.info("Saved %s", args.out)

if __name__ == "__main__":
    main()
