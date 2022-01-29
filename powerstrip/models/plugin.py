import abc
import sys
from pathlib import Path

from powerstrip.models.metadata import Metadata


class Plugin(abc.ABC):
    """
    abstract class from which all plugins
    must derived
    """
    def __init__(self, auto_load_metadata: bool = True):
        # get plugin path from module file
        self.plugin_path = Path(
            sys.modules[self.__module__].__file__
        ).parent

        # get plugin's metadata
        self.metadata = Metadata(self.plugin_path, auto_load_metadata)

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}(metadata='{self.metadata}')>"
        )
