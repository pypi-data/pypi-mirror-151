"""Flake8 extension to add pyproject.toml support."""

from __future__ import annotations

import configparser
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

from flake8.options import config  # type: ignore

if sys.version_info < (3, 11):  # pragma: no cover
    import tomli as tomllib
else:  # pragma: no cover
    import tomllib

if TYPE_CHECKING:
    from typing import Generator, TextIO


class Dummy:  # pylint: disable=too-few-public-methods
    """Dummy class used as reporter entry point."""


class ConfigParser(configparser.RawConfigParser):
    """Add toml support to flake8's config parser."""

    def _read(self, fp: TextIO, fpname: str) -> None:
        if Path(fpname).name == 'pyproject.toml':
            if cfg := tomllib.load(fp.buffer).get('tool', {}).get('flake8'):
                if not self.has_section('flake8'):
                    self.add_section('flake8')
                for key, value in cfg.items():
                    value = str(value) if isinstance(value, bool) else value
                    self.set('flake8', key, value)
            return
        super()._read(fp, fpname)  # type: ignore


_generate_possible_local_files = config.ConfigFileFinder.generate_possible_local_files


def generate_possible_local_files(cff: config.ConfigFileFinder) -> Generator[str, None, None]:
    """Find and generate all local config files."""
    cff.project_filenames = cff.project_filenames + ('pyproject.toml',)
    yield from _generate_possible_local_files(cff)


patched_configparser = ModuleType('configparser')
patched_configparser.ParsingError = configparser.ParsingError  # type: ignore
patched_configparser.RawConfigParser = ConfigParser  # type: ignore
config.configparser = patched_configparser
config.ConfigFileFinder.generate_possible_local_files = generate_possible_local_files
