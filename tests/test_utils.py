import unittest

import xarray

from downloader.utils import convert_csv_to_netcdf, netcdf_filter_columns

class TestNetCDF(unittest.TestCase):
    
    def test_csv_to_netcdf(self):
        file_name = "tests/meteofrance_mf_1969_2022.csv"
        
        metadata = {
            'A': 1, 
            'B': 2
        }
        
        xr = convert_csv_to_netcdf(file_name, metadata)
        self.assertDictEqual(xr.attrs, metadata)


    def test_select_columns(self):
        file_name = "tests/meteofrance_mf_1969_2022.nc"
        xr = xarray.open_dataset(file_name)

        self.assertIn('LAMBX', xr.variables)
        self.assertIn('LAMBY', xr.variables)
        self.assertIn('NUMERO', xr.variables)
        self.assertIn('DATE', xr.variables)
        self.assertIn('SWI_UNIF_MENS3', xr.variables)
        self.assertEquals(len(xr.variables), 6) #LAMBX, LAMBY, NUMERO, DATE, SWI_UNIF_MENS3 and index

        column_list = ["LAMBX", "LAMBY"]
        xr = netcdf_filter_columns(file_name, column_list)

        self.assertIn('LAMBX', xr.variables)
        self.assertIn('LAMBY', xr.variables)
        self.assertNotIn('NUMERO', xr.variables)
        self.assertNotIn('DATE', xr.variables)
        self.assertNotIn('SWI_UNIF_MENS3', xr.variables)
        self.assertEquals(len(xr.variables), 3) #LAMBX, LAMBY and index


if __name__ == "__main__":
    unittest.main()

        