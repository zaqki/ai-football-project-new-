
"""Search YouTube for Creative Commons football clips per player query."""
from __future__ import annotations
import argparse, logging, json, os, time
from typing import List, Dict, Any
from googleapiclient.discovery import build
from common import setup_logging, config

log = logging.getLogger("search_clips")

def build_queries(shortlist_path: str) -> List[str]:
    players = json.load(open(shortlist_path))
    # Example queries: "Alexander Isak goals 2024", "Bukayo Saka skills 2024"
    queries = []
    for p in players:
        name = p.get("player") or p.get("name")
        if not name: 
            continue
        queries += [f"{name} goals", f"{name} skills", f"{name} highlights"]
    # De-dup while preserving order
    seen=set(); unique=[q for q in queries if not (q in seen or seen.add(q))]
    log.info("Built %d queries", len(unique))
    return unique

def youtube_search(api_key: str, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    yt = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
    resp = yt.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video",
        videoLicense="creativeCommon",  # CC only to reduce rights risk
        safeSearch="none"
    ).execute()
    items = resp.get("items", [])
    results = []
    for it in items:
        vid = it["id"]["videoId"]
        snippet = it["snippet"]
        results.append({
            "video_id": vid,
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "publishedAt": snippet.get("publishedAt"),
            "query": query
        })
    return results

def enrich_durations(api_key: str, items: List[Dict[str, Any]]) -> None:
    if not items: return
    yt = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
    # batch by 50
    for i in range(0, len(items), 50):
        batch = items[i:i+50]
        ids = ",".join(x["video_id"] for x in batch)
        resp = yt.videos().list(part="contentDetails,statistics", id=ids).execute()
        dur_map = {it["id"]: it["contentDetails"]["duration"] for it in resp.get("items",[])}
        for x in batch:
            x["duration_iso8601"] = dur_map.get(x["video_id"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", default=os.path.join(config.DATA_DIR, "shortlist.json"))
    parser.add_argument("--out", default=os.path.join(config.DATA_DIR, "clip_candidates.json"))
    parser.add_argument("--max-per-query", type=int, default=5)
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)

    if not config.YT_API_KEY:
        raise SystemExit("Missing YT_API_KEY. Set env var or put it in .env")

    queries = build_queries(args.shortlist)
    all_items: List[Dict[str, Any]] = []
    for q in queries:
        try:
            items = youtube_search(config.YT_API_KEY, q, max_results=args.max_per_query)
            all_items.extend(items)
            time.sleep(0.2)  # be polite
        except Exception as e:
            log.warning("Search failed for '%s': %s", q, e)
    enrich_durations(config.YT_API_KEY, all_items)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(all_items, open(args.out, "w"), indent=2)
    log.info("Saved %s with %d candidates", args.out, len(all_items))

if __name__ == "__main__":
    main()
