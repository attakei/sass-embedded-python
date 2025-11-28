"""sass-embedded is Dart Sass bindings for Python."""

__version__ = "0.1.3"

from .simple import compile_directory, compile_file, compile_string
# from .protocol.compiler import Compiler  # TODO: Uncomment when Compiler is complete

__all__ = ["compile_directory", "compile_file", "compile_string"]  # , "Compiler"]