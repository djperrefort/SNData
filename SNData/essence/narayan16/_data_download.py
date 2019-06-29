#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

import shutil

from . import _meta as meta
from ... import _utils as utils


def download_module_data(force=False):
    """Download data for the current survey / data release

    Args:
        force (bool): Re-Download locally available data (Default: False)
    """

    if force or not meta.vizier_dir.exists():
        print('Downloading tables and photometry...')
        utils.download_tar(
            url=meta.table_url,
            out_dir=meta.vizier_dir,
            mode='r:gz')

    if force or not meta.filter_dir.exists():
        print('Downloading tables and photometry...')
        utils.download_file(
            url=meta.i_filter_url,
            out_file=meta.filter_dir / 'I_band.dat')

        utils.download_file(
            url=meta.r_filter_url,
            out_file=meta.filter_dir / 'R_band.dat')


def delete_module_data():
    """Delete any data for the current survey / data release"""

    try:
        shutil.rmtree(meta.data_dir)

    except FileNotFoundError:
        pass
