import pytest

from sass_embedded._const import DART_SASS_VERSION
from sass_embedded import dart_sass as P


def test_relasename():
    r = P.Release("linux", "x64")
    assert r.fullname == f"{DART_SASS_VERSION}-linux-x64"
    bin_dir = r.resolve_dir(P.resolve_bin_base_dir())
    assert bin_dir.name == r.fullname
    assert bin_dir.parent.name == "_ext"


@pytest.mark.skipif('sys.platform != "linux"')
def test_linux_release_object():
    r = P.Release.init()
    assert r.os == "linux"
    e = r.get_executable(P.resolve_bin_base_dir())
    assert e.dart_vm_path.name == "dart"
    assert e.sass_snapshot_path.name == "sass.snapshot"


@pytest.mark.skipif('sys.platform != "darwin"')
def test_macos_release_object():
    r = P.Release.init()
    assert r.os == "macos"
    e = r.get_executable(P.resolve_bin_base_dir())
    assert e.dart_vm_path.name == "dart"
    assert e.sass_snapshot_path.name == "sass.snapshot"


@pytest.mark.skipif('sys.platform != "win32"')
def test_windows_release_object():
    r = P.Release.init()
    assert r.os == "windows"
    e = r.get_executable(P.resolve_bin_base_dir())
    assert e.dart_vm_path.name == "dart.exe"
    assert e.sass_snapshot_path.name == "sass.snapshot"
