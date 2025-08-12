"""Build search queries for clips, de-dup, quality filter (stubbed)."""
from __future__ import annotations
import argparse, logging, json, os
from typing import List, Dict, Any
from common import setup_logging, config

log = logging.getLogger("search_clips")

def build_queries(shortlist_path: str) -> List[str]:
    players = json.load(open(shortlist_path))
    queries = [f"{p['player']} best goals" for p in players]
    log.info("Built %d queries", len(queries))
    return queries

def search_sources(queries: List[str]) -> List[Dict[str, Any]]:
    # TODO: Use YouTube/TikTok APIs; stubbed
    results = [{"query": q, "url": "https://example.com/video", "quality":"1080p"} for q in queries]
    return results

def save_candidates(cands: List[Dict[str, Any]]) -> str:
    os.makedirs(config.DATA_DIR, exist_ok=True)
    path = os.path.join(config.DATA_DIR, "clip_candidates.json")
    json.dump(cands, open(path, "w"), indent=2)
    log.info("Saved %s", path)
    return path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", default=os.path.join(config.DATA_DIR, "shortlist.json"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    queries = build_queries(args.shortlist)
    cands = search_sources(queries)
    save_candidates(cands)

if __name__ == "__main__":
    main()
