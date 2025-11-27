# tools/exec_tools.py
import subprocess
from pathlib import Path
from typing import Tuple, List

from config import WORKSPACE_ROOT


def run_command(command: List[str], timeout: int = 60) -> Tuple[int, str, str]:
    """
    Run a shell command under workspace directory.
    Returns (return_code, stdout, stderr).
    """
    proc = subprocess.Popen(
        command,
        cwd=str(WORKSPACE_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        return 1, stdout, "Command timed out."
    return proc.returncode, stdout, stderr

