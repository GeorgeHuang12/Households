import pandas as pd 

def demand_data(household : str = "MAC000002") -> pd.DataFrame:
    df = pd.read_csv("D:/uni/mainpro/data set/Small LCL Data/LCL-June2015v2_0.csv")

    house_id = df[df['LCLid'] == household].copy()
    house_id = house_id.iloc[:-1]

    house_id["DateTime"] = pd.to_datetime(house_id["DateTime"])
    house_id["KWH/hh (per half hour)"] = pd.to_numeric(house_id["KWH/hh (per half hour) "],  errors = "coerce" )

    house_id = house_id.dropna(subset=["DateTime", "KWH/hh (per half hour)"])

    house_id["DateTime"] = house_id["DateTime"] - pd.Timedelta(minutes=30)
    house_id = house_id.sort_values("DateTime")
    house_id = house_id.set_index("DateTime")

    hourly_data = pd.DataFrame(house_id["KWH/hh (per half hour)"].resample("1h").sum())

    hourly_data = hourly_data.rename(columns={"KWH/hh (per half hour)": "demand_kwh"})

    hourly_data = hourly_data.reset_index()

    return hourly_data



