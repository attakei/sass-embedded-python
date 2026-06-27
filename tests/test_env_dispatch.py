"""Env-dispatch coverage tests driven by EXPECTED_OS / EXPECTED_ARCH.

Skipped unless both env vars are set, so local pytest runs and the
existing ``test`` job in CI are unaffected. The ``env-coverage-test``
job in ``.github/workflows/main.yaml`` populates them per runner via
``matrix.include``.
"""

import os

import pytest

from sass_embedded import dart_sass as P
from sass_embedded._const import DART_SASS_VERSION
from sass_embedded.dart_sass.installer import install

EXPECTED_OS = os.environ.get("EXPECTED_OS")
EXPECTED_ARCH = os.environ.get("EXPECTED_ARCH")
EXPECTED_LIBC = os.environ.get("EXPECTED_LIBC")

pytestmark = pytest.mark.skipif(
    not (EXPECTED_OS and EXPECTED_ARCH),
    reason="EXPECTED_OS/EXPECTED_ARCH not set",
)


def _expected_libc_suffix() -> str:
    return "-musl" if EXPECTED_LIBC == "musl" else ""


def test_release_init_matches_runner():
    r = P.Release.init()
    assert r.os == EXPECTED_OS
    assert r.arch == EXPECTED_ARCH
    if EXPECTED_LIBC is not None:
        assert r.is_musl is (EXPECTED_LIBC == "musl")


def test_archive_url_encodes_target():
    r = P.Release.init()
    assert f"-{EXPECTED_OS}-{EXPECTED_ARCH}{_expected_libc_suffix()}." in r.archive_url


def test_binary_installation_for_runner():
    install()
    r = P.Release.init()
    bin_dir = r.resolve_dir(P.resolve_bin_base_dir())
    assert (
        bin_dir.name
        == f"{DART_SASS_VERSION}-{EXPECTED_OS}-{EXPECTED_ARCH}{_expected_libc_suffix()}"
    )
    e = r.get_executable()
    assert e.dart_vm_path.exists()
    assert e.sass_snapshot_path.exists()
