"""Ingest fixtures, results, match reports."""
from __future__ import annotations
import argparse, logging, json, os
from typing import List, Dict, Any
from common import setup_logging, config

log = logging.getLogger("ingest")

def fetch_fixtures() -> List[Dict[str, Any]]:
    # TODO: Replace with real API calls
    log.info("Fetching fixtures (stub)...")
    return [{"league":"EPL","home":"Arsenal","away":"Spurs","date":"2025-08-10"}]

def fetch_match_reports() -> List[Dict[str, Any]]:
    # TODO: Scrape or API
    log.info("Fetching match reports (stub)...")
    return [{"match_id":"EPL-001","report_text":"Player X was outstanding; MOTM..." }]

def save_raw(data: Dict[str, Any], name: str) -> str:
    os.makedirs(config.DATA_DIR, exist_ok=True)
    path = os.path.join(config.DATA_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log.info("Saved %s", path)
    return path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    fixtures = fetch_fixtures()
    reports = fetch_match_reports()
    save_raw({"fixtures": fixtures, "reports": reports}, "raw_ingest")

if __name__ == "__main__":
    main()
