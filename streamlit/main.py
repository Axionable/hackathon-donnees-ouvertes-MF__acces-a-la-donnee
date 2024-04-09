import streamlit as st
import requests
import json
from datetime import datetime

import xarray as xr
import numpy as np
import pandas as pd


np.random.seed(0)
temperature = 15 + 8 * np.random.randn(2, 2, 3)
lon = [[-99.83, -99.32], [-99.79, -99.23]]
lat = [[42.25, 42.21], [42.63, 42.59]]
time = pd.date_range("2014-09-06", periods=3)
reference_time = pd.Timestamp("2014-09-05")


da = xr.DataArray(
    data=temperature,
    dims=["x", "y", "time"],
    coords=dict(
        lon=(["x", "y"], lon),
        lat=(["x", "y"], lat),
        time=time,
        reference_time=reference_time,
    ),

    attrs=dict(
        description="Ambient temperature.",
        units="degC",
    ),
)

# da


def telecharger(json):
	r = requests.post('http://localhost:5000/', json=json)
	return r.text

def appli():

	codeInseeList = ["34172", "77280", "77001"]

		#filtre Drias
		# modele : "CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63"
		# parametre : "temperature"
	driasScenarioList = ["historical", "rcp45", "rcp85"]
	isDriasUsed = False

	startDate = datetime.date(datetime.now())
	endDate =  datetime.date(datetime.now())


	f = open('./config.json','r')
	config = json.load(f)
	f.close()


	sourcesList=[]
	for source in config["sources"] :
		sourcesList.append(source["nom"])


	toolName = "Climate Downloader"


	st.write("# "+toolName)
	st.divider()


	st.write("# Filtres")

	f_col_0, f_col_1 = st.columns(2)

	with f_col_0:
		codeInsee = st.selectbox("Commune", codeInseeList)
	with f_col_1 :
		startDate = st.date_input("Date de début", startDate, format="DD/MM/YYYY")
		endDate = st.date_input("Date de fin", endDate if startDate < endDate else startDate , min_value=startDate, format="DD/MM/YYYY")

	st.write("# Collecte")

	sources = st.multiselect("Sources", sourcesList, placeholder="Choisissez au moins une source")

	tableVariableList = []
	usedSources = []

	if sources :

		for source in config["sources"] :
			if source["nom"] in sources :
				usedSources.append(source["nom_out"])
				variableList = { "nom":source["nom_out"], "liste":[], "selected":[] }
				for variable in source["variables"] :
					variableList["liste"].append(variable)
				variableList["selected"] = st.multiselect( "Variables "+source["nom_out"], variableList["liste"], placeholder="Choisissez vos variables")
				tableVariableList.append(variableList)

	apiJson = { 
		"codeInsee" : codeInsee,
		"startDate" : startDate.strftime('%Y-%m-%d'),
		"endDate" : endDate.strftime('%Y-%m-%d'),
		"filtreDonnees" : tableVariableList,
	}

	if "Drias" in usedSources :
		st.write("# Drias")
		scenario = st.selectbox("Paramètre", driasScenarioList)
		apiJson["DriasParams"] = { "modele" : "CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63", "parametre": "temperature", "scenario": scenario }

	if len(tableVariableList) > 0 :
			clicked = st.button("Collecter")
			if clicked :
				response = telecharger(apiJson)

				response



if __name__ == "__main__":
    appli()
		

