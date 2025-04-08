"""Controller of Dart Sass.

This module works to
"""

from __future__ import annotations

import logging
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from .._const import DART_SASS_VERSION

if TYPE_CHECKING:
    pass

OSName = Literal["android", "linux", "macos", "windows"]
ArchName = Literal["arm", "arm64", "ia32", "riscv64", "x64"]

logger = logging.getLogger(__name__)
here = Path(__file__).parent


def resolve_os() -> OSName:
    """Retrieve os name as dart-sass specified."""
    os_name = platform.system()
    if os_name == "Darwin":
        return "macos"
    if os_name in ("Linux", "Windows", "Android"):
        return os_name.lower()  # type: ignore[return-value]
    raise Exception(f"There is not dart-sass binary for {os_name}")


def resolve_arch() -> ArchName:
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
    """Release data of Dart Sass.

    This class manages information about release pack Dart Sass.
    """

    os: OSName
    """Identify of OS."""
    arch: ArchName
    """Identify of CPU architecture."""
    version: str = DART_SASS_VERSION
    """Versionstring of Dart Sass."""

    @property
    def fullname(self) -> str:
        """Full name of release's directory."""
        return f"{self.version}-{self.os}-{self.arch}"

    @property
    def archive_url(self) -> str:
        """URL for archive of GitHub Releases."""
        ext = "zip" if self.os == "windows" else "tar.gz"
        return f"https://github.com/sass/dart-sass/releases/download/{self.version}/dart-sass-{self.version}-{self.os}-{self.arch}.{ext}"

    @property
    def archive_format(self) -> str:
        """String of ``shutil.unpack_archive``."""
        return "zip" if self.os == "windows" else "gztar"

    @classmethod
    def init(cls) -> Release:
        """Create object with current environment and registered version."""
        os_name = resolve_os()
        arch_name = resolve_arch()
        return cls(os=os_name, arch=arch_name)

    def resolve_dir(self, base_dir: Path):
        """Retrieve full path of release's directory."""
        return base_dir / self.fullname

    def get_executable(self, base_dir: Path | None = None) -> Executable:
        """Retrieve executable components object."""
        base_dir = base_dir or resolve_bin_base_dir()
        return Executable(base_dir=base_dir, release=self)


@dataclass
class Executable:
    """Data for local files data of Dart Sass.

    This class manages filepath and more about unpacked Dart Sass.
    """

    base_dir: Path
    """Installed directory."""
    release: Release
    """Release information of installed components."""

    @property
    def dart_vm_path(self) -> Path:
        """Full path of Dart runtime."""
        dir_ = self.release.resolve_dir(self.base_dir)
        ext_ = ".exe" if self.release.os == "windows" else ""
        return (dir_ / "dart-sass" / "src" / f"dart{ext_}").resolve()

    @property
    def sass_snapshot_path(self) -> Path:
        """Full path of compiled module."""
        dir_ = self.release.resolve_dir(self.base_dir)
        return (dir_ / "dart-sass" / "src" / "sass.snapshot").resolve()


def resolve_bin_base_dir() -> Path:
    """Retrieve base directory to install Dart Sass binaries."""
    return here / "_ext"
