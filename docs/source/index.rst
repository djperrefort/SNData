SNData
======

**SNData** provides access to data releases published by a variety of
supernova (SN) surveys. It is designed to support the development of scalable
analysis pipelines that translate with minimal effort between and across data
sets. A summary of accessible data is provided below. Access to additional
surveys is added upon request or as needed for individual research projects
undertaken by the developers. To request an additional survey / data release,
please raise an issue on `GitHub`_.

.. _GitHub: https://github.com/djperrefort/sndata


Using These Docs
----------------

**SNData** is designed to provide as consistent of an interface as possible
across surveys. The *Getting Started* guides are intended to help you get up
and running quickly and to familiarize you with the general **SNData**
interface. Additional API documentation is provided for each individual
data set to highlight any (very) minor deviations a particular survey or
data release may have from the rest of the package. In general you should:

1. Read the installation guide (~1 minute if you know how to use ``pip``)
2. Read the quick start guide to learn how the package works (~5 minutes)
3. Read the slow start guide for a better understanding of the available
   features and how they can make your life easier (~10 minutes)
4. Refer to the API documentation for a given survey as you see necessary


Available Data
--------------

SNData provides data access for the following supernova surveys. If you are
having issues downloading data for a particular survey or data release, please
check the `Server Status Page`_.

+------------------------------------------------------+------------------------------+---------------+
| Survey Name                                          | Data Release                 | Data Type     |
+======================================================+==============================+===============+
| Berkeley Supernova Ia Program                        | `Stahl et al. 2020`_         | Spectroscopic |
+------------------------------------------------------+------------------------------+---------------+
|                                                      | `DR1`_                       | Spectroscopic |
+ Carnegie Supernova Project                           +------------------------------+---------------+
|                                                      | `DR3`_                       | Photometric   |
+------------------------------------------------------+------------------------------+---------------+
| Dark Energy Survey                                   | `SN3YR`_                     | Photometric   |
+------------------------------------------------------+------------------------------+---------------+
+ Equation of State: Supernovae Trace Cosmic Expansion | `Narayan et al. 2016`_       | Photometric   |
+------------------------------------------------------+------------------------------+---------------+
+ Joint Light-Curve Analysis                           | `Betoule et al. 2014`_       | Photometric   |
+------------------------------------------------------+------------------------------+---------------+
+ Lick Observatory Supernova Search                    | `Ganeshalingam et al. 2013`_ | Photometric   |
+------------------------------------------------------+------------------------------+---------------+
|                                                      | `Sako et al. 2018`_          | Photometric   |
+ Sloan Digital Sky Survey                             +------------------------------+---------------+
|                                                      | `Sako et al. 2018`_          | Spectroscopic |
+------------------------------------------------------+------------------------------+---------------+
+ Supernova Legacy Survey                              | `Balland et al. 2009`_       | Spectroscopic |
+------------------------------------------------------+------------------------------+---------------+
+ Sweetspot                                            | `Weyant et al. 2018`_        | Photometric   |
+------------------------------------------------------+------------------------------+---------------+


.. _Stahl et al. 2020: https://ui.adsabs.harvard.edu/abs/2012MNRAS.425.1789S/abstract
.. _Server Status Page: https://stats.uptimerobot.com/gQ8lkslGWO
.. _DR1: https://csp.obs.carnegiescience.edu/news-items/CSP_spectra_DR1
.. _DR3: https://csp.obs.carnegiescience.edu/news-items/csp-dr3-photometry-released
.. _SN3YR: https://des.ncsa.illinois.edu/releases/sn
.. _Narayan et al. 2016: http://www.ctio.noao.edu/essence/
.. _Betoule et al. 2014: https://ui.adsabs.harvard.edu/abs/2014A%26A...568A..22B/abstract
.. _Sako et al. 2018: http://data.darkenergysurvey.org/sdsssn/dataRelease/
.. _Balland et al. 2009: https://ui.adsabs.harvard.edu/abs/2009A%26A...507...85B/abstract
.. _Stahl et al. 2019: https://ui.adsabs.harvard.edu/abs/2019MNRAS.490.3882S/abstract
.. _Ganeshalingam et al. 2013: https://ui.adsabs.harvard.edu/abs/2019MNRAS.490.3882S/abstract
.. _Weyant et al. 2018: https://ui.adsabs.harvard.edu/abs/2018AJ....155..201W/abstract/

.. toctree::
   :hidden:
   :maxdepth: 0

   Overview<self>
   change_log

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Getting Started:

   getting_started/installation
   getting_started/quick_start
   getting_started/slow_start
   getting_started/combining_datasets
   getting_started/custom_classes

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Data Releases:

   module_docs/bsnip
   module_docs/csp
   module_docs/des
   module_docs/essence
   module_docs/jla
   module_docs/loss
   module_docs/sdss
   module_docs/snls
   module_docs/sweetspot

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Package API:

   package_api/sndata
   package_api/base_classes
   package_api/utils
   package_api/utils.data_parsing.rst
   package_api/utils.downloads.rst
   package_api/utils.unit_conversion.rst
   package_api/utils.wrappers.rst
