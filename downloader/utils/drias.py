import json
import os
import sys
import wget

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

def get_url(source, scenario, parametre, modele):
    
    if source is not None:
        data = get_data_info(source)

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

def download_data(data_url, save_path):

    """
    This function aims at uploading a DRIAS file

    :return: the file downloaded

    """    
    return wget.download(data_url, save_path, bar=bar_progress)