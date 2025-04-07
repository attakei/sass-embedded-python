"""Simple interface using Dart Sass."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from .dart_sass import Executable, Release

Syntax = Literal["scss", "sass", "css"]


class CLI:
    """CLI controls."""

    exe: Executable
    paths: list[Path]

    def __init__(
        self,
        load_paths: Optional[list[Path]] = None,
    ):
        self.exe = Release.init().get_executable()
        self.paths = load_paths or []

    def _command_base(self) -> list[str]:
        return [
            str(self.exe.dart_vm_path),
            str(self.exe.sass_snapshot_path),
        ] + [f"--load-path={p}" for p in self.paths]

    def command_with_path(self, source: Path, dest: Path) -> list[str]:
        return self._command_base() + [f"{source}:{dest}"]

    def command_with_stdin(self, syntax: Syntax) -> list[str]:
        opts = ["--stdin"]
        if syntax == "sass":
            opts.append("--indented")
        return self._command_base() + opts


def compile_string(
    source: str, syntax: Syntax = "scss", load_paths: Optional[list[Path]] = None
) -> str:
    """Convert from Sass/SCSS source to CSS."""
    cli = CLI(load_paths)
    proc = subprocess.run(
        cli.command_with_stdin(syntax),
        input=source,
        text=True,
        capture_output=True,
    )
    return proc.stdout


def compile_file(
    source: Path,
    dest: Path,
    load_paths: Optional[list[Path]] = None,
) -> Path:
    """Convert from Sass/SCSS source to CSS."""
    cli = CLI(load_paths)
    proc = subprocess.run(
        cli.command_with_path(source, dest), capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise Exception(proc.stdout + proc.stderr)
    return Path(dest)


def compile_directory(
    source: Path,
    dest: Path,
    load_paths: Optional[list[Path]] = None,
) -> list[Path]:
    """Compile all source files on specified directory.

    This use Many-to-Many Mode of Dart Sass CLI.

    See https://sass-lang.com/documentation/cli/dart-sass/#many-to-many-mode
    """

    cli = CLI(load_paths)
    proc = subprocess.run(
        cli.command_with_path(source, dest), capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise Exception(proc.stdout + proc.stderr)
    return [p for p in Path(dest).glob("*.css")]
