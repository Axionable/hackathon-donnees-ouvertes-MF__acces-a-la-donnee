import os
import urllib
import zipfile
import wget
import tempfile
import geopandas
from utils import LOGGER, get_data_info


def osm_downloader():
    """
    Télécharge le découpage administratif communal français d'OSM depuis
    data.gouv.fr.

    :param test: _description_
    :type test: _type_
    :raises err: _description_
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            url = get_data_info(source_key="insee")["url"]
            zip_file_name = "communes-shp.zip"
            zip_file_path = os.path.join(temp_dir, zip_file_name)
            wget.download(url, out=zip_file_path)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_handler:
                file_name = get_data_info(source_key="insee")["shp_file_name"]
                file_path = os.path.join(temp_dir, "communes-shp", file_name)
                zip_handler.extractall(os.path.join(temp_dir, "communes-shp"))
                data = geopandas.read_file(file_path)

        LOGGER.info("Données de découpage communal téléchargées.")
        return data

    except urllib.error.URLError as err:
        LOGGER.error(f"Erreur lors du téléchargement: {err}")
        raise err


if __name__ == "__main__":
    data = osm_downloader()
    print(data)
