import json
import wget

from datetime import date
from os import path
from utils import LOGGER, bar_progress


def get_data_info(source_key: str) -> dict:
    """
    Fonction pour récupérer les informations d'une source de données spécifiée.
    La source de données est représentée par sa clé (définie dans le fichier "conf/sim.json").

    :param source_key: Clé de la source de données désirée
    :return: Les informations de la source de données (nom du fichier, url de téléchargement)
    """
    if source_key is not None:
        with open("downloader/conf/conf.json", "r") as file:
            content = json.load(file)
            return content["sources"]["sim"][source_key]
 

def get_data_sources_name() -> list[str]:
    """
    Fonction pour récupérer l'ensemble des clés (source de données) présentent 
    dans le fichier de configuration "conf/sim.json".

    :return: Une liste de clé
    """
    with open("downloader/conf/conf.json", "r") as file:
        content = json.load(file)
        return list(content["sources"]["sim"].keys())
    

def extract_years_from_data_source_name(data_source_name: str) -> list[int, int]:
    """
    Fonction pour extraire les années disponibles dans un fichier à 
    partir de la clé d'une source de données.

    :param data_source_name: Clé de la source de données désirée
    :return: Un tableau avec l'année minimale et maximale
    """
    return [int(date) for date in data_source_name.split("_")[-2:]]


def get_required_data_source(start_date: date, end_date: date) -> list[str]:
    """
    Fonction pour sélectionner les sources de données nécessaires pour 
    récupérer les données entre deux dates spécifiées.

    :param start_date: Date minimale
    :param end_date: Date maximale
    :return: Liste des sources de données à télécharger
    """
    min_year = start_date.year
    max_year = end_date.year

    data_sources_name = get_data_sources_name()
    file_to_dl = []

    for name in data_sources_name:
        curr_min, curr_max = extract_years_from_data_source_name(data_source_name=name)
        if min_year >= curr_min and min_year <= curr_max:
            file_to_dl.append(name)
        elif max_year <= curr_max and max_year >= curr_min:
            file_to_dl.append(name)

    return file_to_dl


def download_data(start_date: date, end_date: date) -> None:
    """
    Fonction globale pour télécharger les données.

    :param start_date: Date minimale
    :param end_date: Date maximale
    """
    data_sources_to_dl = get_required_data_source(
        start_date=start_date, 
        end_date=end_date
    )

    for data_source in data_sources_to_dl:
        data_source_info = get_data_info(source_key=data_source)
        filename = data_source_info["filename"]

        if path.exists(f"downloader/data/{filename}"):
            LOGGER.info(f"Le fichier {filename} est déjà disponible localement.")
        
        else:
            LOGGER.info(f"Téléchargement du fichier {filename} en cours ...")
            wget.download(
                url=data_source_info["url"], 
                out=f"downloader/data/{filename}", 
                bar=bar_progress
            )
            print()
            LOGGER.info(f"Téléchargement terminé !")


if __name__ == "__main__":
    download_data(
        start_date=date(2019, 10, 20), 
        end_date=date(2022, 10, 21)
    )
