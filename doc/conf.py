# -*- coding: utf-8 -*-
#
# autoapi documentation build configuration file.
#
# This file is execfile()d with the current directory set to its
# containing dir.

from sys import path
from pathlib import Path
from datetime import date

from autoapi import __version__
from sphinx_readable_theme import get_html_theme_path

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# Allow to find the 'documented.py' example
path.insert(0, str(Path(__file__).resolve().parent))

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'autoapi.sphinx',
    'plantweb.directive',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'AutoAPI'
author = 'KuraLabs S.R.L'
years = '2015-{}'.format(date.today().year)
copyright = '{}, {}'.format(years, author)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__


# -- Options for HTML output ----------------------------------------------

html_theme = 'readable'

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d'


# Add style overrides
def setup(app):
    app.add_stylesheet('styles/custom.css')


# -- Plugins options ----------------------------------------------------------

# AutoAPI configuration
autoapi_modules = {
    'autoapi': {'prune': True},
    'documented': {'output': 'autoapi'}
}

# Plantweb configuration
plantweb_defaults = {
    'use_cache': True,
    'format': 'svg',
}

# Configure Graphviz
graphviz_output_format = 'svg'

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}
