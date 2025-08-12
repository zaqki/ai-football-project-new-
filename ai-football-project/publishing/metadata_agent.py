"""Generate titles, descriptions, hashtags (stubbed)."""
from __future__ import annotations
import argparse, logging, os, json
from common import setup_logging, config

log = logging.getLogger("metadata_agent")

def generate(video_dir: str) -> str:
    meta = {
        "title": "Top Finisher Alert: Alexander Isak 🔥",
        "description": "Insane finishing & movement. Like & subscribe for daily football shorts!",
        "hashtags": ["#football","#isak","#shorts","#tiktokfootball"]
    }
    out = os.path.join(config.DATA_DIR, "metadata.json")
    os.makedirs(config.DATA_DIR, exist_ok=True)
    json.dump(meta, open(out, "w"), indent=2)
    log.info("Saved %s", out)
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-dir", default=os.path.join(config.OUTPUT_DIR, "variants"))
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()
    setup_logging(args.log_level)
    generate(args.video_dir)

if __name__ == "__main__":
    main()
