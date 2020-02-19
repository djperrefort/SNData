#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the <INSERT DATA RELEASE NAME> API"""

from sndata import _utils as utils
from sndata._base import DataRelease


class DataReleaseName(DataRelease):
    """<Describe the data set>

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

    Methods:
        - delete_module_data
        - download_module_data
        - get_available_ids
        - get_available_tables
        - get_data_for_id
        - iter_data
        - load_table
    """

    # General metadata (Required)
    survey_name = None
    survey_abbrev = None
    release = None
    survey_url = None
    data_type = None
    publications = (None,)
    ads_url = None

    # Photometric metadata (Required for photometric data, otherwise delete)
    band_names = tuple()
    zero_point = tuple()
    lambda_effective = tuple()

    def __init__(self):
        # Define local paths of published data
        self._find_or_create_data_dir()
        self.table_dir = self.data_dir / 'tables'  # Paper tables
        self.spectra_dir = self.data_dir / 'spectra'

        # Define urls for remote data
        self.data_url = 'some.url.gov'

    def register_filters(self, force=False):
        """Register filters for this survey / data release with SNCosmo

        Args:
            force: Re-register a band if already registered
        """

        pass

    def _get_available_tables(self):
        """Get available Ids for tables published by the paper for this data
        release"""

        table_nums = []
        return sorted(table_nums)  # The returned Id's should be sorted

    def _load_table(self, table_id):
        """Return a table from the data paper for this survey / data

        Args:
            table_id: The published table number or table name
        """

        pass

    def _get_available_ids(self):
        """Return a list of target object IDs for the current survey"""

        ids = []
        return sorted(set(ids))  # The return should be a sorted, unique list

    # noinspection PyUnusedLocal
    def _get_data_for_id(self, obj_id: str, format_table: bool = True):
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        pass

    def download_module_data(self, force: bool = False):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data (Default: False)
        """

        # Example for downloading uncompressed files
        if (force or not self.table_dir.exists()) \
                and utils.check_url(self.data_url):
            print('Downloading data tables...')
            utils.download_tar(
                url=self.data_url,
                out_dir=self.table_dir,
                mode='r:gz')

        # Example for downloading .tar.gz files
        if (force or not self.spectra_dir.exists())\
                and utils.check_url(self.data_url):
            print('Downloading something else...')
            utils.download_tar(
                url=self.data_url,
                out_dir=self.data_dir,
                mode='r:gz')
