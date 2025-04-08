import re
import shutil
from pathlib import Path

import pytest

from sass_embedded import simple as M

here = Path(__file__).parent

targets = [
    css.stem.split(".")[0]
    for css in (here / "test-basics").glob("*.expanded.css")
    if not css.name.startswith("_") and css.stem not in ["modules.expanded"]
]


@pytest.mark.parametrize("target", targets)
@pytest.mark.parametrize("syntax", ["sass", "scss"])
@pytest.mark.parametrize("style", ["expanded", "compressed"])
def test_compile_string(target: str, syntax: str, style: str):
    source = here / "test-basics" / f"{target}.{syntax}"
    expect = here / "test-basics" / f"{target}.{style}.css"
    result = M.compile_string(source.read_text(), syntax=syntax, style=style)  # type: ignore[arg-type]
    assert result == expect.read_text()


@pytest.mark.parametrize("target", targets)
@pytest.mark.parametrize("syntax", ["sass", "scss"])
@pytest.mark.parametrize("style", ["expanded", "compressed"])
def test_compile_file(target: str, syntax: str, style: str, tmpdir: Path):
    source = here / "test-basics" / f"{target}.{syntax}"
    expect = here / "test-basics" / f"{target}.{style}.css"
    dest = tmpdir / f"{target}.css"
    result = M.compile_file(source, dest, style=style)  # type: ignore[arg-type]
    assert expect.read_text().strip() in result.read_text().strip()


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
    expect = here / "test-basics" / "modules.expanded.css"
    module_dir = here / "test-basics" / load_dir
    result = M.compile_string(
        source.read_text(),
        syntax=source.name[-4:],  # type: ignore[arg-type]
        load_paths=[module_dir],
    )
    assert result == expect.read_text()


def test_compile_string_moduled_sass():
    source = here / "test-basics" / "modules-scss" / "styles.scss"
    expect = here / "test-basics" / "modules.expanded.css"
    result = M.compile_string(
        source.read_text(), syntax="scss", load_paths=[source.parent]
    )
    assert result == expect.read_text()


@pytest.mark.parametrize("syntax", ["sass", "scss"])
@pytest.mark.parametrize("style", ["expanded", "compressed"])
def test_compile_directory(syntax: str, style: str, tmpdir: Path):
    source = tmpdir / "source"
    source.mkdir()
    for s in (here / "test-basics").glob(f"*.{syntax}"):
        shutil.copy(s, source)
    expected = tmpdir / "expected"
    expected.mkdir()
    for s in (here / "test-basics").glob(f"*.{style}.css"):
        shutil.copy(s, expected)
    output = tmpdir / "output"
    output.mkdir()
    result = M.compile_directory(source, output)
