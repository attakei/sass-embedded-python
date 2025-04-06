"""sass-embedded is Dart Sass bindings for Python."""

__version__ = "0.0.0"

from pathlib import Path

from .simple import compile_file, compile_string

package_root = Path(__file__).parent

__all__ = ["compile_file", "compile_string"]
