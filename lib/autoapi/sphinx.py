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
Glue for Sphinx API.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from traceback import format_exc
from os.path import join, dirname, abspath, exists

from jinja2.sandbox import SandboxedEnvironment
from sphinx.util.osutil import ensuredir
from sphinx.jinja2glue import BuiltinTemplateLoader

from . import __version__
from .apinode import APINode


def handle_exception(func):
    """
    Utility decorator to report all exceptions in module without making Sphinx
    to die.
    """
    def wrapper(app):
        try:
            func(app)
        except Exception as e:
            app.warn('Unhandled exception in autoapi module: {}'.format(e))
            app.debug(format_exc())
    return wrapper


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


@handle_exception
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
        # Note: Commenting out, as the situation is more complex than this.
        # For example, a node can not be a leaf, and thus is generated. But
        # later we found out that their leaf children doesn't have a public
        # API, and so we ignore them, but the parent got a reference for them
        # in the toctree. Until I decide what to do with this, if to filter
        # all branches or to just render everything I'll leave it as just
        # render everything. In part, maybe because the documentation for the
        # module can be relevant while not their public API?
        # nodes = [
        #     (name, node) for name, node in tree.directory.items()
        #     if node.has_public_api() or not node.is_leaf()
        # ]
        nodes = tree.directory.items()
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
