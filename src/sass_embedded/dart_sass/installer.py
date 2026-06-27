"""Installation proc.

It works to fetch release archive from GitHub
and install into library directory.
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.request import urlopen

from . import Release, resolve_bin_base_dir

if TYPE_CHECKING:
    from typing import Optional

logger = logging.getLogger(__name__)


def clean():
    """Clean up all executables."""
    logger.info("Clean up executables.")
    shutil.rmtree(resolve_bin_base_dir(), ignore_errors=True)


def install(
    os_name: Optional[str] = None,
    arch_name: Optional[str] = None,
    is_musl: Optional[bool] = None,
):
    """Install Dart Sass executable.

    :param os_name: Target OS of archives.
    :param arch_name: Target CPU architecture of archives.
    :param is_musl: Force musl variant on or off (Linux only).
    """
    base = Release.init()
    target_os = os_name or base.os
    target_arch = arch_name or base.arch
    target_musl = (
        is_musl
        if is_musl is not None
        else (base.is_musl if target_os == base.os else False)
    )
    release = Release(
        os=target_os,  # type: ignore[arg-type]
        arch=target_arch,  # type: ignore[arg-type]
        is_musl=target_musl,
    )
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
