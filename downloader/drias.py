import tempfile
import os
import wget
import urllib
from downloader.utils import LOGGER, get_url, bar_progress


def downloader_drias(scenario, parametre, modele):
    """
    Download drias data.

    :param test: _description_
    :type test: _type_
    :raises err: _description_
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            url = get_url(scenario, parametre, modele)

            filename = "./" + parametre + "_" + modele + "_" + scenario + ".nc"
            file_path = os.path.join(temp_dir, filename)
            data = wget.download(url, out=file_path, bar=bar_progress)
            
        LOGGER.info("Données drias téléchargées.")
        return data

    except urllib.error.URLError as err:
        LOGGER.error(f"Erreur lors du téléchargement: {err}")
        raise err



