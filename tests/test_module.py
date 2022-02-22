#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pytest

from powerstrip.utils.module import load_module
from powerstrip.exceptions import ModuleException


class TestModule:
    """
    tests for powerstrip
    """

    def test_load_module(self):
        """
        do a test
        """
        # invalid module name type
        with pytest.raises(AssertionError):
            load_module(None, None)

        # invalid directory type
        with pytest.raises(AssertionError):
            load_module("bla", None)

        # directory does not exist
        with pytest.raises(ModuleException):
            load_module("unknown_module", "/doesnotexist")

        # module does not exist
        with pytest.raises(ModuleException):
            load_module("unknown_module", ".")

        # correct loading of utils module
        load_module(
            "powerstrip.utils.ensure_path",
            "../powerstrip/utils/utils.py"
        )
        assert "powerstrip.utils.ensure_path" in sys.modules
