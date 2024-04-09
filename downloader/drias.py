import urllib
import numpy as np
import wget
import xarray
from os import path

from datetime import date
from utils import LOGGER, get_url, bar_progress


def downloader_drias(scenario, parametre, modele):
    """_summary_

    :param scenario: _description_
    :param parametre: _description_
    :param modele: _description_
    :return: _description_
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
    """_summary_

    :param filename: _description_
    :return: _description_
    """
    xarr = xarray.open_dataset(filename)
    xarr.attrs = None
    return xarr


def filter_xarr(
    xarr: xarray.core.dataset.Dataset, vars: list[str], start_date: date, end_date: date
) -> xarray.core.dataset.Dataset:
    """_summary_

    :param xarr: _description_
    :param vars: _description_
    :param start_date: _description_
    :param end_date: _description_
    :return: _description_
    """
    # Variable filtering
    xarr = xarr[vars]

    # Date filtering
    xarr = xarr.sel(time=slice(start_date, end_date))

    return xarr


def select_data_for_a_city(
    xarr: xarray.core.dataset.Dataset, insee_code: int
) -> xarray.core.dataset.Dataset:
    """_summary_

    :param xarr: _description_
    :param city: _description_
    :return: _description_
    """
    city_mapping = {
        34172: {"x": 724000, "y": 1849000},
        75056: {"x": 604000, "y": 2425000},
        33063: {"x": 372000, "y": 1985000},
    }

    xarr = xarr.sel(x=city_mapping[insee_code]["x"], y=city_mapping[insee_code]["y"])

    xarr = xarr.assign_coords(insee=("insee", np.array([insee_code])))

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
    """_summary_

    :param insee_code: _description_
    :param start_date: _description_
    :param end_date: _description_
    :param scenario: _description_
    :param parametre: _description_
    :param modele: _description_
    :param vars: _description_
    :return: _description_
    """
    # We collect required data
    downloader_drias(scenario=scenario, parametre=parametre, modele=modele)

    # We load data as Pandas DataFrame
    filename = "downloader/data/" + parametre + "_" + modele + "_" + scenario + ".nc"
    data = get_data_from_file(filename=filename)

    # We processed the data
    xarr = filter_xarr(xarr=data, vars=vars, start_date=start_date, end_date=end_date)
    xarr = select_data_for_a_city(xarr=xarr, insee_code=insee_code)

    return xarr


if __name__ == "__main__":

    xarr = launch_process(
        insee_code=34172,
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 31),
        scenario="rcp45",
        parametre="temperature",
        modele="CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63",
        vars=["tasAdjust"],
    )

    print(xarr)
