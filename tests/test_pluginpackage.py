import pytest

from powerstrip.models.pluginpackage import PluginPackage
from powerstrip.exceptions import MetadataException, PluginPackageException
from .test_metadata import METADATA, METADATA_VALUES


class TestPluginPackage:
    def test_pack(self, tmp_path):
        # target directory where packed plugin files will be stored
        target_directory = tmp_path

        # invalid directory to pack
        with pytest.raises(AssertionError):
            PluginPackage.pack(None, None)

        # invalid directory, since not existing file
        with pytest.raises(ValueError):
            PluginPackage.pack("not_a_directory.txt", target_directory)

        # create temp path
        plugin_dir = tmp_path / "myplugin"
        plugin_dir.mkdir()

        # path exists, but metadata.yml is missing
        with pytest.raises(FileNotFoundError):
            PluginPackage.pack(plugin_dir, target_directory)

        # create metadata.yml file
        metadata_file = plugin_dir / "metadata.yml"
        metadata_file.write_text("")

        # missing fields in metadata.yml
        with pytest.raises(MetadataException):
            PluginPackage.pack(plugin_dir, target_directory)

        # write prepared metadata, but without values
        metadata_file.write_text(
            METADATA.format(**{k: "" for k in METADATA_VALUES})
        )

        # correct fields, but incorrect value types
        with pytest.raises(TypeError):
            PluginPackage.pack(plugin_dir, target_directory)

        # write prepared metadata, but without values
        metadata_file.write_text(
            METADATA.format(**{k: k for k in METADATA_VALUES})
        )

        # correct fields, but wrong values for validation
        with pytest.raises(MetadataException):
            PluginPackage.pack(plugin_dir, target_directory)

        # finally, write correct key, value pairs
        metadata_file.write_text(
            METADATA.format(**METADATA_VALUES)
        )

        # path exists, but target directory does not exist
        with pytest.raises(ValueError):
            PluginPackage.pack(plugin_dir, "target_directory_does_not_exist")

        # correct fields with correct values
        plugin_filename = PluginPackage.pack(plugin_dir, target_directory)

        # plugin package does already exist
        with pytest.raises(PluginPackageException):
            PluginPackage.pack(plugin_dir, target_directory)

        # get info of plugin package with invalid filename
        with pytest.raises(AssertionError):
            PluginPackage.info(None)

        # get info of plugin package with invalid filename
        with pytest.raises(ValueError):
            PluginPackage.info("not_existing_package.psp")

        # get info of valid plugin package
        metadata = PluginPackage.info(plugin_filename)

        # installation directory
        install_directory = tmp_path.joinpath("instdir/")
        install_directory.mkdir()

        # invalid plugin filename
        with pytest.raises(AssertionError):
            PluginPackage.install(None, None)

        # invalid installation path type
        with pytest.raises(AssertionError):
            PluginPackage.install(plugin_filename, None)

        # invalid installation path
        with pytest.raises(ValueError):
            PluginPackage.install(plugin_filename, "doesnotexist/")

        # install plugin to directory
        plugin_dir = PluginPackage.install(
            plugin_filename, install_directory
        )
        assert plugin_dir.joinpath("metadata.yml").exists()

        # plugin is already installed
        with pytest.raises(PluginPackageException):
            PluginPackage.install(
                plugin_filename, install_directory
            )

        # uninstall plugin
        PluginPackage.uninstall(
            METADATA_VALUES["name"], install_directory
        )

        # install plugin to directory with category
        plugin_dir = PluginPackage.install(
            plugin_filename, install_directory, use_category=True
        )
        assert plugin_dir.joinpath("metadata.yml").exists()

        # uninstall plugin
        PluginPackage.uninstall(
            METADATA_VALUES["name"], install_directory, "category"
        )
