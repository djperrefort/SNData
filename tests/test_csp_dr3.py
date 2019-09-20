#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""Tests for the ``csp.dr3`` module."""

from sndata import csp
from base_tests import DataParsingTestBase, DocumentationTestBase


class DataParsing(DataParsingTestBase):
    """Tests for the csp.dr3 module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3
        cls.module.download_module_data(force=True)

    def test_no_empty_data_tables(self):
        self._test_no_empty_data_tables(10)

    def test_paper_tables_are_parsed(self):
        self._test_paper_tables_are_parsed()

    def test_ids_are_sorted(self):
        self._test_ids_are_sorted()

    def test_get_zp(self):
        self._test_get_zp()

    def test_jd_time_format(self):
        self._test_jd_time_format()

    def test_sncosmo_column_names(self):
        self._test_sncosmo_column_names()

    def test_sncosmo_registered_band_names(self):
        self._test_sncosmo_registered_band_names()

    def correct_data_for_2005el(self):
        """Test a handful of measurements for 2005el match values in
        Krisciunas et al. 2017"""

        self.fail()


class Documentation(DocumentationTestBase):
    """Tests for the des.SN3YR module"""

    @classmethod
    def setUpClass(cls):
        cls.module = csp.dr3

    def test_consistent_docs(self):
        self._test_consistent_docs()

    def test_ads_url(self):
        self._test_ads_url_status()

    def test_survey_url(self):
        self._test_survey_url_status()

