"""Tests for the ``bsnip.Stahl20`` module."""

from unittest import TestCase

from sndata.bsnip import Stahl20
from ..common_tests import SpectroscopicDataParsing, SpectroscopicDataUI, download_data_or_skip

download_data_or_skip(Stahl20())


class Stahl20Parsing(TestCase, SpectroscopicDataParsing):
    """Data parsing tests for the Stahl20 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Stahl20()


class Stahl20UI(TestCase, SpectroscopicDataUI):
    """UI tests for the Stahl20 release"""

    @classmethod
    def setUpClass(cls):
        cls.test_class = Stahl20()
