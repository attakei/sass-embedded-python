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


def install(os_name: Optional[str] = None, arch_name: Optional[str] = None):
    """Install Dart Sass executable.

    :param os_name: Target OS of archives.
    :param arch_name: Target CPU architecture of archives.
    """
    if os_name and arch_name:
        release = Release(os=os_name, arch=arch_name)  # type: ignore[arg-type]
    else:
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
