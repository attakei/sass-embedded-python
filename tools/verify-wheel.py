#!/usr/bin/env python
"""Verify an installed sass-embedded wheel ships a runnable Dart Sass binary.

Run after installing the wheel into a fresh virtualenv. Used by the
``verify-wheel`` job in ``.github/workflows/main.yaml``.
"""

from __future__ import annotations

import subprocess
import sys

import sass_embedded
from sass_embedded.dart_sass import Release


def main() -> int:
    print(f"Using: {sass_embedded.__file__}")
    executable = Release.init().get_executable()
    if not executable.dart_vm_path.exists():
        print(f"Missing: {executable.dart_vm_path}", file=sys.stderr)
        return 1
    if not executable.sass_snapshot_path.exists():
        print(f"Missing: {executable.sass_snapshot_path}", file=sys.stderr)
        return 1
    print(f"Binary OK: {executable.dart_vm_path}")
    subprocess.run([str(executable.dart_vm_path), "--version"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
