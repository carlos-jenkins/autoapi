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
Test suite for module autoapi.apinode.

See http://pythontesting.net/framework/pytest/pytest-introduction/#fixtures
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

import pytest  # noqa

from autoapi import APINode


def test_autotree():
    """
    Check that the APINode tree is consistent with a known package.
    """
    tree = APINode('autoapi')

    assert tree.is_root()
    assert len(tree.directory) == 3
    assert tree.is_relevant()
    assert tree.has_public_api()
    assert tree.get_module('autoapi.apinode') is not None
    assert not tree.get_module('autoapi.apinode').is_relevant()
    assert tree.tree()
    assert tree.tree(fullname=False)
    assert repr(tree)
    assert str(tree)

    for node, leaves in tree.walk():
        assert not node.is_leaf()
        for leaf in leaves:
            assert leaf.is_leaf()
