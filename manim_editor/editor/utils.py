from subprocess import run
from typing import List, Optional, Tuple


def capture(command: List[str],
            cwd: Optional[str] = None,
            command_input: Optional[str] = None) -> Tuple[str, str, int]:
    """Run command and capture standard output, standard error and return code."""
    p = run(command, cwd=cwd, input=command_input, capture_output=True, text=True)
    out, err = p.stdout, p.stderr
    return out, err, p.returncode


def run_ffmpeg(params: List[str]) -> Tuple[str, str, int]:
    """Run ffmpeg with params and capture standard output, standard error and return code."""
    return capture(["ffmpeg"] + params)
