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
Example usage of the APINode class.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import readline  # noqa
from code import InteractiveConsole
from logging import basicConfig, DEBUG

from autoapi.apinode import APINode


if __name__ == '__main__':

    basicConfig(level=DEBUG)
    m = APINode('sphinx')

    for node, leaves in m.walk():
        print(
            '{} node has leaves: {}'.format(
                node.name, ', '.join([l.name for l in leaves])
            )
        )

    InteractiveConsole(globals()).interact()
