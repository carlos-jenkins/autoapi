# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Jenkins <carlos@jenkins.co.cr>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
autoapi directive for Sphinx.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from os.path import join, dirname, abspath, exists

from jinja2.sandbox import SandboxedEnvironment
from sphinx.util.osutil import ensuredir
from sphinx.jinja2glue import BuiltinTemplateLoader

from . import __version__
from .apinode import APINode


def get_template_env(app):
    """
    Get the template environment.

    .. note::

       Template should be loaded as a package_data using
       :py:function:`pkgutil.get_data`, but because we want the user to
       override the default template we need to hook it to the Sphinx loader,
       and thus a file system approach is required as it is implemented like
       that.
    """
    template_dir = [join(dirname(abspath(__file__)), 'template')]
    template_loader = BuiltinTemplateLoader()
    template_loader.init(app.builder, dirs=template_dir)
    template_env = SandboxedEnvironment(loader=template_loader)
    return template_env


def builder_inited(app):
    """
    autoapi Sphinx extension hook for the ``builder-inited`` event.

    This hook will read the configuration value ``autoapi_modules`` and render
    the modules described in it.
    """
    # Get modules to build documentation for
    modules = app.config.autoapi_modules
    if not modules:
        return

    # Get template environment
    template_env = get_template_env(app)

    for module, options in modules.items():

        # Get options
        defaults = {
            'override': True,
            'template': 'module.rst',
            'output': module
        }
        if options:
            defaults.update(options)

        # Get template
        template = template_env.get_template(defaults['template'])

        # Build API tree
        tree = APINode(module)

        # Gather nodes to document
        # Ignore leaf nodes without public API
        # Non-leaf nodes without public API are required to be rendered
        # in order to have an index of their subnodes.
        nodes = [
            (name, node) for name, node in tree.directory.items()
            if node.has_public_api() or not node.is_leaf()
        ]
        if not nodes:
            continue

        # Define output directory
        out_dir = join(app.env.srcdir, defaults['output'])
        ensuredir(out_dir)

        # Iterate nodes and render them
        for name, node in nodes:
            out_file = join(out_dir, name + app.config.source_suffix[0])

            # Skip file if it override is off and it exists
            if not defaults['override'] and exists(out_file):
                continue

            with open(out_file, 'w') as fd:
                fd.write(template.render(node=node))


def setup(app):
    """
    autoapi Sphinx extension setup.

    See http://sphinx-doc.org/extdev/tutorial.html#the-setup-function
    """
    # autodoc is required
    app.setup_extension('sphinx.ext.autodoc')
    app.add_config_value('autoapi_modules', {}, True)
    app.connect(b'builder-inited', builder_inited)
    return {'version': __version__}


__all__ = ['builder_inited', 'setup']
