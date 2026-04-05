import pandas as pd 
import matplotlib.pyplot as plt
import os 
from agent import Household
from data_london import demand_data
from pv import pv_data, pv_cal, pv_setting 

hourly_data = demand_data("MAC001267")
pv_df = pv_data()
avg_demand = hourly_data["demand_kwh"].mean()
pv_area, pv_efficiency = pv_setting(avg_demand)

merge_data = pd.merge(hourly_data,  pv_df[["DateTime", "glbl_irad_amt"]], on = "DateTime",  how = "inner")

merge_data["pv_kwh"] = merge_data["glbl_irad_amt"].apply(lambda x : pv_cal(glbl_irad_amt=x, pv_area=pv_area, pv_efficiency=pv_efficiency))

results = []

house = Household(h_id=1, avg_demand = avg_demand)

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


print("average demand", avg_demand)


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
]][10000: 10100])


print("Average demand:", avg_demand)
print("PV area:", pv_area)
print("PV efficiency:", pv_efficiency)
print("Battery capacity:", house.battery.capacity_kwh)

results_df["DateTime"] = pd.to_datetime(results_df["DateTime"])
results_df = results_df.sort_values("DateTime")

# choose a smaller window first so the graph is easier to read
plot_df = results_df.tail(168).copy()   # last 168 hours = 7 days


plot_folder = "plots"
os.makedirs(plot_folder, exist_ok=True)


# 1. Demand and PV
plt.figure(figsize=(12, 5))
plt.plot(plot_df["DateTime"], plot_df["demand"], label="Demand (kWh)")
plt.plot(plot_df["DateTime"], plot_df["pv"], label="PV (kWh)")
plt.xlabel("DateTime")
plt.ylabel("Energy (kWh)")
plt.title("Demand and PV")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_folder, "01_demand_pv.png"))
plt.close()


# 2. Import and Export
plt.figure(figsize=(12, 5))
plt.plot(plot_df["DateTime"], plot_df["import_energy"], label="Import Energy (kWh)")
plt.plot(plot_df["DateTime"], plot_df["export_energy"], label="Export Energy (kWh)")
plt.xlabel("DateTime")
plt.ylabel("Energy (kWh)")
plt.title("Import and Export")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_folder, "02_import_export.png"))
plt.close()


# 3. Battery Charge and Discharge
plt.figure(figsize=(12, 5))
plt.plot(plot_df["DateTime"], plot_df["battery_charged"], label="Battery Charged (kWh)")
plt.plot(plot_df["DateTime"], plot_df["battery_discharged"], label="Battery Discharged (kWh)")
plt.xlabel("DateTime")
plt.ylabel("Energy (kWh)")
plt.title("Battery Charge and Discharge")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_folder, "03_battery_charge_discharge.png"))
plt.close()


# 4. SOC
plt.figure(figsize=(12, 5))
plt.plot(plot_df["DateTime"], plot_df["soc"], label="SOC")
plt.xlabel("DateTime")
plt.ylabel("State of Charge")
plt.title("Battery SOC")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_folder, "04_soc.png"))
plt.close()


# 5. Energy balance before and after battery
plt.figure(figsize=(12, 5))
plt.plot(plot_df["DateTime"], plot_df["energy_before"], label="Energy Before Battery (kWh)")
plt.plot(plot_df["DateTime"], plot_df["energy_after"], label="Energy After Battery (kWh)")
plt.xlabel("DateTime")
plt.ylabel("Energy (kWh)")
plt.title("Energy Balance Before and After Battery")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_folder, "05_energy_before_after.png"))
plt.close()


