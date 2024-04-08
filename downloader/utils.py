import pandas as pd
import xarray
import json
import os
import sys
import logging


FORMAT = "%(asctime)-15s [%(filename)s:%(lineno)s - %(funcName)2s()] %(message)s"
log_level = os.environ.get("LOG_LEVEL") if os.environ.get(
    "LOG_LEVEL") is not None else "INFO"
logging.basicConfig(
    stream=sys.stdout, format=FORMAT, level=logging.getLevelName(log_level)
)
LOGGER = logging.getLogger(__name__)


def convertir_csv_vers_netcdf(csv_nom_fichier, metadonnees_dict):
    df = pd.read_csv(csv_nom_fichier)

    nom_nc = csv_nom_fichier.rsplit( ".", 1 )[ 0 ]

    xr = xarray.Dataset.from_dataframe(df)
    xr.attrs = metadonnees_dict
    xr.to_netcdf(f'{nom_nc}.nc')

    print("Fichier NetCDF généré")
    return xr


def is_source_key_available(source_key: str) -> bool:
    """
    Check if "source_key" is available in the file: downloader/conf/drias.json
    :param source_key: Key corresponding to the desired data source
    :return: Verification status (true or false)
    """

    if source_key is None:
        return False
    
    else:
        with open("acces-a-la-donnee/downloader/conf/drias.json", "r") as file:
            content = json.load(file)
            return source_key in content["sources"].keys()
        

def get_data_info(source_key: str) -> dict:
    """
    Return elements within the config file.
    :param source_key: Key corresponding to the desired data source
    :return: Config element's value
    """
    if source_key is not None:
        with open("acces-a-la-donnee/downloader/conf/drias.json", "r") as file:
            content = json.load(file)
            return content["sources"][source_key]


def get_url(scenario, parametre, modele):
    data = get_data_info("drias")
    if modele in data.keys() and parametre == data[modele]["parametre"]:
        if scenario == "historical":
            return data[modele]["historical_url"]
        elif scenario == "rcp45":
            return data[modele]["rcp45_url"]
        elif scenario == "rcp85":
            return data[modele]["rcp85_url"]
        else:
            print("Scenario invalide...")
            return None
    else:
        print("Parametres invalides...")
        return None         


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (
        current / total * 100,
        current,
        total,
    )
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()
