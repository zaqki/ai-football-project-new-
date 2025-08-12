"""Rank players via performance metrics + report sentiment."""
from __future__ import annotations
import argparse, logging, json, os, random
from typing import Dict, Any, List
from common import setup_logging, config

log = logging.getLogger("scouting_agent")

def rank_players(normalized_path: str) -> List[Dict[str, Any]]:
    with open(normalized_path, "r") as f:
        data = json.load(f)
    # TODO: Use real metrics; here we stub
    shortlist = [
        {"player":"Alexander Isak","team":"Newcastle","score": random.uniform(0.7, 0.95)},
        {"player":"Bukayo Saka","team":"Arsenal","score": random.uniform(0.7, 0.95)},
    ]
    shortlist.sort(key=lambda x: x["score"], reverse=True)
    log.info("Built shortlist of %d players", len(shortlist))
    return shortlist

def save_shortlist(shortlist: List[Dict[str, Any]], name: str = "shortlist") -> str:
    os.makedirs(config.DATA_DIR, exist_ok=True)
    path = os.path.join(config.DATA_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(shortlist, f, indent=2)
    log.info("Saved %s", path)
    return path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalized", default=os.path.join(config.DATA_DIR, "normalized.json"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    sl = rank_players(args.normalized)
    save_shortlist(sl)

if __name__ == "__main__":
    main()
