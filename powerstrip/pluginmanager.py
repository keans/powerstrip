import zipfile
import logging
import shutil
from pathlib import Path
from typing import Union

from click import format_filename
from powerstrip.models import plugin

from powerstrip.utils import load_module
from powerstrip.models.plugin import Plugin
from powerstrip.models.pluginpackage import PluginPackage
from powerstrip.utils.utils import ensure_path
from powerstrip.exceptions import PluginManagerException


# prepare logger
log = logging.getLogger(__name__)

# TODO:
#
# ADD SUBDIRECTORY WHEN FLAG SET IN PM FOR CATEGORIES?!
#

class PluginManager:
    """
    plugin manager
    """
    def __init__(
        self,
        plugins_directory: Union[str, Path],
        auto_discover: bool = True,
        subclass: Plugin = Plugin,
        plugin_ext: str = ".pkg",
        category_subdir: bool = False
    ):
        self.plugins_directory = plugins_directory
        self.plugin_ext = plugin_ext
        self.category_subdir = category_subdir

        if auto_discover:
            # auto discover plugins from directory
            self.discover(subclass)

    @property
    def plugins_directory(self) -> Path:
        """
        returns the plugins directory where all plugins are installed

        :return: plugins directory
        :rtype: Path
        """
        return self._plugin_directory

    @plugins_directory.setter
    def plugins_directory(self, value: Union[str, Path]) -> None:
        """
        set the plugins directory

        :param value: plugins directory
        :type value: Union[str, Path]
        """
        # ensure that plugin_directory is a path
        self._plugin_directory = ensure_path(value, must_exist=True)

    @property
    def plugin_ext(self) -> str:
        """
        returns plugin extension

        :return: plugin extension
        :rtype: str
        """
        return self._plugin_ext

    @plugin_ext.setter
    def plugin_ext(self, value: str):
        """
        set plugin extension

        :param value: plugin extension
        :type value: str
        :raises PluginManagerException: raised if invalid extension
        """
        if not value.startswith("."):
            # leading '.' missing
            raise PluginManagerException(
                f"Invalid extension '{value}'!"
            )

        self._plugin_ext = value

    def get_plugin_classes(
        self,
        subclass: Plugin = Plugin,
        category: str = None,
        tags: list = []
    ) -> list:
        plugin_classes = []
        for plugincls in Plugin.__subclasses__():
            # if (category is not None) and category not in plugincls.C

            # if (
            #     issubclass(plugincls, subclass) and
            #     (plugincls is not subclass)
            # ):
            print(plugincls)

    def discover(self, subclass: Plugin = Plugin) -> None:
        """
        discover all plugins that are located in the plugins directory
        and that do match the given subclass

        :param subclass: subclass for which should be filtered,
                         defaults to Plugin
        :type subclass: Plugin, optional
        """
        log.debug(
            f"Discovering all plugins in '{self.plugins_directory}' for "
            f"subclass '{subclass}'..."
        )
        for fn in self.plugins_directory.glob("**/*.py"):
            # derive from relative path the module name
            module_name = (
                fn.with_suffix("").relative_to(
                    self.plugins_directory
                ).as_posix()
            ).replace("/", ".")

            # load the module
            load_module(module_name, fn)

        # return all classes that are a subclass of the given class
        plugin_classes = [
            plugincls
            for plugincls in Plugin.__subclasses__()
            if (
                issubclass(plugincls, subclass) and
                (plugincls is not subclass)
            )
        ]

        log.debug(
            f"Found {len(plugin_classes)} plugins: "
            f"{', '.join([p.__name__ for p in plugin_classes])}"
        )

        return plugin_classes

    def info(self, plugin_filename: Union[str, Path]) -> dict:
        """
        get metadata information of the given plugin file

        :param plugin_filename: plugin filename
        :type plugin_name: Union[str, Path]
        :return: metata of the plugin
        :rtype: dict
        """
        return PluginPackage.info("pluginB-0.0.2.psp")

    def install(self, filename: Union[str, Path]) -> None:
        """
        install plugin from given filename

        :param filename: plugin filename
        :type filename: Union[str, Path]
        """
        pp = PluginPackage(plugins_directory=self.plugins_directory)
        pp.install(filename)

    def uninstall(self, plugin_name: str) -> None:
        """
        uninstall the plugin with the given name

        :param plugin_name: plugin name
        :type plugin_name: str
        """
        pp = PluginPackage(plugins_directory=self.plugins_directory)
        pp.uninstall(plugin_name)
