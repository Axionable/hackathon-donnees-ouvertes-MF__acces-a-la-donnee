import urllib
import wget
from utils import LOGGER, get_url, bar_progress


def downloader_drias(scenario, parametre, modele):
    """
    Download drias data.

    """
    try:
        url = get_url(scenario, parametre, modele)
        filename = "downloader/data/" + parametre + "_" + modele + "_" + scenario + ".nc"
        wget.download(url, out=filename, bar=bar_progress)
        print()
        LOGGER.info("Données drias téléchargées.")

    except urllib.error.URLError as err:
        LOGGER.error(f"Erreur lors du téléchargement: {err}")
        raise err
    

if __name__ == "__main__":
    downloader_drias(
        scenario="historical", 
        parametre="temperature",
        modele="CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63"
    )