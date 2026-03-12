import pandas as pd

def pv_data() -> pd.DataFrame:
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
    pv_df["DateTime"] = pv_df["DateTime"] - pd.Timedelta(hours=1)

    pv_df = pv_df.sort_values("DateTime")

    return pv_df

# pv calculation from irradance
def pv_cal(glbl_irad_amt: float, pv_size_kwp : float = 4.0, performance_ratio : float = 0.85) -> float:
    solar_energy = glbl_irad_amt / 3600
    pv_kwh = solar_energy * performance_ratio * pv_size_kwp
    return pv_kwh

