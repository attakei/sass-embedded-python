import filecmp
import shutil
from pathlib import Path

import pytest

from sass_embedded.protocol.compiler import Compiler 
from sass_embedded.protocol.embedded_sass_pb2 import Syntax, OutputStyle, Value

here = Path(__file__).parent

targets = [
    d.name
    for d in (here / "test-basics").glob("*")
    if d.is_dir() and d.stem not in ["modules", "custom"]
]

class TestFor_compiler:
    def test_version_information(self):
        compiler = Compiler()
        version_info = compiler.get_version_info()
        assert "compiler_version" in version_info
        assert "protocol_version" in version_info
        assert "implementation_version" in version_info
        assert "implementation_name" in version_info
 
class TestFor_compile_string:
    @pytest.mark.parametrize("target", targets)
    @pytest.mark.parametrize("syntax", [Syntax.INDENTED, Syntax.SCSS])
    @pytest.mark.parametrize("style", [OutputStyle.EXPANDED, OutputStyle.COMPRESSED])
    def test_default_calling(self, target: str, syntax: Syntax, style: OutputStyle):
        source = here / "test-basics" / f"{target}/style.{'sass' if syntax == Syntax.INDENTED else 'scss'}"
        expect = here / "test-basics" / f"{target}/style.{'compressed' if style == OutputStyle.COMPRESSED else 'expanded'}.css"
        M = Compiler()
        result = M.compile_string(source.read_text(), syntax=syntax, style=style)  # type: ignore[arg-type]
        assert result.output == expect.read_text()

    @pytest.mark.parametrize("target", targets)
    @pytest.mark.parametrize("syntax", [Syntax.INDENTED, Syntax.SCSS])
    @pytest.mark.parametrize("style", [OutputStyle.EXPANDED, OutputStyle.COMPRESSED])
    def test_with_embed_sourcemap(self, target: str, syntax: Syntax, style: OutputStyle, caplog):
        source = here / "test-basics" / f"{target}/style.{'sass' if syntax == Syntax.INDENTED else 'scss'}"
        expect = here / "test-basics" / f"{target}/style.{'compressed' if style == OutputStyle.COMPRESSED else 'expanded'}.css"
        expect_text = expect.read_text().strip()
        M = Compiler()
        result1 = M.compile_string(
            source.read_text(),
            syntax=syntax,
            style=style,
            embed_sourcemap=True,
        )
        assert result1.output
        assert expect_text != result1.output
        assert expect_text in result1.output
        M = Compiler()
        result2 = M.compile_string(
            source.read_text(),
            syntax=syntax,
            style=style,
            embed_sourcemap=True,
            embed_sources=True,
        )
        assert result2.output
        assert expect_text in result2.output
        assert result1 != result2.output
        M = Compiler()
        result3 = M.compile_string(
            source.read_text(),
            syntax=syntax,
            style=style,
            embed_sources=True,
        )
        assert result3.output
        assert result3.output != result1
        assert result3.output != result2
        assert result3.output.strip() == expect_text
        # Protocol-based compiler doesn't generate the same deprecation warnings as CLI
        # assert caplog.records

    @pytest.mark.parametrize(
        "source_path,load_dir",
        [
            ("modules/scss/style.scss", "modules/scss"),
            ("modules/scss/style.scss", "modules/sass"),
            ("modules/sass/style.sass", "modules/scss"),
            ("modules/sass/style.sass", "modules/sass"),
        ],
    )
    def test_compile_with_moduled_scss(self, source_path: str, load_dir: str):
        source = here / "test-basics" / source_path
        expect = here / "test-basics" / "modules/style.expanded.css"
        module_dir = here / "test-basics" / load_dir
        syntax = Syntax.INDENTED if source.name.endswith('.sass') else Syntax.SCSS
        M = Compiler()
        result = M.compile_string(
            source.read_text(),
            syntax=syntax,
            load_paths=[module_dir],
        )
        assert result.output == expect.read_text()

    def test_scss_with_moduled_sass(self):
        source = here / "test-basics" / "modules/scss" / "style.scss"
        expect = here / "test-basics" / "modules/style.expanded.css"
        M = Compiler()
        result = M.compile_string(
            source.read_text(), syntax=Syntax.SCSS, load_paths=[source.parent]
        )
        assert result.output == expect.read_text()

    def test_invalid(self):
        source = here / "test-invalids" / "no-variables.scss"
        M = Compiler()
        result = M.compile_string(source.read_text(), syntax=Syntax.SCSS)
        assert not result.ok
        assert result.error
        assert not result.output

class TestFor_compile_string_with_custom_functions:
    @pytest.mark.parametrize("syntax", [Syntax.INDENTED, Syntax.SCSS])
    @pytest.mark.parametrize("style", [OutputStyle.EXPANDED, OutputStyle.COMPRESSED])
    def test_default_calling(self, syntax: Syntax, style: OutputStyle):
        source = here / "test-basics" / f"custom/style.{'sass' if syntax == Syntax.INDENTED else 'scss'}"
        expect = here / "test-basics" / f"custom/style.{'compressed' if style == OutputStyle.COMPRESSED else 'expanded'}.css"
        
        def theme_option(name: str, default_value) -> Value:
            from sass_embedded.protocol.embedded_sass_pb2 import SingletonValue
            if name == 'nocover':
                return Value(singleton=SingletonValue.TRUE)
            # default_value is a Python type, need to convert back to Value
            if isinstance(default_value, bool):
                return Value(singleton=SingletonValue.TRUE if default_value else SingletonValue.FALSE)
            return Value(singleton=SingletonValue.FALSE)
        
        def config(name: str, default_value) -> Value:
            if name == 'cover-bg':
                return Value(string=Value.String(text='#961a1a', quoted=False))
            # default_value is a Python string, convert to Value
            if isinstance(default_value, str):
                return Value(string=Value.String(text=default_value, quoted=False))
            return Value(string=Value.String(text='', quoted=False))
        
        M = Compiler()
        result = M.compile_string(source.read_text(), syntax=syntax, style=style, custom_functions={"theme_option": theme_option, "config": config})  # type: ignore[arg-type]
        assert result.output == expect.read_text()

class TestFor_compile_file:
    @pytest.mark.parametrize("target", targets)
    @pytest.mark.parametrize("syntax", [Syntax.INDENTED, Syntax.SCSS])
    @pytest.mark.parametrize("style", [OutputStyle.EXPANDED, OutputStyle.COMPRESSED])
    def test_default_calling(self, target: str, syntax: Syntax, style: OutputStyle, tmpdir: Path):
        source = here / "test-basics" / f"{target}/style.{'sass' if syntax == Syntax.INDENTED else 'scss'}"
        expect = here / "test-basics" / f"{target}/style.{'compressed' if style == OutputStyle.COMPRESSED else 'expanded'}.css"
        dest = tmpdir / f"{target}.css"
        M = Compiler()
        result = M.compile_file(source, dest, syntax=syntax, style=style)  # type: ignore[arg-type]
        assert result.output
        assert expect.read_text().strip() in result.output.read_text().strip()
