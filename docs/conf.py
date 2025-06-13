import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "OpenPecha Toolkit"
copyright = "2024, OpenPecha"
author = "OpenPecha"

# The full version, including alpha/beta/rc tags
release = "2.1.13"

# The short X.Y version
version = "2.1"

# The master toctree document
master_doc = "index"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Enable MyST features
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "html_admonition",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# MyST configuration
myst_heading_anchors = 3
myst_all_links_external = False
