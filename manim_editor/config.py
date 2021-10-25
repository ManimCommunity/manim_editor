import os
from typing import Any


class Config:
    # don't use this in an online environment, it invalidates all sessions when restarting
    SECRET_KEY = os.urandom(16)
    # one of: quiet, panic, fatal, error, warning, info, verbose, debug, trace
    FFMPEG_LOGLEVEL = "error"

    @staticmethod
    def set(key: str, value: Any):
        if getattr(Config, key) is None:
            raise ValueError(f"Key '{key}' doesn't exist in config")
        setattr(Config, key, value)
