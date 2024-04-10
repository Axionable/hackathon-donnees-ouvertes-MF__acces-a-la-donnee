import streamlit as st
import requests
import json
from json import loads
from datetime import datetime
from PIL import Image

import pandas as pd


def telecharger(json):
    r = requests.post("http://localhost:5000/", json=json)
    dic = loads(r.text)
    print(dic)
    return pd.DataFrame.from_dict(dic)


def appli():
    codeInseeList = ["34172 - Montpellier", "75056 - Paris", "33063 - Bordeaux"]
    driasScenarioList = ["historical", "rcp45", "rcp85"]
    response = None

    startDate = datetime.date(datetime.now())
    endDate = datetime.date(datetime.now())

    with open("./config.json", "r") as f:
        config = json.load(f)

    sourcesList = []
    for source in config["sources"]:
        sourcesList.append(source["nom"])

    st.write("# Climate Accessibility")

    f_col_0, f_col_1, _ = st.columns((5, 9, 7))
    with f_col_0:
        st.write("#### Conçu & Développé par")
    with f_col_1:
        st.image(Image.open("./images/logo-axionable.png"))

    st.divider()

    with st.expander(":one:	**Récupération des données**"):
        st.write("### Paramètres globaux")

        f_col_0, f_col_1 = st.columns(2)

        with f_col_0:
            startDate = st.date_input("Date de début", startDate, format="DD/MM/YYYY")
            codeInsee = st.selectbox("Commune", codeInseeList)
        with f_col_1:
            endDate = st.date_input(
                "Date de fin",
                endDate if startDate < endDate else startDate,
                min_value=startDate,
                format="DD/MM/YYYY",
            )

        st.write("### Paramètres spécifiques aux sources de données")

        sources = st.multiselect(
            "Sources", sourcesList, placeholder="Choisissez au moins une source"
        )

        tableVariableList = []
        usedSources = []

        if sources:
            for source in config["sources"]:
                if source["nom"] in sources:
                    usedSources.append(source["nom_out"])
                    variableList = {
                        "nom": source["nom_out"],
                        "liste": [],
                        "selected": [],
                    }
                    for variable in source["variables"]:
                        variableList["liste"].append(variable)
                    if source["nom"] == "Drias":
                        f_col_0, f_col_1 = st.columns(2)
                        with f_col_0:
                            variableList["selected"] = st.multiselect(
                                "Variables à collecter pour la source : "
                                + source["nom_out"],
                                variableList["liste"],
                                placeholder="Choisissez vos variables",
                            )
                        with f_col_1:
                            scenario = st.selectbox("Scénario Drias", driasScenarioList)
                    else:
                        variableList["selected"] = st.multiselect(
                            "Variables à collecter pour la source : "
                            + source["nom_out"],
                            variableList["liste"],
                            placeholder="Choisissez vos variables",
                        )
                    tableVariableList.append(variableList)

        apiJson = {
            "codeInsee": codeInsee,
            "startDate": startDate.strftime("%Y-%m-%d"),
            "endDate": endDate.strftime("%Y-%m-%d"),
            "filtreDonnees": tableVariableList,
        }

        if "Drias" in usedSources:
            apiJson["DriasParams"] = {
                "modele": "CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63",
                "parametre": "temperature",
                "scenario": scenario,
            }

        if len(tableVariableList) > 0:
            clicked = st.button("Lancer la collecte !")
            if clicked:
                response = telecharger(apiJson)

    if response is not None:
        with st.expander(":two: **Visualisation des résultats**"):
            st.dataframe(response, hide_index=True)

    st.divider()

    st.write(
        "Preuve de Concept d'une application web développée lors du **Hackathon données Ouvertes Météo-France** organisé par"
    )
    f_col_0, _, f_col_1 = st.columns((3, 0.5, 0.65))
    with f_col_0:
        st.image(Image.open("./images/logo-datagouv.png"))
    with f_col_1:
        st.image(Image.open("./images/logo-meteofrance.jpeg"))


if __name__ == "__main__":
    appli()
