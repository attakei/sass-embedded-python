"""sass-embedded is Dart Sass bindings for Python."""

__version__ = "0.0.0"

from pathlib import Path

package_root = Path(__file__).parent

from .simple import compile_file, compile_string

__all__ = ["compile_file", "compile_string"]
