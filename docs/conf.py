# Configuration file for the Sphinx documentation builder.
import importlib.metadata

# -- Project information
project = "Sass-embedded for Python"
copyright = "2025, Kazuya Takei"
author = "Kazuya Takei"
release = importlib.metadata.version("sass_embedded")

# -- General configuration
extensions = [
    "sphinx.ext.autodoc",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "alabaster"
html_static_path = ["_static"]
html_title = f"{project} v{release} documentation"
html_short_title = f"{project} v{release}"
