from pathlib import Path as _Path

from single_version import get_version as _get_version

from .cli import cli

__version__ = _get_version(__name__, _Path(__file__).parent.parent)
