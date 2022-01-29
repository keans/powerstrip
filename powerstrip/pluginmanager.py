import zipfile
import logging
import shutil
from pathlib import Path
from typing import Union

from click import format_filename

from powerstrip.utils import load_module
from powerstrip.models.plugin import Plugin
from powerstrip.utils.utils import ensure_path
from powerstrip.exceptions import PluginManagerException


# prepare logger
log = logging.getLogger(__name__)


class PluginManager:
    """
    plugin manager
    """
    def __init__(
        self, plugin_directory: Union[str, Path] = ".",
        auto_discover: bool = True, subclass: Plugin = Plugin,
        plugin_ext=".pkg"
    ):
        self.plugin_directory = plugin_directory
        self.plugin_ext = plugin_ext

        if auto_discover:
            # auto discover plugins from directory
            self.discover(subclass)

    @property
    def plugin_directory(self) -> Path:
        return self._plugin_directory

    @plugin_directory.setter
    def plugin_directory(self, value):
        # ensure that plugin_directory is a path
        self._plugin_directory = ensure_path(value, must_exist=True)

    @property
    def plugin_ext(self) -> str:
        return self._plugin_ext

    @plugin_ext.setter
    def plugin_ext(self, value: str):
        if not value.startswith("."):
            # leading '.' missing
            raise PluginManagerException(
                f"Invalid extension '{value}'!"
            )

        self._plugin_ext = value

    def discover(self, subclass=Plugin):
        """
        discover all plugins from plugins
        """
        log.debug(
            f"Discovering all plugins in '{self.plugin_directory}' for "
            f"subclass '{subclass}'..."
        )
        for fn in self.plugin_directory.glob("**/*.py"):
            # derive from relative path the module name
            module_name = (
                fn.with_suffix("").relative_to(
                    self.plugin_directory
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

    def info(self, plugin_name: str):
        """
        uninstall a plugin
        """
        pass

    def install(self, filename: Union[str, Path]):
        """
        install a plugin from filename
        """
        pass

    def uninstall(self, plugin_name: str):
        """
        uninstall a plugin
        """
        pass
