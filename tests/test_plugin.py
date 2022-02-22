#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pytest

from powerstrip.models import Plugin


class TestPlugin:
    """
    tests for powerstrip
    """

    def test_plugin(self):
        """
        do a test
        """

        # cannot use abstract class
        with pytest.raises(TypeError):
            p = Plugin()

        # create child class
        class ExamplePlugin(Plugin):
            def init(self):
                pass
            def run(self):
                pass
            def shutdown(self):
                pass

        plugin = ExamplePlugin(auto_load_metadata=False)

        # call all methods
        plugin.init()
        plugin.run()
        plugin.shutdown()

        print(plugin)
