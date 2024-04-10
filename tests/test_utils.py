import unittest

import xarray

from downloader.utils import city_mapping, convert_csv_to_netcdf, netcdf_filter_columns


class TestNetCDF(unittest.TestCase):
    def test_csv_to_netcdf(self):
        file_name = "tests/meteofrance_mf_1969_2022.csv"

        metadata = {"A": 1, "B": 2}

        xr = convert_csv_to_netcdf(file_name, metadata)
        self.assertDictEqual(xr.attrs, metadata)

    def test_select_columns(self):
        file_name = "tests/meteofrance_mf_1969_2022.nc"
        xr = xarray.open_dataset(file_name)

        self.assertIn("LAMBX (hm)", xr.variables)
        self.assertIn("LAMBY (hm)", xr.variables)
        self.assertIn("NUMERO", xr.variables)
        self.assertIn("DATE", xr.variables)
        self.assertIn("SWI_UNIF_MENS3", xr.variables)
        self.assertEquals(
            len(xr.variables), 6
        )  # LAMBX, LAMBY, NUMERO, DATE, SWI_UNIF_MENS3 and index

        column_list = ["LAMBX (hm)", "LAMBY (hm)"]
        xr = netcdf_filter_columns(file_name, column_list)

        self.assertIn("LAMBX (hm)", xr.variables)
        self.assertIn("LAMBY (hm)", xr.variables)
        self.assertNotIn("NUMERO", xr.variables)
        self.assertNotIn("DATE", xr.variables)
        self.assertNotIn("SWI_UNIF_MENS3", xr.variables)
        self.assertEquals(len(xr.variables), 3)  # LAMBX, LAMBY and index

    def test_city_mapping(self):
        dimensions = ["LAMBX  (hm)", "LAMBY (hm)"]
        file_name = "tests/meteofrance_mf_1969_2022.nc"

        xr = city_mapping(file_name, dimensions)

        self.assertIn("LAMBX (hm)", xr.variables)
        self.assertIn("LAMBY (hm)", xr.variables)
        self.assertIn("NUMERO", xr.variables)
        self.assertIn("DATE", xr.variables)
        self.assertIn("SWI_UNIF_MENS3", xr.variables)
        self.assertIn("code_insee", xr.variables)
        self.assertIn("nom_commune", xr.variables)
        self.assertIn("centroide_longitude", xr.variables)
        self.assertIn("centroide_latitude", xr.variables)
        self.assertIn("x_drias", xr.variables)
        self.assertIn("y_drias", xr.variables)


if __name__ == "__main__":
    unittest.main()
