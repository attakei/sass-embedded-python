"""Simple interface using Dart Sass."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from .dart_sass import Release

Syntax = Literal["scss", "sass", "css"]


def compile_string(
    source: str, syntax: Syntax = "scss", load_paths: Optional[list[Path]] = None
) -> str:
    """Convert from Sass/SCSS source to CSS."""
    exe = Release.init().get_executable()
    cmd = [
        str(exe.dart_vm_path),
        str(exe.sass_snapshot_path),
        "--stdin",
    ]
    if syntax == "sass":
        cmd.append("--indented")
    if load_paths:
        cmd += [f"--load-path={p}" for p in load_paths]
    proc = subprocess.run(
        cmd,
        input=source,
        text=True,
        capture_output=True,
    )
    return proc.stdout


def compile_file(
    source: Path,
    dest: Path,
    syntax: Syntax = "scss",
    load_paths: Optional[list[Path]] = None,
) -> Path:
    """Convert from Sass/SCSS source to CSS."""
    exe = Release.init().get_executable()
    cmd = [
        str(exe.dart_vm_path),
        str(exe.sass_snapshot_path),
        str(source),
        str(dest),
    ]
    if syntax == "sass":
        cmd.append("--indented")
    if load_paths:
        cmd += [f"--load-path={p}" for p in load_paths]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise Exception(proc.stdout + proc.stderr)
    return Path(dest)
