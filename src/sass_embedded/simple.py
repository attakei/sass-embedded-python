"""Simple interface using Dart Sass."""

from __future__ import annotations

import subprocess
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
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
