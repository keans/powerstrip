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
        self,
        filename: str = None
    ):
        assert (filename is None) or isinstance(filename, (str, Path))

        self.filename = filename

    @property
    def filename(self) -> Path:
        """
        set filename of the plugin package

        :return: filename of the plugin package
        :rtype: Path
        """
        return self._filename

    @filename.setter
    def filename(self, value: Union[str, Path]):
        """
        sets the filename of the plugin package

        :param value: filename plugin
        :type value: Union[str, Path]
        """
        if value is not None:
            # set filename
            self._filename = ensure_path(path=value)

        else:
            # special case of unset filename directory
            self._filename = None

    def pack(
        self,
        directory: Union[str, Path],
        target_directory: Union[str, Path],
        ext: str = ".psp"
    ) -> Path:
        """
        packs raw plugin from given directory and creates a plugin
        package based on the given target plugin package name.

        :param directory: directory with raw plugin content
        :type directory: Union[str, Path]
        :param target_directory: target directory of the plugin package
        :type target_directory: Union[str, Path]
        :param ext: name of the plugin package extension
        :type ext: str
        :returns: name of the plugin package
        :type ext: Path
        :raises PluginPackageException: if plugin package is already existing
        """
        assert isinstance(directory, (str, Path))
        assert isinstance(target_directory, (str, Path))
        assert isinstance(ext, str) and ext.startswith(".")

        # ensure that directory is a Path and that it does exist
        directory = ensure_path(directory, must_exist=True)

        # load metadata from directory
        md = Metadata.create_from_directory(directory)

        # target directory must exist
        target_directory = ensure_path(target_directory, must_exist=True)
        # TODO: FIX THIS TEST
        # plugin package filename
        plugin_filename = target_directory.joinpath(
            f"{md.name.lower()}-{md.version}{ext}"
        )
        if plugin_filename.exists():
            # plugin package does already exist
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

        return plugin_filename

    def install(
        self,
        plugin_filename: Union[str, Path],
        target_directory: Union[str, Path]
    ):
        """
        installs a plugin package from a given plugin file
        into the provided target directory

        :param plugin_filename: plugin filename
        :type plugin_filename: Union[str, Path]
        :param target_directory: target directory
        :type target_directory: Union[str, Path]
        :raises PluginPackageException: when plugin file does not exist
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
                target_directory = target_directory.joinpath(metadata.name)
                if target_directory.exists():
                    # plugin does already exist
                    raise PluginPackageException(
                        f"The plugin '{metadata.name}' does already "
                        f"exist in '{target_directory}'! Abort."
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

    def uninstall(
        self,
        plugin_name: str,
        target_directory: Union[str, Path]
    ):
        """
        uninstall plugin package from ginve target directory

        :param plugin_name: name of the plugin
        :type plugin_name: str
        :param target_directory: target directory of the plugins
        :type target_directory: Union[str, Path]
        :raises PluginPackageException:
        """
        if not target_directory is None:
            # target directory not set
            raise PluginPackageException(
                "The plugins directory '{target_directory}' is not "
                "set so that the plugin cannot be uninstalled! Abort."
            )

        # get plugin directory by its name
        plugin_directory = target_directory.joinpath(plugin_name)
        if not plugin_directory.exists():
            raise PluginPackageException(
                f"The plugin '{plugin_name}' is not installed "
                f"in '{target_directory}'! Abort."
            )

        # read metadata before, to check if valid plugin directory
        md = Metadata(plugin_directory)

        # remove the plugin directory
        log.debug(
            f"removing plugin directory '{plugin_directory}'..."
        )
        shutil.rmtree(plugin_directory)

    @classmethod
    def info(cls, plugin_filename: Union[str, Path]) -> Metadata:
        """
        show info about plugin package from metadata file

        :param plugin_filename: plugin filename
        :type plugin_filename: Union[str, Path]
        :raises PluginPackageException: if, plugin file is broken
        :return: metadata with information about the plugin
        :rtype: Metadata
        """
        assert isinstance(plugin_filename, (str, Path))

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
