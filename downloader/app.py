import xarray
from datetime import date
from sim import launch_process as sim_lp
from drias import launch_process as drias_lp
from flask import Flask

app = Flask(__name__)

@app.route("/collect")
def main():
    sim_xarr = sim_lp(
        insee_code=34172,
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 31),
        vars=["T_Q"],
    )
    print(sim_xarr)

    drias_xarr = drias_lp(
        insee_code=34172,
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 31),
        scenario="rcp45",
        parametre="temperature",
        modele="CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63",
        vars=["tasAdjust"],
    )
    print()
    print(drias_xarr)

    print()
    print("--------------- MERGE ---------------")
    xarr = xarray.combine_by_coords([sim_xarr, drias_xarr])
    print(xarr)
    print()

    return xarr

if __name__ == '__main__':
  app.run(debug=True)



    


# sim_xarr = sim_lp(
#     insee_code=34172,
#     start_date=date(2020, 1, 1),
#     end_date=date(2020, 1, 31),
#     vars=["T_Q"],
# )
# print(sim_xarr)

# drias_xarr = drias_lp(
#     insee_code=34172,
#     start_date=date(2020, 1, 1),
#     end_date=date(2020, 1, 31),
#     scenario="rcp45",
#     parametre="temperature",
#     modele="CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63",
#     vars=["tasAdjust"],
# )
# print()
# print(drias_xarr)

# print()
# print("--------------- MERGE ---------------")
# xarr = xarray.combine_by_coords([sim_xarr, drias_xarr])
# print(xarr)
# print()

