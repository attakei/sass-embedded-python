"""Simple interface using Dart Sass.

This module to work Dart Sass by same process of command line interface.

Finally, this provides all features of `Dart Sass CLI`_ excluded something.

.. _Dart Sass CLI: https://sass-lang.com/documentation/cli/dart-sass/
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from .dart_sass import Executable, Release

Syntax = Literal["scss", "sass", "css"]
OutputStyle = Literal["expanded", "compressed"]


class CLI:
    """CLI controls."""

    exe: Executable
    paths: list[Path]
    style: OutputStyle

    def __init__(
        self,
        load_paths: Optional[list[Path]] = None,
        output_style: OutputStyle = "expanded",
    ):
        self.exe = Release.init().get_executable()
        self.paths = load_paths or []
        self.style = output_style

    def _command_base(self) -> list[str]:
        return [
            str(self.exe.dart_vm_path),
            str(self.exe.sass_snapshot_path),
            f"--style={self.style}",
        ] + [f"--load-path={p}" for p in self.paths]

    def command_with_path(self, source: Path, dest: Path) -> list[str]:
        return self._command_base() + [f"{source}:{dest}"]

    def command_with_stdin(self, syntax: Syntax) -> list[str]:
        opts = ["--stdin"]
        if syntax == "sass":
            opts.append("--indented")
        return self._command_base() + opts


def compile_string(
    source: str,
    syntax: Syntax = "scss",
    load_paths: Optional[list[Path]] = None,
    style: OutputStyle = "expanded",
) -> str:
    """Convert from Sass/SCSS source to CSS.

    :param srouce: Source text. It must be format for Sass or SCSS.
    :param syntax: Source format.
    :param load_paths: List of addtional load path for Sass compile.
    :param style: Output style.
    """
    cli = CLI(load_paths, style)
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
    style: OutputStyle = "expanded",
) -> Path:
    """Convert from Sass/SCSS source to CSS.

    :param source: Source path. It must have extension ``.sass``, ``.scss`` or ``.css``.
    :param dest: Output destination.
    :param load_paths: List of addtional load path for Sass compile.
    :param style: Output style.
    """
    cli = CLI(load_paths, style)
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
    style: OutputStyle = "expanded",
) -> list[Path]:
    """Compile all source files on specified directory.

    This use Many-to-Many Mode of Dart Sass CLI.

    See https://sass-lang.com/documentation/cli/dart-sass/#many-to-many-mode

    :param source: Source path. It must have extension ``.sass``, ``.scss`` or ``.css``.
    :param dest: Output destination.
    :param load_paths: List of addtional load path for Sass compile.
    :param style: Output style.
    """

    cli = CLI(load_paths, style)
    proc = subprocess.run(
        cli.command_with_path(source, dest), capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise Exception(proc.stdout + proc.stderr)
    return [p for p in Path(dest).glob("*.css")]
