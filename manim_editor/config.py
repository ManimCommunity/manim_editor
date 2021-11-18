import json
import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent.absolute()


class Config:
    # NOTE: don't use this in an online environment, it invalidates all sessions when restarting
    SECRET_KEY = os.urandom(16)
    # one of: quiet, panic, fatal, error, warning, info, verbose, debug, trace
    FFMPEG_LOGLEVEL = "error"
    # protect user from scanning entire system when run in root
    RECURSION_DEPTH = 10

    ROOT_DIR = BASE_DIR
    STATIC_DIR = BASE_DIR / "app" / "static"

    VERSION = "v0.3.2"

    with open(BASE_DIR / "section_index.schema.json", "r") as file:
        SECTION_INDEX_SCHEMA = json.load(file)
    with open(BASE_DIR / "project.schema.json", "r") as file:
        PROJECT_SCHEMA = json.load(file)

    @staticmethod
    def set(key: str, value: Any):
        if getattr(Config, key) is None:
            raise ValueError(f"Key '{key}' doesn't exist in config")
        setattr(Config, key, value)
