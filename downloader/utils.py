import json
import logging
import os
import pandas as pd
import sys
import xarray


FORMAT = "%(asctime)-15s [%(filename)s:%(lineno)s - %(funcName)2s()] %(message)s"
log_level = (
    os.environ.get("LOG_LEVEL") if os.environ.get("LOG_LEVEL") is not None else "INFO"
)
logging.basicConfig(
    stream=sys.stdout, format=FORMAT, level=logging.getLevelName(log_level)
)
LOGGER = logging.getLogger(__name__)


def convert_csv_to_netcdf(csv_path: str, metadata: dict) -> xarray:
    """
    Convertir un fichier CSV en un fichier NetCDF
    :param csv_file_name: Chemin d'accès au fichier CSV à convertir
    :param metadata: Métadonnées à exporter dans le fichier NetCDF
    :return: Nouveau fichier NetCDF généré
    """
    df = pd.read_csv(csv_path)

    nom_nc = csv_path.rsplit(".", 1)[0]

    xr = xarray.Dataset.from_dataframe(df)
    xr.attrs = metadata
    xr.to_netcdf(f"{nom_nc}.nc")

    return xr


def is_source_key_available(source_key: str) -> bool:
    """
    Vérifier si "source_key" est disponible dans le fichier : downloader/conf/sim.json
    :param source_key: Clé correspondant à la source de données souhaitée
    :return: Statut de vérification (vrai ou faux)
    """
    if source_key is None:
        return False

    else:
        with open("downloader/conf/conf.json", "r") as file:
            content = json.load(file)
            return source_key in content["sources"].keys()


def get_data_info(source_key: str) -> dict:
    """
    Retourne les éléments du fichier de configuration.
    :param source_key: Clé correspondant à la source de données souhaitée
    :return: Valeur de l'élément dans le fichier de config
    """
    if source_key is not None:
        with open("downloader/conf/conf.json", "r") as file:
            content = json.load(file)
            return content["sources"][source_key]


def get_url(scenario: str, parametre: str, modele: str) -> str:
    """
    Renvoie le lien pour télécharger les données, selon les paramètres envoyés
    :param scenario: Scénario choisi
    :param parametre: Paramètres sélectionnés
    :param modele: Modèle choisi
    :return: Lien de téléchargement des données
    """
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


def netcdf_filter_columns(netcdf_file: str, column_list: list[str]) -> xarray:
    """
    Renvoie un fichier NetCDF comprenant uniquement les colonnes demandées
    :param netcdf_file: Nom du fichier à traiter
    :param column_list: Liste des colonnes à conserver
    :return: Nouveau fichier NetCDF
    """
    data = xarray.open_dataset(netcdf_file)
    data_subset = data[column_list]
    data_subset.to_netcdf(f"{netcdf_file}_final.nc")

    return data_subset


def city_mapping(source: str, dimensions: list[str]) -> xarray:
    """
    Concatene un fichier source avec le fichier de mapping des villes, sur les dimensions choisies
    :param source: Nom du fichier source
    :param dimensions: Liste des dimensions sur lesquelles effectuer le filtre
    :return: Fichier final concaténé
    """
    xarray_city_mapper = xarray.open_dataset("downloader/data/city_mapping.nc")
    city_mapper_subset = xarray_city_mapper[["code_insee"]]
    xarray_source = xarray.open_dataset(source)

    mapped_city = xarray.concat([xarray_source, city_mapper_subset], dim=dimensions)

    return mapped_city
