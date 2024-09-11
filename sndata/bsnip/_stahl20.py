"""This module defines the BSNIP Stahl20 API"""

from typing import List

from astropy import units as u
from astropy.io import ascii
from astropy.io.ascii.core import InconsistentTableError
from astropy.table import Table, vstack

from ..base_classes import SpectroscopicRelease
from ..utils import unit_conversion, downloads, data_parsing


class Stahl20(SpectroscopicRelease):
    """The second data release of the Berkeley Supernova Ia Program
    (BSNIP), including 637 low-redshift optical spectra collected  between
    2009 and 2018. Targets include 626 spectra (of 242 objects) that are
    unambiguously classified as belonging to Type Ia supernovae (SNe Ia).
    Of these, 70 spectra of 30 objects are classified as spectroscopically
    peculiar and 79 SNe Ia (covered by 328 spectra) have complementary
    photometric coverage. The median SN in the data set has one epoch of
    spectroscopy, a redshift of 0.0208 (with a low of 0.0007 and high of
    0.1921), and is first observed spectroscopically 1.1 days after maximum
    light. (Source:  Stahl et al. 2020)

    Deviations from the standard UI:
        - Metadata such as object Ra, DEC, and redshifts are not included
          in the official data release files.
        - Reported error values may or may not be available depending on the
          particular published spectra.

    Cuts on returned data:
        - None
    """

    survey_name = 'Berkeley Supernova Ia Program'
    survey_abbrev = 'BSNIP'
    release = 'Stahl20'
    survey_url = 'http://heracles.astro.berkeley.edu/sndb/'
    publications = ('Stahl et al. 2020',)
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2020MNRAS.492.4325S/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._spectra_dir = self._data_dir / 'spectra'
        self._tables_dir = self._data_dir / 'tables'
        self._meta_data_path = self._data_dir / 'meta_data.yml'

        # Define urls / path for remote / local data.
        self._spectra_url = 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPdata2/spectra.tar.gz'
        self._tables_url = 'https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/tar.gz?J/MNRAS/492/4325'
        self._tables_dir = self._data_dir / 'tables'
        self._meta_table_url = 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPdata2/spectra.csv'
        self._meta_table_path = self._data_dir / 'spectra.csv'

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        tables = ['spectra']
        for file in self._tables_dir.glob('table*.dat'):
            table_id = file.stem[5:]
            if table_id.isnumeric():
                table_id = int(table_id)

            tables.append(table_id)

        return sorted(tables, key=str)

    def _load_table(self, table_id: str) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        if table_id == 'spectra':
            return Table.read(self._meta_table_path)

        readme_path = self._tables_dir / 'ReadMe'
        table_path = self._tables_dir / f'table{table_id}.dat'

        # The CDS readme has an incorrect data type for the second columns in tables a1 adn s1
        # As a workaround, we parse the file manually
        if table_id == 'a1':
            data = Table.read(
                table_path,
                format='ascii.fixed_width_no_header',
                delimiter=' ',
                col_starts=[0, 24, 35, 44, 53, 60, 62, 68, 76, 79, 85, 91],
                units=[None, '"Y:M:D"', u.deg, u.deg, None, None, u.mag, None, None, u.day, u.day, None],
                names=['Name', 'Discov', 'RAdeg', 'DEdeg', 'z', 'r_z', 'E(B-V)',
                       'Subtype', 'Nsp', 'fepoch', 'lepoch', 'References'])

        elif table_id == 's1':
            p1nm = u.CompositeUnit(0.1, [u.nm], [1])
            data = Table.read(
                table_path,
                format='ascii.fixed_width_no_header',
                delimiter=' ',
                col_starts=[0, 24, 39, 45, 47, 52, 58, 63, 68, 74, 79, 84, 90],
                units=[None, '"Y:M:D"', u.day, None, p1nm, p1nm, p1nm, p1nm, u.deg, None, u.s, None, None],
                names=['Name', 'UTDate', 'tLC', 'Inst', 'lambdamin', 'lambdamax',
                       'Resb', 'Resr', 'PA', 'Airmass', 'ExpTime', 'S/N', 'Ref'])

        else:
            data = ascii.read(str(table_path), format='cds', readme=str(readme_path))

        description_dict = data_parsing.parse_vizier_table_descriptions(readme_path)
        data.meta['description'] = description_dict[table_id]
        return data

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        obj_ids = self.load_table('spectra')['ObjName']
        return sorted(set(obj_ids))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        data_tables = []
        all_spectra_inventory = self.load_table('spectra')
        object_spectra_inventory = all_spectra_inventory[all_spectra_inventory['ObjName'] == obj_id]
        for row in object_spectra_inventory:
            path = self._spectra_dir / row['Filename']

            # Tables either have two or three columns
            try:
                table = Table.read(
                    str(path), format='ascii',
                    names=['wavelength', 'flux', 'fluxerr'])

            except InconsistentTableError:
                table = Table.read(
                    str(path), format='ascii',
                    names=['wavelength', 'flux'])

            if format_table:
                table['time'] = unit_conversion.convert_to_jd(row['UT_Date'], format='UT')
                table['instrument'] = row['Instrument']

            data_tables.append(table)

        meta_data = self.load_table('a1')
        object_meta_data = meta_data[meta_data['Name'] == obj_id][0]

        all_data = vstack(data_tables)
        all_data.sort('wavelength')
        all_data.meta['obj_id'] = obj_id
        all_data.meta['ra'] = object_meta_data['RAdeg']
        all_data.meta['dec'] = object_meta_data['DEdeg']
        all_data.meta['z'] = object_meta_data['z']
        all_data.meta['z_err'] = None

        # Return data with columns in a standard order
        return all_data

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        downloads.download_file(
            url=self._meta_table_url,
            destination=self._meta_table_path,
            force=force,
            timeout=timeout
        )

        downloads.download_tar(
            url=self._tables_url,
            out_dir=self._tables_dir,
            skip_exists=self._tables_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )

        downloads.download_tar(
            url=self._spectra_url,
            out_dir=self._data_dir,
            skip_exists=self._spectra_dir,
            mode='r:gz',
            force=force,
            timeout=timeout
        )
