import logging
import sys
import importlib
from pathlib import Path


# prepare logger
log = logging.getLogger(__name__)


def load_module(module_name: str, directory: Path):
    """
    load module by name from given directory
    """
    assert isinstance(module_name, str)
    assert isinstance(directory, Path)

    # get modules spec
    log.debug(
        f"getting specs for module '{module_name}' in "
        f"'{directory.as_posix()}'..."
    )
    spec = importlib.util.spec_from_file_location(
        name=module_name, location=directory.as_posix()
    )

    # get module from spec
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod

    # load the module
    spec.loader.exec_module(mod)
