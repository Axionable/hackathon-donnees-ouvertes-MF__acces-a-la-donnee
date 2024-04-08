import pandas as pd
import xarray

def convertir_csv_vers_netcdf(csv_nom_fichier, metadonnees_dict):
    df = pd.read_csv(csv_nom_fichier)

    nom_nc = csv_nom_fichier.rsplit( ".", 1 )[ 0 ]

    xr = xarray.Dataset.from_dataframe(df)
    xr.attrs = metadonnees_dict
    xr.to_netcdf(f'{nom_nc}.nc')

    print("Fichier NetCDF généré")
    return xr


