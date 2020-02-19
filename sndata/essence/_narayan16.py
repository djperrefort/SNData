#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the Essence Narayan16 API"""

from pathlib import Path

import numpy as np
from astropy.table import Table

from .. import _utils as utils
from .._base import DataRelease
from ..exceptions import InvalidObjId


def _format_table(data_table: Table):
    """Format a data table for use with SNCosmo

    Args:
        data_table: A data table returned by ``get_data_for_id``

    Returns:
        The same data in a new table following the SNCosmo data model
    """

    out_table = Table()
    out_table.meta = data_table.meta

    out_table['time'] = data_table['JD']
    out_table['band'] = ['csp_dr3_' + band for band in data_table['Passband']]
    out_table['zp'] = np.full(len(data_table), 25)
    out_table['zpsys'] = np.full(len(data_table), 'ab')
    out_table['flux'] = data_table['Flux']
    out_table['fluxerr'] = np.max(
        [data_table['Fluxerr_hi'], data_table['Fluxerr_lo']], axis=0)

    return out_table


class Narayan16(DataRelease):
    """The ``Narayan16`` class provides access to photometric data for 213
    Type Ia supernovae discovered by the ESSENCE survey at redshifts
    0.1 <= z <= 0.81 between 2002 and 2008. It includes R and I band photometry
    measured from images obtained using the MOSAIC II camera at the CTIO
    Blanco telescope. (Source: Narayan et al. 2016)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None

    Attributes:
        - survey_name
        - release
        - survey_abbrev
        - survey_url
        - data_type
        - publications
        - ads_url
        - band_names
        - zero_point
        - lambda_effective

    Methods:
        - delete_module_data
        - download_module_data
        - get_available_ids
        - get_available_tables
        - get_data_for_id
        - iter_data
        - load_table
    """

    # General metadata
    survey_name = 'Equation of State: Supernovae trace Cosmic Expansion'
    survey_abbrev = 'ESSENCE'
    release = 'narayan16'
    survey_url = 'http://www.ctio.noao.edu/essence/'
    data_type = 'photometric'
    publications = ('Narayan et al. 2016',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2016ApJS..224....3N/abstract'

    # Photometric metadata (Required for photometric data, otherwise delete)
    band_names = ('essence_narayan16_R', 'essence_narayan16_I')
    lambda_effective = (6440, 8050)
    zero_point = tuple(27.5 for _ in band_names)

    def __init__(self):
        # Define local paths of published data
        self._find_or_create_data_dir()
        self._table_dir = self.data_dir / 'vizier'
        self._photometry_dir = self._table_dir / 'lcs'
        self._filter_dir = self.data_dir / 'filters'

        # Define urls for remote data
        self._table_url = 'http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/tar.gz?J/ApJS/224/3'
        self._r_filter_url = 'https://www.noao.edu/kpno/mosaic/filters/asc6004.f287.r04.txt'
        self._i_filter_url = 'https://www.noao.edu/kpno/mosaic/filters/asc6028.f287.r04.txt'
        self._filter_file_names = ('R_band.dat', 'I_band.dat')

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey"""

        utils.require_data_path(self._photometry_dir)
        files = self._photometry_dir.glob('*.dat')
        return sorted(Path(f).name.split('.')[0] for f in files)

    # noinspection PyUnusedLocal
    def _get_data_for_id(self, obj_id: str, format_table: bool = True):
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        if obj_id not in self.get_available_ids():
            raise InvalidObjId()

        path = self._photometry_dir / f'{obj_id}.W6yr.clean.nn2.Wstd.dat'
        data_table = Table.read(
            path, format='ascii',
            names=['Observation', 'MJD', 'Passband', 'Flux', 'Fluxerr_lo',
                   'Fluxerr_hi']
        )

        data_table['JD'] = utils.convert_to_jd(data_table['MJD'])

        # Get meta data
        with open(path) as infile:
            keys = infile.readline().lstrip('# ').split()
            vals = infile.readline().lstrip('# ').split()

        for k, v in zip(keys, vals):
            data_table.meta[k] = v

        # Enforce uniformity across package
        data_table.meta['obj_id'] = data_table.meta.pop('objid')

        # Remove column names from table comments
        del data_table.meta['comments']

        if format_table:
            data_table = _format_table(data_table)

        return data_table

    def download_module_data(self, force: bool = False):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data (Default: False)
        """

        if (force or not self._table_dir.exists()) \
                and utils.check_url(self._table_url):
            print('Downloading tables and photometry...')
            utils.download_tar(
                url=self._table_url,
                out_dir=self._table_dir,
                mode='r:gz')

        if (force or not self._filter_dir.exists()) \
                and utils.check_url(self._i_filter_url):
            print('Downloading tables and photometry...')
            utils.download_file(
                url=self._i_filter_url,
                out_file=self._filter_dir / 'I_band.dat')

            utils.download_file(
                url=self._r_filter_url,
                out_file=self._filter_dir / 'R_band.dat')
