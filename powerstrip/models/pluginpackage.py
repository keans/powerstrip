import logging
import shutil
import zipfile
from pathlib import Path
from typing import Union

from powerstrip.utils.utils import ensure_path
from powerstrip.models import Metadata, plugin
from powerstrip.exceptions import PluginPackageException


# prepare logger
log = logging.getLogger(__name__)


class PluginPackage:
    """
    plugin package
    """
    def __init__(
        self, plugins_directory: Union[str, Path],
        extension=".psp"
    ):
        self.plugins_directory = plugins_directory
        self.extension = extension

    @property
    def plugins_directory(self) -> Path:
        return self._plugins_directory

    @plugins_directory.setter
    def plugins_directory(self, value: Union[str, Path]):
        self._plugins_directory = ensure_path(path=value, must_exist=True)

    @property
    def extension(self) -> Path:
        return self._extension

    @extension.setter
    def extension(self, value: str):
        if not value.startswith("."):
            # invalid plugin package extension
            raise PluginPackageException(
                f"Invalid extension '{value}'!"
            )

        self._extension = value

    def pack(self, directory: Union[str, Path]):
        """
        pack plugin directory into a plugin file
        """
        # ensure that directory is a Path and that it does exist
        directory = ensure_path(directory, must_exist=True)

        # try to read metadata to ensure that it is existing
        md = Metadata(directory)

        # plugin package filename
        plugin_filename = Path(f"{md.plugin_name}{self.extension}")
        if plugin_filename.exists():
            # plugin does already exist
            raise PluginPackageException(
                f"The plugin file '{plugin_filename}' does already exist!"
            )

        log.debug(f"Opening '{plugin_filename}'...")
        with zipfile.ZipFile(plugin_filename, "w") as zf:
            for fn in directory.glob("**/*"):
                if fn.suffix in (".pyc", ) or fn.name == "__pycache__":
                    # skip unwanted extensions
                    continue

                log.debug(f"Adding '{fn}' to plugin package...")
                zf.write(fn, fn.relative_to(directory))

    def install(self, plugin_filename: Union[str, Path]):
        """
        install plugin package from plugin file
        """
        # check that plugin filename is a Path and that it exists
        plugin_filename = ensure_path(plugin_filename, must_exist=True)
        if plugin_filename.suffix != self.extension:
            # invalid plugin extension
            raise PluginPackageException(
                f"Invalid plugin extension '{plugin_filename.suffix}' "
                f"(required: '{self.extension}')!"
            )

        try:
            log.debug(f"Opening '{plugin_filename}'...")
            with zipfile.ZipFile(plugin_filename) as zf:
                # get metadata from metadata file within the plugin package
                metadata = Metadata.create_from_f_obj(
                    zf.read(Metadata.METADATA_FILENAME)
                )

                # prepare target directory and check if it already exists
                target_directory = self.plugins_directory.joinpath(
                    metadata.name
                )
                if target_directory.exists():
                    # plugin does already exist
                    raise PluginPackageException(
                        f"The plugin '{metadata.name}' does already "
                        f"exist in '{self.plugins_directory}'! Abort."
                    )

                log.debug(f"Installing plugin to '{target_directory}'...")

                # create plugin directory
                target_directory.mkdir()

                # extract all files from plugin package to target directory
                zf.extractall(path=target_directory)

        except zipfile.BadZipFile as e:
            # not a zip file, i.e., not a valid plugin
            raise PluginPackageException(
                f"The file '{plugin_filename}' is not a valid plugin file!"
            )

    def uninstall(self, plugin_name: str):
        """
        uninstall plugin package
        """
        # get plugin directory by its name
        plugin_directory = self.plugins_directory.joinpath(plugin_name)
        if not plugin_directory.exists():
            raise PluginPackageException(
                f"The plugin '{plugin_name}' is not installed "
                f"in '{self.plugins_directory}'! Abort."
            )

        # read metadata before, to check if valid plugin directory
        md = Metadata(plugin_directory)

        # remove the plugin directory
        log.debug(
            f"removing plugin directory '{plugin_directory}'..."
        )
        shutil.rmtree(plugin_directory)

    def info(self, plugin_filename: Union[str, Path]):
        """
        show info about plugin package from metadata file
        """
        # check that plugin filename is a Path and that it exists
        plugin_filename = ensure_path(plugin_filename, must_exist=True)

        try:
            log.debug(f"Opening '{plugin_filename}'...")
            with zipfile.ZipFile(plugin_filename) as zf:
                # get metadata from metadata file within the plugin package
                metadata = Metadata.create_from_f_obj(
                    zf.read(Metadata.METADATA_FILENAME)
                )

                return metadata

        except zipfile.BadZipFile as e:
            # not a zip file, i.e., not a valid plugin
            raise PluginPackageException(
                f"The file '{plugin_filename}' is not a valid plugin file!"
            )
