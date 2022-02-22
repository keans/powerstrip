import tempfile
from pathlib import Path

import pytest

from powerstrip.models.metadata import Metadata
from powerstrip.exceptions import MetadataException
from powerstrip.utils.semver import SemVer


# dummy metadata file
METADATA = """---
uuid: {uuid}
name: {name}
description: {description}
license: {license}
version: {version}
author: {author}
url: {url}
category: {category}
tags: {tags}
"""

# values for the metadata
METADATA_VALUES = {
    "uuid": "deadbeef",
    "name": "MyPlugin",
    "description": "This is my description.",
    "license": "MIT",
    "version": "1.2.3",
    "author": "Foo Bar <foo.bar@example.com>",
    "url": "https://www.example.com",
    "category": "category",
    "tags": "bla, blup"
}

# temporary file
TEMP_FILE = Path(
    tempfile.NamedTemporaryFile(delete=False).name
).parent.joinpath("metadata.yml")


@pytest.fixture
def md():
    return Metadata()


class TestMetadata:
    def test_init(self, md: Metadata):
        # create valid metadata class instance on current directory
        assert isinstance(md, Metadata)

        print(md)

    def test_uuid(self, md: Metadata):
        # create valid metadata class
        assert md.uuid == ""

        # invalid type
        with pytest.raises(AssertionError):
            md.uuid = -1

        # None as valid uuid
        md.uuid = None
        assert md.uuid == ""

        # valid uuid
        md.uuid = "deadbeef"
        assert md.uuid == "deadbeef"

    def test_name(self, md: Metadata):
        # create valid metadata class
        assert md.name == ""

        # invalid type
        with pytest.raises(AssertionError):
            md.name = -1

        # None as valid name
        md.name = None
        assert md.name == ""

        # valid name
        md.name = "deadbeef"
        assert md.name == "deadbeef"

    def test_author(self, md: Metadata):
        # create valid metadata class
        assert md.author == ""

        # invalid type
        with pytest.raises(AssertionError):
            md.name = -1

        # None as valid author
        md.author = None
        assert md.author == ""

        # valid author
        md.author = "deadbeef"
        assert md.author == "deadbeef"

    def test_description(self, md: Metadata):
        # create valid metadata class
        assert md.description == ""

        # invalid type
        with pytest.raises(AssertionError):
            md.description = -1

        # None as valid description
        md.description = None
        assert md.description == ""

        # valid description
        md.description = "deadbeef"
        assert md.description == "deadbeef"

    def test_version(self, md: Metadata):
        # create valid metadata class
        assert isinstance(md.version, SemVer)

        # invalid type
        with pytest.raises(AssertionError):
            md.version = -1

        # invalid version string
        with pytest.raises(TypeError):
            md.version = "1.x.3bla"

        # correct assignment
        md.version = "1.2.3-rc3+20220208"
        assert str(md.version) == "1.2.3-rc3+20220208"

    def test_tags(self, md: Metadata):
        # create valid metadata class
        assert md.tags == []

        # invalid tag type
        with pytest.raises(AssertionError):
            md.tags = 1

        # set empty string, i.e., tags must be empty
        md.tags = ""
        assert md.tags == []

        # set None, i.e., tags must be empty
        md.tags = None
        assert md.tags == []

        # set 'one' string
        md.tags = "one"
        assert md.tags == ["one"]

        # set 'one' string with leading comma
        md.tags = ",one"
        assert md.tags == ["one"]

        # set 'one' string with trailing comma
        md.tags = "one,"
        assert md.tags == ["one"]

        # set 'one,two,three' string
        md.tags = "one,two,three"
        assert md.tags == ["one", "two", "three"]

        # set 'one,two,three' string with strange spaces
        md.tags = "  one,  two   ,  three "
        assert md.tags == ["one", "two", "three"]

        # set 'one,two,three' string with mixed cases
        md.tags = "one,TWO,Three"
        assert md.tags == ["one", "two", "three"]

    def test_category(self, md: Metadata):
        # create valid metadata class
        assert md.category == "default"

        # invalid type
        with pytest.raises(AssertionError):
            md.category = -1

        # None as valid category
        md.category = None
        assert md.category == "default"

        # valid category
        md.category = "deadbeef"
        assert md.category == "deadbeef"

    def test_url(self, md: Metadata):
        # create valid metadata class
        assert md.url == ""

        # invalid type
        with pytest.raises(AssertionError):
            md.url = -1

        # None as valid url
        md.url = None
        assert md.url == ""

        # valid url
        md.url = "deadbeef"
        assert md.url == "deadbeef"

    def test_dict(self, md: Metadata):
        for field in (
            'uuid', 'name', 'author', 'description', 'version',
            'category', 'url', 'tags'
        ):
            assert field in md.dict

    def test_from_dict(self, md: Metadata):
        # invalid parameter type
        with pytest.raises(AssertionError):
            md.from_dict(None)

        # dict, but missing parameters
        with pytest.raises(MetadataException):
            md.from_dict({})

        # correct input value
        md.from_dict(METADATA_VALUES)

    def test_create_from_dict(self):
        # not a valid dictionary type
        with pytest.raises(AssertionError):
            md = Metadata.create_from_dict(None)

        # create new instance based on given dictionary
        md = Metadata.create_from_dict(METADATA_VALUES)
        assert isinstance(md, Metadata)

    def test_get_filename(self, md: Metadata):
        # get valid filename from current directory
        assert isinstance(md.get_filename(), Path)
        assert isinstance(md.get_filename("."), Path)

        # get filename with invalid type
        for value in (-1, None):
            with pytest.raises(AssertionError):
                md.get_filename(value)

        # get filename with invalid type
        with pytest.raises(ValueError):
            md.get_filename("directory_does_not_exist")

    def test_save_and_load(self, md: Metadata):
        # invalid file object type
        with pytest.raises(AssertionError):
            md.save(None)

        # save some dummy data
        md.from_dict(METADATA_VALUES)
        with TEMP_FILE.open("w") as f:
            md.save(f)

        # create new instance for loading
        md = Metadata()

        # wrong file object type for loading
        with pytest.raises(AssertionError):
            md.load(None)

        # correct file object type
        with TEMP_FILE.open("r") as f:
            md.load(f)

        # ensure that saved and loaded data equals original input data
        assert all([
            (md.dict[k], METADATA_VALUES[k])
            for k in METADATA_VALUES
        ])
        print(md)

        # read file again from directory
        md2 = md.create_from_directory(TEMP_FILE.parent)

        # ensure that saved and loaded data equals original input data
        assert all([
            (md2.dict[k], METADATA_VALUES[k])
            for k in METADATA_VALUES
        ])

    def test_create_from_f(self):
        # not a valid file object type
        with pytest.raises(AssertionError):
            md = Metadata.create_from_f(None)

        # save some dummy data
        md = Metadata()
        md.from_dict(METADATA_VALUES)
        with TEMP_FILE.open("w") as f:
            md.save(f)

        # create new instance based on given file object
        with TEMP_FILE.open("r") as f:
            md = Metadata.create_from_f(f)
            assert isinstance(md, Metadata)
