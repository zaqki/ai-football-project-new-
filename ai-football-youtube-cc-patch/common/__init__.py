"""
Common utilities for config, logging, and simple HTTP helpers.
Now supports loading a .env-style file if present.
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

def _load_dotenv():
    path = os.getenv("ENV_FILE", ".env")
    if os.path.exists(path):
        try:
            for line in open(path):
                line=line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k,v=line.split("=",1)
                os.environ.setdefault(k.strip(), v.strip())
        except Exception:
            pass

@dataclass
class Config:
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "out")
    YT_API_KEY: str = os.getenv("YT_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    @classmethod
    def from_env(cls) -> "Config":
        _load_dotenv()
        return cls(
            DATA_DIR=os.getenv("DATA_DIR", "data"),
            OUTPUT_DIR=os.getenv("OUTPUT_DIR", "out"),
            YT_API_KEY=os.getenv("YT_API_KEY", ""),
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", ""),
        )

    @classmethod
    def from_file(cls, path: str) -> "Config":
        _load_dotenv()
        if not os.path.exists(path):
            return cls.from_env()
        with open(path, "r") as f:
            data = json.load(f)
        base = cls.from_env().__dict__
        base.update(data)
        return cls(**base)

config = Config.from_env()
