import pandas as pd

def unscale(arr_scaled, min_val, max_val):
    """
    Convert scaled values back to raw kWh.
    Works for both 1D and 2D arrays.
    """
    return arr_scaled * (max_val - min_val) + min_val

def demand_data(household: str = "MAC001249") -> pd.DataFrame:
    df = pd.read_parquet(r"D:\uni\mainpro\Households\selected_100_normalised_ph.parquet")

    house_id = df[df["LCLid"] == household].copy()

    house_id["DateTime"] = pd.to_datetime(house_id["DateTime"], errors="coerce")
    house_id["kwh"] = pd.to_numeric(house_id["kwh"], errors="coerce")

    house_id = house_id.dropna(subset=["DateTime", "kwh"])
    house_id = house_id.sort_values("DateTime")

    hourly_data = house_id[["DateTime", "kwh"]].copy()
    hourly_data = hourly_data.rename(columns={"kwh": "demand_kwh"})
    hourly_data = hourly_data.reset_index(drop=True)

    return hourly_data




