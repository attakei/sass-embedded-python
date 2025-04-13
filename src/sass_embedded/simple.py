"""Simple interface using Dart Sass.

This module to work Dart Sass by same process of command line interface.

Finally, this provides all features of `Dart Sass CLI`_ excluded something.

.. note:: This will not provide full-featured JavaScript API because it is to wrap CLI.

.. _Dart Sass CLI: https://sass-lang.com/documentation/cli/dart-sass/
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generic, Literal, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

from .dart_sass import Executable, Release

T = TypeVar("T")

Syntax = Literal["scss", "sass", "css"]
OutputStyle = Literal["expanded", "compressed"]
SourceMapStyle = Literal["refer", "embed"]
SourceMapUrl = Literal["relative", "absolute"]

logger = logging.getLogger(__name__)


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

    def get_arguments(self, use_stdout: bool) -> list[str]:
        args = [] if use_stdout else [f"--source-map-urls={self.source_url}"]
        if self.style == "embed":
            args.append("--embed-source-map")
        if self.source_embed:
            args.append("--embed-sources")
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
        if not self.sourcemap_options:
            args.append("--no-source-map")
            return args
        return args + self.sourcemap_options.get_arguments(use_stdout)


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


@dataclass
class Result(Generic[T]):
    ok: bool
    error: Optional[str] = None
    options: Optional[CompileOptions] = None
    output: Optional[T] = None


def compile_string(
    source: str,
    syntax: Syntax = "scss",
    load_paths: Optional[list[Path]] = None,
    style: OutputStyle = "expanded",
    embed_sourcemap: bool = False,
    embed_sources: bool = False,
) -> Result[str]:
    """Convert from Sass/SCSS source to CSS.

    :param srouce: Source text. It must be format for Sass or SCSS.
    :param syntax: Source format.
    :param load_paths: List of addtional load path for Sass compile.
    :param style: Output style.
    :param embed_sourcemap: Flag to embed source-map into output.
    :param embed_sources: Flag to embed sources into output. It works only when ``embed_sourcemap`` is ``True``.
    """
    sourcemap_options = None
    if embed_sourcemap:
        sourcemap_options = SourceMapOptions(style="embed", source_embed=embed_sources)
    elif embed_sources:
        logger.warning("'embed_sourcemap' should be True when 'embed_sources' is True.")
    options = CompileOptions(
        load_paths or [], style, sourcemap_options=sourcemap_options
    )
    cli = CLI(options)
    proc = subprocess.run(
        cli.command_with_stdin(syntax),
        input=source,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return Result(False, error=proc.stderr, options=options)
    return Result(True, options=options, output=proc.stdout)


def compile_file(
    source: Path,
    dest: Path,
    load_paths: Optional[list[Path]] = None,
    style: OutputStyle = "expanded",
    no_sourcemap: bool = False,
    embed_sourcemap: bool = False,
    embed_sources: bool = False,
    source_urls: SourceMapUrl = "relative",
) -> Result[Path]:
    """Convert from Sass/SCSS source to CSS.

    :param source: Source path. It must have extension ``.sass``, ``.scss`` or ``.css``.
    :param dest: Output destination.
    :param load_paths: List of addtional load path for Sass compile.
    :param style: Output style.
    :param no_sourcemap: Flag to skip generating source-map.
    :param embed_sourcemap: Flag to embed source-map into output.
    :param embed_sources: Flag to embed sources into output.
    :param source_urls: Style for refer to sources on source-map.
    """
    source = Path(source)
    dest = Path(dest)
    sourcemap_options = (
        None
        if no_sourcemap
        else SourceMapOptions(
            style="embed" if embed_sourcemap else "refer",
            source_embed=embed_sources,
            source_url=source_urls,
        )
    )
    options = CompileOptions(load_paths or [], style, sourcemap_options)
    cli = CLI(options)
    proc = subprocess.run(
        cli.command_with_path(source, dest), capture_output=True, text=True
    )
    if proc.returncode != 0:
        return Result(False, error=proc.stdout + proc.stderr, options=options)
    return Result(True, options=options, output=dest)


def compile_directory(
    source: Path,
    dest: Path,
    load_paths: Optional[list[Path]] = None,
    style: OutputStyle = "expanded",
    no_sourcemap: bool = False,
    embed_sourcemap: bool = False,
    embed_sources: bool = False,
    source_urls: SourceMapUrl = "relative",
) -> Result[list[Path]]:
    """Compile all source files on specified directory.

    This use Many-to-Many Mode of Dart Sass CLI.

    See https://sass-lang.com/documentation/cli/dart-sass/#many-to-many-mode

    :param source: Source path. It must have extension ``.sass``, ``.scss`` or ``.css``.
    :param dest: Output destination.
    :param load_paths: List of addtional load path for Sass compile.
    :param style: Output style.
    :param no_sourcemap: Flag to skip generating source-maps.
    :param embed_sourcemap: Flag to embed source-map into output.
    :param embed_sources: Flag to embed sources into output.
    :param source_urls: Style for refer to sources on source-maps.
    """
    sourcemap_options = (
        None
        if no_sourcemap
        else SourceMapOptions(
            style="embed" if embed_sourcemap else "refer",
            source_embed=embed_sources,
            source_url=source_urls,
        )
    )
    options = CompileOptions(load_paths or [], style, sourcemap_options)
    cli = CLI(options)
    proc = subprocess.run(
        cli.command_with_path(source, dest), capture_output=True, text=True
    )
    if proc.returncode != 0:
        return Result(False, error=proc.stdout + proc.stderr, options=options)
    return Result(True, options=options, output=[p for p in Path(dest).glob("*.css")])
