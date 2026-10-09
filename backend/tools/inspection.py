"""Read-only project inspection tools bounded to a requested directory."""

from pathlib import Path
import subprocess


def inspect_project(directory: str) -> dict:
    path = Path(directory).expanduser().resolve()
    if not path.is_dir():
        return {"success": False, "message": f"Not a directory: {path}"}
    files = [str(item.relative_to(path)) for item in path.rglob("*") if item.is_file()][:200]
    return {"success": True, "path": str(path), "files": files, "message": f"Found {len(files)} files."}


def read_file(path: str, max_bytes: int = 100_000) -> dict:
    target = Path(path).expanduser().resolve()
    if not target.is_file():
        return {"success": False, "message": f"Not a file: {target}"}
    try:
        content = target.read_text(encoding="utf-8", errors="replace")[:max_bytes]
        return {"success": True, "path": str(target), "content": content, "message": f"Read {target}."}
    except OSError as error:
        return {"success": False, "message": f"Could not read file: {error}"}


def git_status(directory: str) -> dict:
    path = Path(directory).expanduser().resolve()
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=path, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"success": False, "message": f"Could not inspect Git status: {error}"}
    if result.returncode:
        return {"success": False, "message": result.stderr.strip() or "Not a Git repository."}
    return {"success": True, "status": result.stdout, "message": "Git status inspected."}
