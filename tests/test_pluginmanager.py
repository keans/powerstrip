#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pytest

from powerstrip.pluginmanager import PluginManager
from powerstrip.exceptions import PluginManagerException
from .test_metadata import METADATA, METADATA_VALUES


# dummy plugin file
PLUGIN_PYTHON = """
from powerstrip import Plugin

class {PluginName}(Plugin):
    def init(self):
        pass

    def run(self):
        pass

    def shutdown(self):
        pass
"""


class TestPluginManager:
    """
    tests for powerstrip
    """

    def test_pluginmanager(self, tmp_path):
        """
        do a test
        """
        # target directory where packed plugin files will be stored
        target_directory = tmp_path / "plugins"
        target_directory.mkdir()

        # invalid pluginmanager directory
        with pytest.raises(ValueError):
            pm = PluginManager("doesnotexit/")

        # valid pluginmanager directory
        pm = PluginManager(target_directory)

        # no categories
        assert len(pm.categories) == 0

        # valid pluginmanager directory with categories
        pm = PluginManager(target_directory, use_category=True)
        assert pm.plugins_directory == target_directory

        # create temp path
        plugin_dir = tmp_path / "myplugin"
        plugin_dir.mkdir()

        # create metadata.yml file
        metadata_file = plugin_dir / "metadata.yml"
        metadata_file.write_text(
            METADATA.format(**METADATA_VALUES)
        )

        # create plugin file
        plugin_file = plugin_dir / "plugin.py"
        plugin_file.write_text(
            PLUGIN_PYTHON.format(**{
                "PluginName" : METADATA_VALUES["name"]
            })
        )

        # create plugin package
        plugin_filename = pm.pack(plugin_dir, target_directory=target_directory)
        assert plugin_filename.exists()

        # get plugin info
        info = pm.info(plugin_filename)

        # install plugin
        plugin_dir = pm.install(plugin_filename)

        # get categories
        assert pm.categories == [METADATA_VALUES["category"]]

        # discover plugins
        pm.discover()

        # get all plugins
        assert len(pm.get_plugin_classes()) == 1

        # get all plugins with given tag, i.e., the one installed
        assert len(pm.get_plugin_classes(tag="blup")) == 1

        # get all plugins with unknown tag
        assert len(pm.get_plugin_classes(tag="xyz")) == 0

        # get all plugins with given category, i.e., the one installed
        assert len(
            pm.get_plugin_classes(category=METADATA_VALUES["category"])
        ) == 1

        # get all plugins with unknown category
        assert len(pm.get_plugin_classes(category="unknow_category")) == 0

        # get all plugins with given category and valid tag
        assert len(
            pm.get_plugin_classes(
                category=METADATA_VALUES["category"],
                tag="blup"
            )
        ) == 1

        # get all plugins with given category and invalid tag
        assert len(
            pm.get_plugin_classes(
                category=METADATA_VALUES["category"],
                tag="xyz"
            )
        ) == 0

        # uninstall plugin
        pm.uninstall(
            plugin_name=METADATA_VALUES["name"],
            category=METADATA_VALUES["category"]
        )

