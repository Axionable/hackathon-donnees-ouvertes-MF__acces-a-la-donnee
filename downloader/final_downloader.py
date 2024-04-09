import xarray
from downloader.drias import downloader_drias, select_data_for_a_city
from downloader.sim import download_data
from downloader.utils import city_mapping, convert_csv_to_netcdf, netcdf_filter_columns


def collect_final_drias(donnees_json):
    liste_drias = next((filtre['liste'] for filtre in donnees_json['filtreDonnees'] if filtre['nom'] == 'Drias'), None)
       
    drias_data_netcdf = downloader_drias(donnees_json['DriasParams']['scenario'], donnees_json['DriasParams']['parametre'], donnees_json['DriasParams']['modele'])
    
    drias_filtered_columns = netcdf_filter_columns(drias_data_netcdf, liste_drias)
    dim = ['x_drias', 'y_drias']

    final_drias = city_mapping(drias_filtered_columns, dim)
    return final_drias


def collect_final_sim(donnees_json):
    liste_sim = next((filtre['liste'] for filtre in donnees_json['filtreDonnees'] if filtre['nom'] == 'SIM'), None)

    sim_data_csv = download_data(donnees_json['start_date'], donnees_json['end_date'])
    sim_data_netcdf = convert_csv_to_netcdf(sim_data_csv)
    
    sim_filtered_columns = netcdf_filter_columns(sim_data_netcdf, liste_sim)
    
    sim_filtered_city = select_data_for_a_city(sim_filtered_columns)
    dim = ['LAMBX (hm)', 'LAMBY(hm)']

    final_sim = city_mapping(sim_filtered_city, dim)
    return final_sim


def collect_final_data(donnees_json):
    bool_drias = any(filtre['nom'] == 'Drias' for filtre in donnees_json['filtreDonnees'])
    bool_sim = any(filtre['nom'] == 'SIM' for filtre in donnees_json['filtreDonnees'])

    if bool_drias:
        final_drias = collect_final_drias(donnees_json)

    if bool_sim:
        final_sim = collect_final_sim(donnees_json)

    dim = ['code_insee']
    if bool_drias and bool_sim:
        final_data = xarray.concat([final_sim, final_drias], dim = dim)
    
    return final_data