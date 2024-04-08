from downloader.utils.drias import is_source_key_available, get_data_info, get_url, download_data
import os

if __name__ == "__main__":
    path = os.path.abspath("../")
    os.chdir(path)

    source = "drias"
    modele = "CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63"
    parametre =  "temperature"
    scenario = "historical"
    filename = "acces-a-la-donnee/downloader/" + parametre + "_" + modele + "_" + scenario + ".nc" 

    url = get_url(source, scenario, parametre, modele)

    file = download_data(url, save_path=filename)
    print(file)