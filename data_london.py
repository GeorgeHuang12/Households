import pandas as pd


def unscale(arr_scaled, min_val, max_val):
    return arr_scaled * (max_val - min_val) + min_val


def demand_data(household: str = "MAC001267") -> pd.DataFrame:
    df = pd.read_parquet(r"D:\uni\mainpro\Households\selected_100_normalised_ph.parquet")
    scaler_df = pd.read_csv(r"D:\uni\mainpro\Households\local_kwh_scaler.csv")

    df.columns = df.columns.str.strip()
    scaler_df.columns = scaler_df.columns.str.strip()

    house_id = df[df["LCLid"] == household].copy()

    house_id["DateTime"] = pd.to_datetime(house_id["DateTime"], errors="coerce")
    house_id["kwh"] = pd.to_numeric(house_id["kwh"], errors="coerce")

    house_id = house_id.dropna(subset=["DateTime", "kwh"])
    house_id = house_id.sort_values("DateTime")

    scaler_row = scaler_df[scaler_df["house_id"] == household].copy()

    if scaler_row.empty:
        raise ValueError(f"No scaler row found for household {household}")

    kwh_min = float(scaler_row["kwh_min"].iloc[0])
    kwh_max = float(scaler_row["kwh_max"].iloc[0])

    house_id["demand_kwh"] = unscale(house_id["kwh"], kwh_min, kwh_max)

    hourly_data = house_id[["DateTime", "demand_kwh"]].copy()
    hourly_data = hourly_data.reset_index(drop=True)

    return hourly_data