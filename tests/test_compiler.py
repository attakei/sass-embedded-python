import filecmp
import shutil
from pathlib import Path

import pytest

from sass_embedded.protocol.compiler import Compiler

here = Path(__file__).parent

targets = [
    d.name
    for d in (here / "test-basics").glob("*")
    if d.is_dir() and d.stem not in ["modules"]
]

class TestFor_compiler:
    def test_version_information(self):
        compiler = Compiler()
        version_info = compiler.get_version_info()
        assert "compiler_version" in version_info
        assert "protocol_version" in version_info
        assert "implementation_version" in version_info
        assert "implementation_name" in version_info


