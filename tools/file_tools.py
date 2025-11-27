# tools/file_tools.py
from pathlib import Path
from typing import Union

from config import WORKSPACE_ROOT


def ensure_workspace_subpath(relative_path: Union[str, Path]) -> Path:
    """
    Resolve a path under WORKSPACE_ROOT to prevent path traversal.
    """
    base = WORKSPACE_ROOT
    target = base / Path(relative_path)
    target = target.resolve()
    if not str(target).startswith(str(base.resolve())):
        raise ValueError("Unsafe path detected.")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def create_file(relative_path: Union[str, Path], content: str = "") -> None:
    """
    Create a new file under workspace with optional initial content.
    """
    target = ensure_workspace_subpath(relative_path)
    if not target.exists():
        target.write_text(content, encoding="utf-8")
    else:
        # Overwrite behavior can be adjusted if needed.
        target.write_text(content, encoding="utf-8")


def append_to_file(relative_path: Union[str, Path], content: str) -> None:
    """
    Append content to a file.
    """
    target = ensure_workspace_subpath(relative_path)
    with target.open("a", encoding="utf-8") as f:
        f.write(content)


def read_file(relative_path: Union[str, Path]) -> str:
    """
    Read a file content under workspace.
    """
    target = ensure_workspace_subpath(relative_path)
    if not target.exists():
        raise FileNotFoundError(f"File not found: {relative_path}")
    return target.read_text(encoding="utf-8")

