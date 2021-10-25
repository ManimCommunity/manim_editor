import subprocess
from typing import List, Optional, Tuple

from .config import get_config


def capture(command: List[str],
            cwd: Optional[str] = None,
            command_input: Optional[str] = None) -> Tuple[str, str, int]:
    """Run command and capture standard output, standard error and return code."""
    p = subprocess.run(command, cwd=cwd, input=command_input, capture_output=True, text=True)
    out, err = p.stdout, p.stderr
    return out, err, p.returncode


def capture_ffmpeg(params: List[str]) -> Tuple[str, str, int]:
    """Run ffmpeg with params and capture standard output, standard error and return code."""
    return capture(["ffmpeg"] + params)


def run_ffmpeg(params: List[str]) -> bool:
    """Run ffmpeg with params, print output to terminal and return true at success."""
    return subprocess.call(["ffmpeg"] + params + ["-loglevel", get_config().FFMPEG_LOGLEVEL]) == 0
