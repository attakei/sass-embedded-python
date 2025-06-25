"""sass-embedded is Dart Sass bindings for Python."""

__version__ = "0.1.2"

from .simple import compile_directory, compile_file, compile_string

__all__ = ["compile_directory", "compile_file", "compile_string"]
