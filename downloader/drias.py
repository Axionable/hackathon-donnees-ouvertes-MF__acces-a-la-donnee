import urllib
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
    filename = (
        "downloader/data/" + parametre + "_" + modele + "_" + scenario + ".nc"
    )
    
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
    xarr = xarr.sel(
        time=slice(start_date, end_date)
    )

    return xarr


def select_data_for_a_city(
    xarr: xarray.core.dataset.Dataset, city: str
) -> xarray.core.dataset.Dataset:
    """_summary_

    :param xarr: _description_
    :param city: _description_
    :return: _description_
    """
    city_mapping = {
        "montpellier": {"x": 724000, "y": 1849000},
        "paris": {"x": 604000, "y": 2425000},
        "bordeaux": {"x": 372000, "y": 1985000},
    }

    return xarr.sel(
        x=city_mapping[city]["x"], y=city_mapping[city]["y"]
    )

def launch_process(insee_code: int, start_date: date, end_date: date, scenario:str, parametre:str, modele:str, vars: list[str]) -> xarray.core.dataset.Dataset:
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
    # downloader_drias(
    #     scenario="historical",
    #     parametre="temperature",
    #     modele="CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63"
    # )

    xarr = get_data_from_file(
        filename="downloader/data/temperature_CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63_historical.nc"
    )
    print(xarr)
    print()

    xarr = filter_xarr(
        xarr=xarr,
        vars=["tasAdjust"],
        start_date=date(2005, 1, 1),
        end_date=date(2005, 1, 2),
    )
    print(xarr)
    print()

    xarr = select_data_for_a_city(xarr=xarr, city="montpellier")
    print(xarr)
