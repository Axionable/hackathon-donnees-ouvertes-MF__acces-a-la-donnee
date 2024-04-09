import xarray
from sim import launch_process as launch_sim
from drias import launch_process as launch_drias
import datetime
from flask import Flask, request, Response

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
                    insee_code=34172,
                    start_date=datetime.date(2020, 1, 1),
                    end_date=datetime.date(2020, 1, 31),
                    scenario="rcp45",
                    parametre="temperature",
                    modele="CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63",
                    vars=["tasAdjust"],
                )

            if data["nom"] == "SIM":
                dl_sim = True
                sim_xarr = launch_sim(
                    insee_code=34172,
                    start_date=datetime.date(2020, 1, 1),
                    end_date=datetime.date(2020, 1, 2),
                    vars=["T_Q"],
                )

        if dl_drias and dl_sim:
            xarr = xarray.combine_by_coords([sim_xarr, drias_xarr])
            print()
            print()
            print("------ FINAL DATASET: DRIAS & SIM MERGED ------")
            print(xarr)
            print()
            print()
        elif dl_drias and not dl_sim:
            pass
        elif not dl_drias and dl_sim:
            pass
        
        return Response(
            f"OK",
            status=200
        )
        
    except (KeyError, AssertionError) as err:
        return Response(
            f"Erreur : mauvais corps de requête. Détails: {err}",
            status=400
        )


if __name__ == '__main__':
    app.run(debug=True)
