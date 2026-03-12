import pandas as pd


# demand data

df = pd.read_csv("D:/uni/mainpro/data set/Small LCL Data/LCL-June2015v2_0.csv")
df.columns = df.columns.str.strip()

house_id = df[df["LCLid"] == "MAC000002"].copy()
house_id = house_id.iloc[:-1]

house_id["DateTime"] = pd.to_datetime(house_id["DateTime"])
house_id["KWH/hh (per half hour)"] = pd.to_numeric(
    house_id["KWH/hh (per half hour)"],
    errors="coerce"
)

house_id["DateTime"] = house_id["DateTime"] - pd.Timedelta(minutes=30)
house_id = house_id.sort_values("DateTime")
house_id = house_id.set_index("DateTime")

hourly_data = pd.DataFrame(
    house_id["KWH/hh (per half hour)"].resample("1h").sum()
)

hourly_data = hourly_data.rename(
    columns={"KWH/hh (per half hour)": "demand_kwh"}
)

hourly_data = hourly_data.reset_index()


# pv data


pv_2012 = pd.read_csv("D:/uni/mainpro/data set/2012.csv", skiprows=78)
pv_2013 = pd.read_csv("D:/uni/mainpro/data set/2013.csv", skiprows=78)
pv_2014 = pd.read_csv("D:/uni/mainpro/data set/2014.csv", skiprows=78)

pv_df = pd.concat([pv_2012, pv_2013, pv_2014], ignore_index=True)
pv_df.columns = pv_df.columns.str.strip()

pv_df = pv_df[["ob_end_time", "glbl_irad_amt"]].copy()
pv_df = pv_df.rename(columns={"ob_end_time": "DateTime"})

pv_df["DateTime"] = pd.to_datetime(pv_df["DateTime"], errors="coerce")
pv_df["glbl_irad_amt"] = pd.to_numeric(
    pv_df["glbl_irad_amt"],
    errors="coerce"
)

pv_df = pv_df.dropna(subset=["DateTime", "glbl_irad_amt"])
pv_df = pv_df.sort_values("DateTime")

# merge

merged_data = pd.merge(
    hourly_data,
    pv_df,
    on="DateTime",
    how="inner"
)

print(merged_data.head())
print(merged_data.tail())
print(merged_data.shape)

print("Demand range:", hourly_data["DateTime"].min(), "to", hourly_data["DateTime"].max())
print("PV range:", pv_df["DateTime"].min(), "to", pv_df["DateTime"].max())