"""The ``data_parsing`` module provides file parsing tools for any file formats
used by multiple astronomical surveys and / or data releases. It is also
responsible for locating and registering data located on the local machine.
"""

import os
from pathlib import Path
from typing import Union

import numpy as np
import sncosmo

from ..exceptions import NoDownloadedData


def require_data_path(*data_dirs: Path):
    """Raise NoDownloadedData exception if given paths don't exist

    Args:
        *data_dirs: Path objects to check exists
    """

    for data_dir in data_dirs:
        if not data_dir.exists():
            raise NoDownloadedData()


def find_data_dir(survey_abbrev: str, release: str) -> Path:
    """Determine the directory where data files are stored for a data release

    If the directory does not exist, create it.

    Args:
        survey_abbrev: Abbreviation of the survey to load data for (e.g., CSP)
        release: Name of the data release from the survey (e.g., DR1)

    Returns:
        The path of the directory where
    """

    # Enforce the use of lowercase file names
    safe_survey = survey_abbrev.lower().replace(' ', '_')
    safe_release = release.lower().replace(' ', '_')

    # Default to using data directory specified in the environment
    if 'SNDATA_DIR' in os.environ:
        base_dir = Path(os.environ['SNDATA_DIR']).resolve()

    else:
        base_dir = Path(__file__).resolve().parent.parent / 'data'

    data_dir = base_dir / safe_survey / safe_release
    return data_dir


def parse_vizier_table_descriptions(readme_path: Union[Path, str]):
    """Returns the table descriptions from a vizier readme file

    Args:
        readme_path: Path of the file to read

    Returns:
        A dictionary {<Table number (int)>: <Table description (str)>}
    """

    table_descriptions = dict()
    with open(readme_path) as ofile:

        # Skip lines before table summary
        line = next(ofile)
        while line.strip() != 'File Summary:':
            line = next(ofile)

        # Skip table header
        for _ in range(5):
            line = next(ofile)

        # Iterate until end of table marker
        while not line.startswith('---'):
            line_list = line.split()
            table_num = line_list[0][len('table'):].rstrip('.dat')
            if table_num.isdigit():
                table_num = int(table_num)

            table_desc = ' '.join(line_list[3:])
            line = next(ofile)

            # Keep building description for multiline descriptions
            while line.startswith(' '):
                table_desc += ' ' + line.strip()
                line = next(ofile)

            table_descriptions[table_num] = table_desc

    return table_descriptions


def register_filter_file(file_path: str, filter_name: str, force: bool = False):
    """Registers filter profiles with sncosmo if not already registered

    Assumes the file at ``file_path`` is a two column, white space delimited
    ascii table.

    Args:
        file_path: Path of ascii table with wavelength (Ang) and transmission
        filter_name: The name of the registered filter.
        force: Whether to re-register a band if already registered
    """

    # Get set of registered builtin and custom band passes
    # noinspection PyProtectedMember
    available_bands = set(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._loaders)

    # noinspection PyProtectedMember
    available_bands.update(
        k[0] for k in sncosmo.bandpasses._BANDPASSES._instances)

    # Register the new bandpass
    if filter_name not in available_bands:
        wave, trans = np.genfromtxt(file_path).T
        is_good_data = ~np.isnan(wave) & ~np.isnan(trans)
        band = sncosmo.Bandpass(wave[is_good_data], trans[is_good_data])
        band.name = filter_name
        sncosmo.register(band, force=force)
