from downloader.drias import downloader_drias
import os

if __name__ == "__main__":
    path = os.path.abspath("../")
    os.chdir(path)

    modele = "CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63"
    parametre =  "temperature"
    scenario = "historical"

    data = downloader_drias(scenario, parametre, modele)
    print(data)