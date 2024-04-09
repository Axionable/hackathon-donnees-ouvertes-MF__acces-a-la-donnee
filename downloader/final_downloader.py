from downloader.drias import downloader_drias
from downloader.sim import download_data
from downloader.utils import convert_csv_to_netcdf, netcdf_filter_columns


def collect_final_data(donnees_json):

    bool_drias = any(filtre['nom'] == 'Drias' for filtre in donnees_json['filtreDonnees'])
    bool_sim = any(filtre['nom'] == 'SIM' for filtre in donnees_json['filtreDonnees'])

    if bool_drias:
        liste_drias = next((filtre['liste'] for filtre in donnees_json['filtreDonnees'] if filtre['nom'] == 'Drias'), None)
       
        drias_data_netcdf = downloader_drias(donnees_json['DriasParams']['scenario'], donnees_json['DriasParams']['parametre'], donnees_json['DriasParams']['modele'])
        
        drias_netcdf_final = netcdf_filter_columns(drias_data_netcdf, liste_drias)

    if bool_sim:
        liste_sim = next((filtre['liste'] for filtre in donnees_json['filtreDonnees'] if filtre['nom'] == 'SIM'), None)

        sim_data_csv = download_data(donnees_json['start_date'], donnees_json['end_date'])
        sim_data_netcdf = convert_csv_to_netcdf(sim_data_csv)
        
        sim_netcdf_final = netcdf_filter_columns(sim_data_netcdf, liste_sim)

    if bool_drias and bool_sim:
        