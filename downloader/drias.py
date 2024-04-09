import urllib
import wget
import xarray

from datetime import date
from utils import LOGGER, get_url, bar_progress


def downloader_drias(scenario, parametre, modele):
    """
    Download drias data.

    """
    try:
        url = get_url(scenario, parametre, modele)
        filename = (
            "downloader/data/" + parametre + "_" + modele + "_" + scenario + ".nc"
        )
        wget.download(url, out=filename, bar=bar_progress)
        print()
        LOGGER.info("Données drias téléchargées.")

    except urllib.error.URLError as err:
        LOGGER.error(f"Erreur lors du téléchargement: {err}")
        raise err


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
        "montpellier": {"lon": 3.871099949, "lat": 43.63199234},
        "paris": {"lon": 2.39095163, "lat": 48.82337189},
        "bordeaux": {"lon": -0.545815527, "lat": 44.82810593},
    }

    # xarr = xarr.set_index(lat="lat")
    # xarr = xarr.set_index(lon="lon")

    return xarr.sel(
        lon=city_mapping[city]["lon"], lat=city_mapping[city]["lat"]
    )


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
