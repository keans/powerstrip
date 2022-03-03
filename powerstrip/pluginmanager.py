from inspect import isclass
import logging
from pathlib import Path
from typing import Union

from powerstrip.utils import load_module
from powerstrip.models.plugin import Plugin
from powerstrip.models.metadata import Metadata
from powerstrip.models.pluginpackage import PluginPackage
from powerstrip.utils.utils import ensure_path
from powerstrip.exceptions import PluginManagerException


class PluginManager:
    """
    plugin manager
    """
    def __init__(
        self,
        plugins_directory: Union[str, Path],
        subclass: Plugin = Plugin,
        use_category: bool = False,
        auto_discover: bool = True,
        plugin_ext: str = ".psp"
    ):
        """
        initialize the plugin manager class

        :param plugins_directory: directory where plugins are installed
        :type plugins_directory: Union[str, Path]
        :param subclass: subclass of Plugin that is managed by the
                         plugin manager, defaults to Plugin
        :type subclass: Plugin, optional
        :param category_subdir: use category subdirectories, defaults to False
        :type use_category: bool, optional
        :param auto_discover: if True, plugins will be discovered on startup,
                              defaults to True
        :type auto_discover: bool, optional
        :param plugin_ext: plugin extension name, defaults to ".psp"
        :type plugin_ext: str, optional
        """
        self.plugins_directory = plugins_directory
        self.subclass = subclass
        self.use_category = use_category
        self.plugin_ext = plugin_ext
        self.log = logging.getLogger(self.__class__.__name__)

        if auto_discover and not use_category :
            # auto discover plugins from directory, if no category required
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
        self._plugin_directory = ensure_path(value)

        if not self._plugin_directory.exists():
            # plugin directory does not exist => create it
            self._plugin_directory.mkdir(parents=True)

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

    @property
    def categories(self) -> list:
        """
        return list of categories, i.e., list of subdirectories
        in plugin directory; if category is disabled return
        empty list

        :return: list of categories, if category is disabled empty list
        :rtype: list
        """
        if not self.use_category:
            # categories not used, return empty list
            return []

        return [
            directory.parents[1].name
            for directory in self.plugins_directory.glob(
                f"**/{Metadata.METADATA_FILENAME}"
            )
            if directory
        ]

    def get_plugin_classes(
        self,
        subclass: Plugin = None,
        category: str = None,
        tag: str = None
    ) -> list:
        # if not provided, use originally define subclass
        subclass = subclass or self.subclass

        plugin_classes = []
        for plugincls in subclass.__subclasses__():
            plugin = plugincls()

            match = True
            if (
                (subclass is not None) and
                not issubclass(plugincls, subclass)
            ):
                # subclass is not matching
                match = False

            if (
                (category is not None) and
                (category != plugin.metadata.category)
            ):
                # category is not matching
                match = False

            if (
                (tag is not None) and
                (tag not in plugincls().metadata.tags)
            ):
                # tag is not matching
                match = False

            if match:
                # matching search criteria then add to list
                plugin_classes.append(plugincls)

        return plugin_classes

    def discover(
        self,
        subclass: Plugin = Plugin,
    ) -> None:
        """
        discover all plugins that are located in the plugins directory
        and that do match the given subclass

        :param subclass: subclass for which should be filtered,
                         defaults to Plugin
        :type subclass: Plugin, optional
        """
        assert (subclass is None) or issubclass(subclass, Plugin)

        self.log.debug(
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

        self.log.debug(
            f"Found {len(plugin_classes)} plugins: "
            f"{', '.join([p.__name__ for p in plugin_classes])}"
        )

        return plugin_classes

    def pack(
        self,
        directory: Union[str, Path],
        target_directory: Union[str, Path] = "."
    ) -> Path:
        """
        pack plugin from given source directory and store the
        resulting plugin package to the target directory

        :param directory: plugin source directory
        :type directory: Union[str, Path]
        :param target_directory: target directory to which packed plugin
                                 will be stored
        :type target_directory: Union[str, Path]
        :return: filename of the packed plugin
        :rtype: Path
        """
        return PluginPackage.pack(
            directory=directory,
            target_directory=target_directory,
            ext=self.plugin_ext
        )

    def info(self, plugin_filename: Union[str, Path]) -> dict:
        """
        get metadata information of the given plugin file

        :param plugin_filename: plugin filename
        :type plugin_name: Union[str, Path]
        :return: metata of the plugin
        :rtype: dict
        """
        return PluginPackage.info(plugin_filename)

    def install(
        self,
        plugin_filename: Union[str, Path]
    ) -> Path:
        """
        install plugin from given filename

        :param plugin_filename: plugin filename
        :type plugin_filename: Union[str, Path]
        :return: installed plugin directory
        """
        return PluginPackage.install(
            plugin_filename=plugin_filename,
            target_directory=self.plugins_directory,
            use_category=self.use_category
        )

    def uninstall(
        self,
        plugin_name: str,
        category: str = None
    ) -> None:
        """
        uninstall the plugin with the given name

        :param plugin_name: plugin name
        :type plugin_name: str
        :param category: plugin's category
        :type category: str
        """
        PluginPackage.uninstall(
            plugin_name=plugin_name,
            target_directory=self.plugins_directory,
            category=category
        )

    def __repr__(self) -> str:
        """
        string representation of plugin manager

        :return: string representation of plugin manager
        :rtype: str
        """
        return (
            f"<PluginManager(plugins_directory='{self.plugins_directory}', "
            f"subclass={self.subclass}, plugin_ext='{self.plugin_ext}')>"
        )
