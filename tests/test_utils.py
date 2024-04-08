import unittest

from downloader.utils import convertir_csv_vers_netcdf

class TestConvertion(unittest.TestCase):
    
    def test_csv_to_netcdf(self):
        nom_fichier = "tests/meteofrance_mf_1969_2022.csv"
        
        metadonnees = {
            'A': 1, 
            'B': 2
        }
        
        xr = convertir_csv_vers_netcdf(nom_fichier, metadonnees)
        self.assertDictEqual(xr.attrs, metadonnees)

if __name__ == "__main__":
    unittest.main()

        