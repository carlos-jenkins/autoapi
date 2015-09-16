"""
FIXME: Make it work.
FIXME: Add new documents to process queue. Determine where to put them.
FIXME: Do something with root toctree to hook direct submodules.
"""

from os.path import join, dirname, abspath
from traceback import print_exc

from jinja2.sandbox import SandboxedEnvironment

from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from sphinx.util.osutil import ensuredir
from sphinx.jinja2glue import BuiltinTemplateLoader

from . import __version__
from .apinode import APINode


class AutoAPI(Directive):
    """
    Autoapi directive.

    This directive will perform the following steps:

    - Build a :class:`autoapi.apinode.APINode` tree with the module name
      specified as argument.
    - Render the Jinja2 template with the root node and append the result as
      content for this directive.
    - Traverse the tree and for each node, except for leaf nodes without public
      API, render the Jinja2 template and write the result as a new source
      file.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True
    option_spec = {}

    def autoapi_build(self, tree):
        """
        """
        env = self.state.document.settings.env

        # DEBUG
        print('=' * 79)
        print(env.config.source_suffix)
        print(env.srcdir)
        print(env.doctreedir)
        print(env.found_docs)
        print('=' * 79)

        # Get template
        # Note: Template should be loaded as a package_data using
        # pkgutil.get_data(), but because we want the user to override the
        # default template we need to hook it to the Sphinx loader, and thus
        # a file system approach is required as it is implemented like that.
        template_dir = [join(dirname(abspath(__file__)), 'template')]
        template_loader = BuiltinTemplateLoader()
        template_loader.init(env.app.builder, dirs=template_dir)
        template_env = SandboxedEnvironment(loader=template_loader)
        template = template_env.get_template('module.rst')

        # Render root and append it to current node content
        autodoc = template.render(node=tree)
        self.content.extend(
            ViewList(initlist=autodoc.splitlines(), source=tree.name)
        )

        # Render all remaining nodes as separated documents
        gen_dir = join(env.srcdir, 'fixme')
        ensuredir(gen_dir)

        for name, node in tree.directory.items():

            # Ignore leaf nodes with public API
            # Non-leaf nodes without public API are required to be rendered
            # in order to have an index of their subnodes.
            if node.is_leaf and not node.has_public_api():
                continue

            out_file = join(gen_dir, name + env.config.source_suffix)
            with open(out_file, 'w') as fd:
                fd.write(template.render(node=node))

    def run(self):
        # Get name of the module that is directive argument
        module = self.arguments[0]

        try:
            # Build module tree
            tree = APINode(module)

            # Generate content
            self.autoapi_build(tree)

        except Exception as e:
            # Create a warning if the process failed
            print_exc()
            msg = 'Unable to build autoapi for {}: {}'.format(module, str(e))
            return [
                self.state.document.reporter.warning(msg, line=self.lineno)
            ]

        return []


def setup(app):
    # autodoc is required
    app.setup_extension('sphinx.ext.autodoc')
    app.add_directive('autoapi', AutoAPI)
    return {'version': __version__, 'parallel_read_safe': True}


__all__ = ['AutoAPI']
