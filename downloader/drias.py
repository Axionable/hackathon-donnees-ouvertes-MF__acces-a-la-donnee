import urllib
import numpy as np
import wget
import xarray
from os import path

from datetime import date
from utils import LOGGER, get_url, bar_progress


def downloader_drias(scenario: str, parametre: str, modele: str) -> None:
    """
    Télécharge les données drias.

    :param scenario: Scenario climatique (Historical, rcp45, rcp85)
    :param parametre: Paramètre du modèle.
    :param modele: Modèle climatique.
    :return: None
    """
    url = get_url(scenario, parametre, modele)
    filename = "downloader/data/" + parametre + "_" + modele + "_" + scenario + ".nc"

    if path.exists(filename):
        LOGGER.info(f"Le fichier {filename} est déjà disponible localement.")

    else:
        LOGGER.info(f"Téléchargement du fichier {filename} en cours ...")
        wget.download(
            url=url,
            out=filename,
            bar=bar_progress,
        )
        print()
        LOGGER.info(f"Téléchargement terminé !")


def get_data_from_file(filename: str) -> xarray.core.dataset.Dataset:
    """
    Charge et renvoie le fichier téléchargé en local.

    :param filename: Chemin du fichier à charger.
    :return: Le dataset au format netcdf.
    """
    xarr = xarray.open_dataset(filename)
    xarr.attrs = None
    return xarr


def filter_xarr(
    xarr: xarray.core.dataset.Dataset, vars: list[str], start_date: date, end_date: date
) -> xarray.core.dataset.Dataset:
    """
    Fonction pour filtrer un xarray : par dates.

    :param xarr: Données drias à filtrer.
    :param vars: Les colonnes à garder
    :param start_date: Date minimale.
    :param end_date: Date maximale.
    :return: Un xarray filtré
    """
    # Variable filtering
    xarr = xarr[vars]

    # Date filtering
    xarr = xarr.sel(time=slice(start_date, end_date))

    return xarr


def select_data_for_a_city(
    xarr: xarray.core.dataset.Dataset, insee_code: int
) -> xarray.core.dataset.Dataset:
    """
    Fonction pour filtrer les données d'une ou plusieurs communes.

    :param xarr: Dataset à filtrer.
    :param insee_code: Le code insee de la commune recherchée.
    :return: Dataset filtré.
    """
    city_mapping = {
        34172: {"x": 724000, "y": 1849000},
        75056: {"x": 604000, "y": 2425000},
        33063: {"x": 372000, "y": 1985000},
    }

    xarr = xarr.sel(x=city_mapping[insee_code]["x"], y=city_mapping[insee_code]["y"])

    xarr = xarr.assign_coords(INSEE=("INSEE", np.array([insee_code])))

    return xarr


def launch_process(
    insee_code: int,
    start_date: date,
    end_date: date,
    scenario: str,
    parametre: str,
    modele: str,
    vars: list[str],
) -> xarray.core.dataset.Dataset:
    """
    Fonction pour gérer l'ensemble du processus Drias.

    :param insee_code: Code insee de la commune recherchée.
    :param start_date: Date minimale.
    :param end_date: Date maximale.
    :param scenario: Scénario climatique.
    :param parametre: Paramètre du modèle.
    :param modele: Modèle climatique.
    :param vars: Colonnes à garder pour le filtrage.
    :return: Le dataset final.
    """
    # We collect required data
    downloader_drias(scenario=scenario, parametre=parametre, modele=modele)

    # We load data as Pandas DataFrame
    filename = "downloader/data/" + parametre + "_" + modele + "_" + scenario + ".nc"
    data = get_data_from_file(filename=filename)

    # We processed the data
    xarr = filter_xarr(xarr=data, vars=vars, start_date=start_date, end_date=end_date)
    xarr = select_data_for_a_city(xarr=xarr, insee_code=insee_code)
    xarr = xarr.assign(tasAdjust_C=lambda x: x.tasAdjust - 273.15)
    xarr = xarr.drop_vars(["x", "y", "lat", "lon"])
    xarr = xarr.rename({"time": "DATE", "tasAdjust": "tasAdjust_K"})

    return xarr
