import pytest

from sass_embedded._const import DART_SASS_VERSION
from sass_embedded import dart_sass as P


def test_relasename():
    r = P.Release("linux", "x64")
    assert r.fullname == f"{DART_SASS_VERSION}-linux-x64"
    bin_dir = r.resolve_dir(P.resolve_bin_base_dir())
    assert bin_dir.name == r.fullname
    assert bin_dir.parent.name == "_vendor"


def test_release_with_musl_suffix():
    r = P.Release("linux", "x64", is_musl=True)
    assert r.fullname == f"{DART_SASS_VERSION}-linux-x64-musl"
    assert r.archive_url.endswith(
        f"dart-sass-{DART_SASS_VERSION}-linux-x64-musl.tar.gz"
    )


def test_release_rejects_musl_on_non_linux():
    with pytest.raises(ValueError):
        P.Release("macos", "arm64", is_musl=True)


def test_release_init_picks_up_musl(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(P.platform, "system", lambda: "Linux")
    monkeypatch.setattr(P, "resolve_arch", lambda: "x64")
    monkeypatch.setattr(
        P, "sys_tags", lambda: [SimpleNamespace(platform="musllinux_1_2_x86_64")]
    )
    r = P.Release.init()
    assert r.os == "linux"
    assert r.is_musl is True


def test_release_init_no_musl_on_glibc(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(P.platform, "system", lambda: "Linux")
    monkeypatch.setattr(P, "resolve_arch", lambda: "x64")
    monkeypatch.setattr(
        P, "sys_tags", lambda: [SimpleNamespace(platform="manylinux_2_28_x86_64")]
    )
    r = P.Release.init()
    assert r.is_musl is False


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
