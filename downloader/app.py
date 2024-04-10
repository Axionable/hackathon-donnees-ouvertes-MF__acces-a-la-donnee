import datetime
import xarray

from flask import Flask, request, Response

from drias import launch_process as launch_drias
from sim import launch_process as launch_sim


app = Flask(__name__)


@app.route("/", methods=["POST"])
def full_process():
    """
    Lance le process de téléchargement global.
    NOTE : Cette API attend la fin de(s) téléchargement(s) pour renvoyer
    une réponse HTTP. Dans une architecture Cloud, cette API pourrait
    être asynchrone (voir schéma d'architecture joint).
    """
    body = request.get_json()
    dl_drias = False
    dl_sim = False

    try:
        assert len(body["filtreDonnees"]) <= 2
        for data in body["filtreDonnees"]:
            if data["nom"] == "Drias":
                dl_drias = True
                drias_xarr = launch_drias(
                    insee_code=int(body["codeInsee"].split(" - ")[0]),
                    start_date=datetime.datetime.strptime(
                        body["startDate"], "%Y-%m-%d"
                    ).date(),
                    end_date=datetime.datetime.strptime(
                        body["endDate"], "%Y-%m-%d"
                    ).date(),
                    scenario=body["DriasParams"]["scenario"],
                    parametre=body["DriasParams"]["parametre"],
                    modele=body["DriasParams"]["modele"],
                    vars=data["selected"],
                )

            if data["nom"] == "Météo France - SIM":
                dl_sim = True
                sim_xarr = launch_sim(
                    insee_code=int(body["codeInsee"].split(" - ")[0]),
                    start_date=datetime.datetime.strptime(
                        body["startDate"], "%Y-%m-%d"
                    ).date(),
                    end_date=datetime.datetime.strptime(
                        body["endDate"], "%Y-%m-%d"
                    ).date(),
                    vars=data["selected"],
                )

        if dl_drias and dl_sim:
            xarr = xarray.combine_by_coords([sim_xarr, drias_xarr])
            df = xarr.to_dataframe().reset_index()
            df["DATE"] = df["DATE"].dt.strftime("%Y-%m-%d")
            df = df.to_json(orient="records")
            return Response(
                df,
                mimetype="application/json",
            )
        elif dl_drias and not dl_sim:
            df = drias_xarr.to_dataframe().reset_index()
            df["DATE"] = df["DATE"].dt.strftime("%Y-%m-%d")
            df = df.to_json(orient="records")
            return Response(
                df,
                mimetype="application/json",
            )
        elif not dl_drias and dl_sim:
            df = sim_xarr.to_dataframe().reset_index()
            df["DATE"] = df["DATE"].dt.strftime("%Y-%m-%d")
            df = df.to_json(orient="records")
            return Response(
                df,
                mimetype="application/json",
            )
    except (KeyError, AssertionError) as err:
        return Response(
            f"Erreur : mauvais corps de requête. Détails: {err}", status=400
        )


if __name__ == "__main__":
    app.run(debug=True)
