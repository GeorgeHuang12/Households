import pandas as pd 
from agent import Household
from data_london import demand_data
from pv import pv_data, pv_cal, pv_setting 

hourly_data = demand_data("MAC000002")
pv_df = pv_data()
pv_area, pv_efficiency = pv_setting()

merge_data = pd.merge(hourly_data,  pv_df[["DateTime", "glbl_irad_amt"]], on = "DateTime",  how = "inner")

merge_data["pv_kwh"] = merge_data["glbl_irad_amt"].apply(lambda x : pv_cal(glbl_irad_amt=x, pv_area=pv_area, pv_efficiency=pv_efficiency))

results = []

house = Household(h_id=1)

for _, row in merge_data.iterrows():
    demand = row["demand_kwh"]
    pv = row["pv_kwh"]
    t_h = 1.0

    result = house.run_slot(demand = demand, pv = pv, t_h = t_h)
    result["DateTime"] = row["DateTime"]
    result["glbl_irad_amt"] = row["glbl_irad_amt"]
    result["pv_kwh"] = row["pv_kwh"]

    results.append(result)

results_df = pd.DataFrame(results)

pd.set_option("display.max_rows", None)
print(results_df[[
    "DateTime",
    "demand",
    "pv",
    "battery_charged",
    "battery_discharged",
    "import_energy",
    "export_energy",
    "soc"
]][-150:])





