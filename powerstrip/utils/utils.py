from typing import Union
from pathlib import Path

from importlib_metadata import pathlib


def ensure_path(
    path: Union[str, Path], must_exist: bool = False
) -> Path:
    """
    ensures that given path is of type Path
    and that HOME directory is resolved
    """
    path = (
        path
        if isinstance(path, Path) else
        Path(path)
    ).expanduser()

    if must_exist and not path.exists():
        # path does not exist
        raise ValueError(
            f"The directory '{path}' does not exist!"
        )

    return path
