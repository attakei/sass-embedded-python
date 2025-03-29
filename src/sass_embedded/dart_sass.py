"""Controller of Dart Sass."""

from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from . import __dart_sass_version__, package_root

if TYPE_CHECKING:
    from pathlib import Path

OS_NAME = Literal["android", "linux", "macos", "windows"]
ARCH_NAME = Literal["arm", "arm64", "ia32", "riscv64", "x64"]


def resolve_os() -> OS_NAME:
    """Retrieve os name as dart-sass specified."""
    os_name = platform.system()
    if os_name == "Darwin":
        return "macos"
    if os_name in ("Linux", "Windows", "Android"):
        return os_name.lower()  # type: ignore[return-value]
    raise Exception(f"There is not dart-sass binary for {os_name}")


def resolve_arch() -> ARCH_NAME:
    """Retrieve cpu architecture string as dart-sass specified."""
    # NOTE: This logic is not all covered.
    arch_name = platform.machine()
    if arch_name in ("x86_64", "AMD64"):
        arch_name = "x64"
    if arch_name.startswith("arm") and arch_name != "arm64":
        arch_name = "arm"
    return arch_name  # type: ignore[return-value]


@dataclass
class Release:
    os: OS_NAME
    arch: ARCH_NAME
    version: str = __dart_sass_version__

    @property
    def fullname(self) -> str:
        return f"{self.version}-{self.os}-{self.arch}"

    @classmethod
    def init(cls) -> Release:
        os_name = resolve_os()
        arch_name = resolve_arch()
        return cls(os=os_name, arch=arch_name)

    def resolve_dir(self, base_dir: Path):
        return base_dir / self.fullname


def resolve_bin_base_dir() -> Path:
    """Retrieve base directory to install Dart Sass binaries."""
    return package_root / "dart-sass"
