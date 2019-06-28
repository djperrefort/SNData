#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for downloading data."""

from . import _meta as meta
from ... import _utils as utils


def download_module_data():
    """Download data for the current survey / data release"""

    if not meta.filter_dir.exists():
        print('Downloading filters...')
        utils.download_tar(
            url=meta.filter_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if not meta.photometry_dir.exists():
        print('Downloading photometry...')
        utils.download_tar(
            url=meta.photometry_url,
            out_dir=meta.data_dir,
            mode='r:gz')

    if not meta.fits_dir.exists():
        print('Downloading Light-Curve Fits...')
        utils.download_tar(
            url=meta.fits_url,
            out_dir=meta.data_dir,
            mode='r:gz')


def delete_module_data():
    """Delete any data for the current survey / data release"""

    import shutil

    try:
        shutil.rmtree(meta.data_dir)

    except FileNotFoundError:
        pass
