from pathlib import Path

import pytest

from sass_embedded import simple as M

here = Path(__file__).parent

targets = [
    css.stem
    for css in (here / "test-basics").glob("*.css")
    if not css.name.startswith("_")
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
