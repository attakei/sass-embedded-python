from pathlib import Path
import shutil

import pytest

from sass_embedded import simple as M

here = Path(__file__).parent

targets = [
    css.stem
    for css in (here / "test-basics").glob("*.css")
    if not css.name.startswith("_") and css.stem not in ["modules"]
]


@pytest.mark.parametrize("target", targets)
def test_compile_string_scss(target: str):
    source = here / "test-basics" / f"{target}.scss"
    expect = here / "test-basics" / f"{target}.css"
    result = M.compile_string(source.read_text(), syntax="scss")
    assert result == expect.read_text()


@pytest.mark.parametrize("target", targets)
def test_compile_string_sass(target: str):
    source = here / "test-basics" / f"{target}.sass"
    expect = here / "test-basics" / f"{target}.css"
    result = M.compile_string(source.read_text(), syntax="sass")
    assert result == expect.read_text()


@pytest.mark.parametrize("target", targets)
def test_compile_file_scss(target: str, tmpdir: Path):
    source = here / "test-basics" / f"{target}.scss"
    expect = here / "test-basics" / f"{target}.css"
    dest = tmpdir / f"{target}.css"
    result = M.compile_file(source, dest)
    assert expect.read_text() in result.read_text()


@pytest.mark.parametrize("target", targets)
def test_compile_file_sass(target: str, tmpdir: Path):
    source = here / "test-basics" / f"{target}.sass"
    expect = here / "test-basics" / f"{target}.css"
    dest = tmpdir / f"{target}.css"
    result = M.compile_file(source, dest)
    assert expect.read_text() in result.read_text()


@pytest.mark.parametrize(
    "source_path,load_dir",
    [
        ("modules-scss/styles.scss", "modules-scss"),
        ("modules-scss/styles.scss", "modules-sass"),
        ("modules-sass/styles.sass", "modules-scss"),
        ("modules-sass/styles.sass", "modules-sass"),
    ],
)
def test_compile_string_moduled_scss(source_path: str, load_dir: str):
    source = here / "test-basics" / source_path
    expect = here / "test-basics" / "modules.css"
    module_dir = here / "test-basics" / load_dir
    result = M.compile_string(
        source.read_text(),
        syntax=source.name[-4:],  # type: ignore[arg-type]
        load_paths=[module_dir],
    )
    assert result == expect.read_text()


def test_compile_string_moduled_sass():
    source = here / "test-basics" / "modules-scss" / "styles.scss"
    expect = here / "test-basics" / "modules.css"
    result = M.compile_string(
        source.read_text(), syntax="scss", load_paths=[source.parent]
    )
    assert result == expect.read_text()


def test_compile_directory(tmpdir: Path):
    source = tmpdir / "source"
    source.mkdir()
    for s in (here / "test-basics").glob("*.scss"):
        shutil.copy(s, source)
    expected = tmpdir / "expected"
    expected.mkdir()
    for s in (here / "test-basics").glob("*.css"):
        shutil.copy(s, expected)
    output = tmpdir / "output"
    output.mkdir()
    result = M.compile_directory(source, output)
