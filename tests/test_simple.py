import filecmp
import shutil
from pathlib import Path

import pytest

from sass_embedded import simple as M

here = Path(__file__).parent

targets = [
    d.name
    for d in (here / "test-basics").glob("*")
    if d.is_dir() and d.stem not in ["modules"]
]


class TestFor_compie_string:
    @pytest.mark.parametrize("target", targets)
    @pytest.mark.parametrize("syntax", ["sass", "scss"])
    @pytest.mark.parametrize("style", ["expanded", "compressed"])
    def test_default_calling(self, target: str, syntax: str, style: str):
        source = here / "test-basics" / f"{target}/style.{syntax}"
        expect = here / "test-basics" / f"{target}/style.{style}.css"
        result = M.compile_string(source.read_text(), syntax=syntax, style=style)  # type: ignore[arg-type]
        assert result == expect.read_text()

    @pytest.mark.parametrize("target", targets)
    @pytest.mark.parametrize("syntax", ["sass", "scss"])
    @pytest.mark.parametrize("style", ["expanded", "compressed"])
    def test_with_embed_sourcemap(self, target: str, syntax: str, style: str, caplog):
        source = here / "test-basics" / f"{target}/style.{syntax}"
        expect = here / "test-basics" / f"{target}/style.{style}.css"
        expect_text = expect.read_text().strip()
        result1 = M.compile_string(
            source.read_text(),
            syntax=syntax,  # type: ignore[arg-type]
            style=style,  # type: ignore[arg-type]
            embed_sourcemap=True,
        )
        assert expect_text != result1
        assert expect_text in result1
        result2 = M.compile_string(
            source.read_text(),
            syntax=syntax,  # type: ignore[arg-type]
            style=style,  # type: ignore[arg-type]
            embed_sourcemap=True,
            embed_sources=True,
        )
        assert expect_text in result2
        assert result1 != result2
        result3 = M.compile_string(
            source.read_text(),
            syntax=syntax,  # type: ignore[arg-type]
            style=style,  # type: ignore[arg-type]
            embed_sources=True,
        )
        assert result3 != result1
        assert result3 != result2
        assert result3.strip() == expect_text
        assert caplog.records


class TestFor_compie_file:
    @pytest.mark.parametrize("target", targets)
    @pytest.mark.parametrize("syntax", ["sass", "scss"])
    @pytest.mark.parametrize("style", ["expanded", "compressed"])
    def test_compile_file(self, target: str, syntax: str, style: str, tmpdir: Path):
        source = here / "test-basics" / f"{target}/style.{syntax}"
        expect = here / "test-basics" / f"{target}/style.{style}.css"
        dest = tmpdir / f"{target}.css"
        result = M.compile_file(source, dest, style=style)  # type: ignore[arg-type]
        assert expect.read_text().strip() in result.read_text().strip()

    @pytest.mark.parametrize("target", targets)
    def test_compile_with_embed_sourcemap(self, target: str, tmpdir: Path):
        source = here / "test-basics" / f"{target}/style.scss"
        dest = tmpdir / f"{target}.css"
        M.compile_file(source, dest, embed_sourcemap=True)
        assert not (tmpdir / f"{target}.css.map").exists()
        r_embed_map = dest.read_text(encoding="utf8")
        M.compile_file(source, dest, embed_sourcemap=True, embed_sources=True)
        assert not (tmpdir / f"{target}.css.map").exists()
        r_embed_sources = dest.read_text(encoding="utf8")
        assert r_embed_map != r_embed_sources


@pytest.mark.parametrize(
    "source_path,load_dir",
    [
        ("modules/scss/style.scss", "modules/scss"),
        ("modules/scss/style.scss", "modules/sass"),
        ("modules/sass/style.sass", "modules/scss"),
        ("modules/sass/style.sass", "modules/sass"),
    ],
)
def test_compile_string_moduled_scss(source_path: str, load_dir: str):
    source = here / "test-basics" / source_path
    expect = here / "test-basics" / "modules/style.expanded.css"
    module_dir = here / "test-basics" / load_dir
    result = M.compile_string(
        source.read_text(),
        syntax=source.name[-4:],  # type: ignore[arg-type]
        load_paths=[module_dir],
    )
    assert result == expect.read_text()


def test_compile_string_moduled_sass():
    source = here / "test-basics" / "modules/scss" / "style.scss"
    expect = here / "test-basics" / "modules/style.expanded.css"
    result = M.compile_string(
        source.read_text(), syntax="scss", load_paths=[source.parent]
    )
    assert result == expect.read_text()


@pytest.mark.parametrize("syntax", ["sass", "scss"])
@pytest.mark.parametrize("style", ["expanded", "compressed"])
def test_compile_directory(syntax: str, style: str, tmpdir: Path):
    source = tmpdir / "source"
    source.mkdir()
    for s in (here / "test-basics").glob(f"*/*.{syntax}"):
        name = f"{s.parent.name}.{syntax}"
        shutil.copy(s, source / name)
    expected = tmpdir / "expected"
    expected.mkdir()
    for s in (here / "test-basics").glob(f"*/style.{style}.css"):
        if s.parent.name == "modules":
            continue
        name = f"{s.parent.name}.css"
        shutil.copy(s, expected / name)
    output = tmpdir / "output"
    output.mkdir()
    M.compile_directory(source, output)
    cmp = filecmp.dircmp(output, expected)
    output_files = list(Path(output).glob("*.css"))
    output_maps = list(Path(output).glob("*.css.map"))
    expexted_files = list(Path(expected).glob("*"))
    assert len(expexted_files) == len(output_files)
    assert len(output_files) == len(output_maps)
    assert cmp.left_only == sorted([f.name for f in output_maps])
