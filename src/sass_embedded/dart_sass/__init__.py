"""Controller of Dart Sass."""

from __future__ import annotations

import logging
import platform
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal
from urllib.request import urlopen

from .. import __dart_sass_version__

if TYPE_CHECKING:
    pass

OS_NAME = Literal["android", "linux", "macos", "windows"]
ARCH_NAME = Literal["arm", "arm64", "ia32", "riscv64", "x64"]

logger = logging.getLogger(__name__)
here = Path(__file__).parent


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
    """Release data of Dart Sass.

    This class manages information about release pack Dart Sass.
    """

    os: OS_NAME
    arch: ARCH_NAME
    version: str = __dart_sass_version__

    @property
    def fullname(self) -> str:
        return f"{self.version}-{self.os}-{self.arch}"

    @property
    def archive_url(self) -> str:
        """Retrieve URL for archive of GitHub Releases."""
        ext = "zip" if self.os == "windows" else "tar.gz"
        return f"https://github.com/sass/dart-sass/releases/download/{self.version}/dart-sass-{self.version}-{self.os}-{self.arch}.{ext}"

    @property
    def archive_format(self) -> str:
        """String of ``shutil.unpack_archive``."""
        return "zip" if self.os == "windows" else "gztar"

    @classmethod
    def init(cls) -> Release:
        os_name = resolve_os()
        arch_name = resolve_arch()
        return cls(os=os_name, arch=arch_name)

    def resolve_dir(self, base_dir: Path):
        return base_dir / self.fullname

    def get_executable(self, base_dir: Path | None = None) -> Executable:
        base_dir = base_dir or resolve_bin_base_dir()
        return Executable(base_dir=base_dir, release=self)


@dataclass
class Executable:
    """Data for local files data of Dart Sass.

    This class manages filepath and more about unpacked Dart Sass.
    """

    base_dir: Path
    release: Release

    @property
    def dart_vm_path(self) -> Path:
        dir_ = self.release.resolve_dir(self.base_dir)
        ext_ = ".exe" if self.release.os == "windows" else ""
        return (dir_ / "dart-sass" / "src" / f"dart{ext_}").resolve()

    @property
    def sass_snapshot_path(self) -> Path:
        dir_ = self.release.resolve_dir(self.base_dir)
        return (dir_ / "dart-sass" / "src" / "sass.snapshot").resolve()


def resolve_bin_base_dir() -> Path:
    """Retrieve base directory to install Dart Sass binaries."""
    return here / "_ext"


def install():
    """Install Dart Sass binary for local machine."""
    release = Release.init()
    release_dir = release.resolve_dir(resolve_bin_base_dir())
    logging.debug(f"Find '{release_dir}'")
    if release_dir.exists() and (release_dir / "src").exists():
        logging.info("Dart Sass binary is already installed.")
        return
    logging.info("Fetching Dart Sass binary.")
    shutil.rmtree(release_dir, ignore_errors=True)
    # TODO: Add error handling if it needs.
    resp = urlopen(release.archive_url)
    archive_path = Path(tempfile.mktemp())
    archive_path.write_bytes(resp.read())
    shutil.unpack_archive(archive_path, release_dir, release.archive_format)
