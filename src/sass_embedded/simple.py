"""Simple interface using Dart Sass."""

import subprocess
from typing import Literal

from .dart_sass import Release

Syntax = Literal["scss", "sass", "css"]


def compile_string(source: str, syntax: Syntax = "scss") -> str:
    """Convert from Sass/SCSS source to CSS."""
    exe = Release.init().get_executable()
    cmd = [
        str(exe.dart_vm_path),
        str(exe.sass_snapshot_path),
        "--stdin",
    ]
    if syntax == "sass":
        cmd.append("--indented")
    proc = subprocess.run(
        cmd,
        input=source,
        text=True,
        capture_output=True,
    )
    return proc.stdout
