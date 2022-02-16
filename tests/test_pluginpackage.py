import pytest

from powerstrip.models.pluginpackage import PluginPackage
from powerstrip.exceptions import MetadataException, PluginPackageException
from .test_metadata import METADATA, METADATA_VALUES


class TestPluginPackage:
    def test_init(self):
        # invalid plugin filename
        with pytest.raises(AssertionError):
            pp = PluginPackage(42)

        # create plugin package without parameters
        pp = PluginPackage()
        assert isinstance(pp, PluginPackage)

        # create plugin package with None filename
        pp = PluginPackage(None)
        assert isinstance(pp, PluginPackage)

        # create plugin package with filename
        pp = PluginPackage("foo.pkg")
        assert isinstance(pp, PluginPackage)

    def test_pack(self, tmp_path):
        # target directory where packed plugin files will be stored
        target_directory = tmp_path

        # prepare plugin package without filename
        pp = PluginPackage()

        # invalid directory to pack
        with pytest.raises(AssertionError):
            pp.pack(None, None)

        # invalid directory, since not existing file
        with pytest.raises(ValueError):
            pp.pack("not_a_directory.txt", target_directory)

        # create temp path
        plugin_dir = tmp_path / "myplugin"
        plugin_dir.mkdir()

        # path exists, but metadata.yml is missing
        with pytest.raises(FileNotFoundError):
            pp.pack(plugin_dir, target_directory)

        # create metadata.yml file
        metadata_file = plugin_dir / "metadata.yml"
        metadata_file.write_text("")

        # missing fields in metadata.yml
        with pytest.raises(MetadataException):
            pp.pack(plugin_dir, target_directory)

        # write prepared metadata, but without values
        metadata_file.write_text(
            METADATA.format(**{k: "" for k in METADATA_VALUES})
        )

        # correct fields, but incorrect value types
        with pytest.raises(TypeError):
            pp.pack(plugin_dir, target_directory)

        # write prepared metadata, but without values
        metadata_file.write_text(
            METADATA.format(**{k: k for k in METADATA_VALUES})
        )

        # correct fields, but wrong values for validation
        with pytest.raises(MetadataException):
            pp.pack(plugin_dir, target_directory)

        # finally, write correct key, value pairs
        metadata_file.write_text(
            METADATA.format(**METADATA_VALUES)
        )

        # path exists, but target directory does not exist
        with pytest.raises(ValueError):
            pp.pack(plugin_dir, "target_directory_does_not_exist")

        # correct fields with correct values
        plugin_filename = pp.pack(plugin_dir, target_directory)

        # plugin package does already exist
        with pytest.raises(PluginPackageException):
            pp.pack(plugin_dir, target_directory)

        # get info of plugin package with invalid filename
        with pytest.raises(AssertionError):
            pp.info(None)

        # get info of plugin package with invalid filename
        with pytest.raises(ValueError):
            pp.info("not_existing_package.psp")

        # get info of valid plugin package
        metadata = pp.info(plugin_filename)
