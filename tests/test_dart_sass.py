import pytest

from sass_embedded import __dart_sass_version__
from sass_embedded import dart_sass as P


def test_relasename():
    r = P.Release("linux", "x64")
    assert r.fullname == f"{__dart_sass_version__}-linux-x64"
    bin_dir = r.resolve_dir(P.resolve_bin_base_dir())
    assert bin_dir.name == r.fullname
    assert bin_dir.parent.name == "dart-sass"


@pytest.mark.skipif('sys.platform != "linux"')
def test_linux_release_object():
    r = P.Release.init()
    assert r.os == "linux"
    e = r.executor(P.resolve_bin_base_dir())
    assert e.dart_vm_path.name == "dart"
    assert e.sass_snapshot_path.name == "sass.snapshot"


@pytest.mark.skipif('sys.platform != "win32"')
def test_windows_release_object():
    r = P.Release.init()
    assert r.os == "windows"
    e = r.executor(P.resolve_bin_base_dir())
    assert e.dart_vm_path.name == "dart.exe"
    assert e.sass_snapshot_path.name == "sass.snapshot"
