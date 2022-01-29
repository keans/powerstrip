import logging
from pathlib import Path
from typing import Union
from io import TextIOWrapper

import yaml

from powerstrip.cerberusutils.customvalidator import CustomValidator
from powerstrip.cerberusutils.schema import plugin_metadata_schema
from powerstrip.exceptions import MetadataException
from powerstrip.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


class Metadata:
    """
    metadata class
    """
    METADATA_FILENAME = "metadata.yml"

    def __init__(
        self, plugin_directory: Union[str, Path] = ".",
        auto_load: bool = True
    ):
        self.plugin_directory = ensure_path(plugin_directory)
        self.validator = CustomValidator(plugin_metadata_schema)

        if auto_load:
            # load metadata file
            self.load()

    @property
    def filename(self) -> Path:
        """
        returns complete filename
        """
        return self.plugin_directory.joinpath(self.METADATA_FILENAME)

    @property
    def plugin_name(self) -> str:
        """
        derive plugin name from meta data
        """
        return f"{self.name}-{self.version}"

    def _load_from_f_obj(self, f):
        """
        load YAML from file, validate the input
        and set internal properties
        """
        y = yaml.safe_load(f) or {}
        if not self.validator.validate(y):
            # invalid content => raise exception with errors
            raise MetadataException(self.validator.errors)

        # set internal properties
        for k,v in y.items():
            setattr(self, k, v)

    def load(self):
        """
        load metadata from file
        """
        if not self.filename.exists():
            # meta data file does not exist
            raise MetadataException(
                f"The metadata file '{self.filename}' does not exist!"
            )

        # load metadata file
        log.debug(f"Loading '{self.filename}'...")
        with self.filename.open() as f:
            self._load_from_f_obj(f)

    @staticmethod
    def create_from_f_obj(
        f, plugin_directory: Union[str, Path] = "."
    ):
        """
        create metadata instance from file object
        """
        metadata = Metadata(plugin_directory=plugin_directory)
        metadata._load_from_f_obj(f)

        return metadata

    def __repr__(self) -> str:
        return (
            f"<Metadata(uuid='{self.uuid}', name='{self.name}', "
            f"description='{self.description}', version='{self.version}', "
            f"url='{self.url}')>"
        )
