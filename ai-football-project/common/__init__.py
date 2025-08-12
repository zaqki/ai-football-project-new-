"""
Common utilities for config, logging, and simple HTTP helpers.
"""
from __future__ import annotations
import logging
import os
import sys
import json
from dataclasses import dataclass
from typing import Any, Dict

def setup_logging(level: str = None) -> None:
    level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

@dataclass
class Config:
    # Minimal config; extend as needed
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "out")
    YT_API_KEY: str = os.getenv("YT_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    @classmethod
    def from_file(cls, path: str) -> "Config":
        if not os.path.exists(path):
            return cls()
        with open(path, "r") as f:
            data = json.load(f)
        return cls(**data)

config = Config()
