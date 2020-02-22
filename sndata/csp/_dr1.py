#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the CSP DR1 API"""

from pathlib import Path
from typing import List, Union

from astropy.table import Table, vstack

from .. import _utils as utils
from ..base_classes import SpectroscopicRelease


def _read_file(path: Union[str, Path]) -> (float, float, Table):
    """Read a file path of spectroscopic data from CSP DR1

    Args:
        path (str or Path): Path of file to read

    Returns:
        - The data of maximum for the observed target
        - The redshift of the target
        - An astropy table with file data and meta data
    """

    # Handle the single file with a different data model:
    # There are three columns instead of two
    path = Path(path)
    if path.stem == 'SN07bc_070409_b01_BAA_IM':
        data = Table.read(path, format='ascii', names=['wavelength', 'flux', '_'])
        data.remove_column('_')

    else:
        data = Table.read(path, format='ascii', names=['wavelength', 'flux'])

    # Get various data from the table meta data
    file_comments = data.meta['comments']
    redshift = float(file_comments[1].lstrip('Redshift: '))
    max_date = float(file_comments[2].lstrip('JDate_of_max: '))
    obs_date = float(file_comments[3].lstrip('JDate_of_observation: '))
    epoch = float(file_comments[4].lstrip('Epoch: '))

    # Add remaining columns. These values are constant for a single file
    # (i.e. a single spectrum) but vary across files (across spectra)
    _, _, w_range, telescope, instrument = path.stem.split('_')
    data['date'] = obs_date
    data['epoch'] = epoch
    data['wavelength_range'] = w_range
    data['telescope'] = telescope
    data['instrument'] = instrument

    # Ensure dates are in JD format
    data['date'] = utils.convert_to_jd(data['date'])
    return max_date, redshift, data


class DR1(SpectroscopicRelease):
    """The ``DR1`` class provides access to spectra from the first release of
    optical spectroscopic data of low-redshift Type Ia supernovae (SNe Ia) by
    the Carnegie Supernova Project. It includes 604 previously unpublished
    spectra of 93 SNe Ia. The observations cover a range of phases from 12 days
    before to over 150 days after the time of B-band maximum light.
    (Source: Folatelli et al. 2013)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    # General metadata
    survey_name = 'Carnegie Supernova Project'
    release = 'DR1'
    survey_abbrev = 'CSP'
    survey_url = 'https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1'
    publications = ('Folatelli et al. 2013',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2013ApJ...773...53F/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()

        # Local paths
        self._spectra_dir = self._data_dir / 'spectra' / 'CSP_spectra_DR1'
        self._table_dir = self._data_dir / 'tables'

        # Define urls for remote data
        self._spectra_url = 'https://csp.obs.carnegiescience.edu/data/CSP_spectra_DR1.tgz'
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJ/773/53'

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        utils.require_data_path(self._spectra_dir)
        files = self._spectra_dir.glob('SN*.dat')
        ids = ('20' + Path(f).name.split('_')[0].lstrip('SN') for f in files)
        return sorted(set(ids))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        out_table = Table(
            names=['date', 'wavelength', 'flux', 'epoch', 'wavelength_range',
                   'telescope', 'instrument'],
            dtype=[float, float, float, float, 'U3', 'U3', 'U2']
        )

        files = self._spectra_dir.rglob(f'SN{obj_id[2:]}_*.dat')
        if not files:
            raise ValueError(f'No data found for obj_id {obj_id}')

        for path in files:
            max_date, redshift, spectral_data = _read_file(path)
            out_table = vstack([out_table, spectral_data])

        # Add meta data
        out_table.meta['obj_id'] = obj_id
        out_table.meta['ra'] = None
        out_table.meta['dec'] = None
        out_table.meta['z'] = redshift
        out_table.meta['z_err'] = None
        del out_table.meta['comments']

        if format_table:
            out_table.rename_column('date', 'time')

        return out_table

    def download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        utils.download_tar(
            url=self._table_url,
            out_dir=self._table_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        # Download spectra
        utils.download_tar(
            url=self._spectra_url,
            out_dir=self._data_dir / 'spectra',
            mode='r:gz',
            force=force,
            timeout=timeout
        )
