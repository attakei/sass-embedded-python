"""Simple interface using Dart Sass.

This module to work Dart Sass by same process of command line interface.

Finally, this provides all features of `Dart Sass CLI`_ excluded something.

.. _Dart Sass CLI: https://sass-lang.com/documentation/cli/dart-sass/
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from .dart_sass import Executable, Release

Syntax = Literal["scss", "sass", "css"]
OutputStyle = Literal["expanded", "compressed"]
SourceMapStyle = Literal["refer", "embed"]
SourceMapUrl = Literal["relative", "absolute"]


@dataclass
class SourceMapOptions:
    """Source-map option values to compile for Dart Sass CLI."""

    style: SourceMapStyle = "refer"
    """Generating format for source-map.

    :ref: https://sass-lang.com/documentation/cli/dart-sass/#embed-source-map
    """
    source_url: SourceMapUrl = "relative"
    """Refer style for URL of source-map.

    :ref: https://sass-lang.com/documentation/cli/dart-sass/#source-map-urls
    """
    source_embed: bool = False
    """Flag to inject sources into sourcemap.

    :ref: https://sass-lang.com/documentation/cli/dart-sass/#embed-sources
    """

    @property
    def as_arguments(self) -> list[str]:
        args = ["--source-map-urls=relative"]
        return args


@dataclass
class CompileOptions:
    """Compile option values for Dart Sass CLI."""

    paths: list[Path] = field(default_factory=list)
    """Path list of external modules.

    :ref: https://sass-lang.com/documentation/cli/dart-sass/#load-path
    """
    output_style: OutputStyle = "expanded"
    """Generating format for CSS.

    :ref: https://sass-lang.com/documentation/cli/dart-sass/#style
    """
    sourcemap_options: Optional[SourceMapOptions] = None
    """Generating options for source-map."""

    def get_cli_arguments(self, use_stdout: bool = False) -> list[str]:
        """Retrieve arguments collection to pass CLI.

        :param use_stdout: Set True when CLI write compile files into STDOUT.
        """
        args = [
            f"--style={self.output_style}",
        ] + [f"--load-path={p}" for p in self.paths]
        if use_stdout:
            # When use stdout to write compiled CSS, it cannot use source-map options.
            return args
        # Work arguments for source-map.
        if not self.sourcemap_options:
            return args
        return args + self.sourcemap_options.as_arguments


class CLI:
    """CLI controls."""

    exe: Executable
    options: CompileOptions

    def __init__(self, options: CompileOptions):
        self.exe = Release.init().get_executable()
        self.options = options

    def _command_base(self) -> list[str]:
        return [
            str(self.exe.dart_vm_path),
            str(self.exe.sass_snapshot_path),
        ]

    def command_with_path(self, source: Path, dest: Path) -> list[str]:
        return (
            self._command_base()
            + self.options.get_cli_arguments()
            + [f"{source}:{dest}"]
        )

    def command_with_stdin(self, syntax: Syntax) -> list[str]:
        opts = ["--stdin"]
        if syntax == "sass":
            opts.append("--indented")
        return self._command_base() + opts + self.options.get_cli_arguments(True)


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
    options = CompileOptions(load_paths or [], style)
    cli = CLI(options)
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
    options = CompileOptions(load_paths or [], style)
    cli = CLI(options)
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

    options = CompileOptions(load_paths or [], style)
    cli = CLI(options)
    proc = subprocess.run(
        cli.command_with_path(source, dest), capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise Exception(proc.stdout + proc.stderr)
    return [p for p in Path(dest).glob("*.css")]
