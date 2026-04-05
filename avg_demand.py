import pandas as pd


def unnormalise_kwh(
    kwh_scaled: pd.Series,
    kwh_min: pd.Series,
    kwh_max: pd.Series
) -> pd.Series:
    return kwh_scaled * (kwh_max - kwh_min) + kwh_min


def calculate_avg_demand_all_households(
    parquet_path: str = r"D:\uni\mainpro\Households\selected_100_normalised_ph.parquet",
    scaler_path: str = r"D:\uni\mainpro\Households\local_kwh_scaler.csv"
) -> pd.DataFrame:
    df = pd.read_parquet(parquet_path)
    df.columns = df.columns.str.strip()

    scaler_df = pd.read_csv(scaler_path)
    scaler_df.columns = scaler_df.columns.str.strip()

    df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")
    df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")

    df = df.dropna(subset=["DateTime", "kwh", "LCLid"])

    merged_df = pd.merge(
        df,
        scaler_df,
        left_on="LCLid",
        right_on="house_id",
        how="left"
    )

    merged_df = merged_df.dropna(subset=["kwh_min", "kwh_max"])

    merged_df["demand_kwh"] = unnormalise_kwh(
        merged_df["kwh"],
        merged_df["kwh_min"],
        merged_df["kwh_max"]
    )

    avg_demand_df = (
        merged_df.groupby("LCLid")["demand_kwh"]
        .mean()
        .reset_index()
        .rename(columns={"demand_kwh": "avg_demand"})
        .sort_values("avg_demand")
        .reset_index(drop=True)
    )

    return avg_demand_df


if __name__ == "__main__":
    avg_demand_df = calculate_avg_demand_all_households()

    print("All households average demand:")
    print(avg_demand_df)

    print()
    print("Number of households:", len(avg_demand_df))

    print()
    print("Lowest average demand household:")
    print(avg_demand_df.head(1))

    print()
    print("Highest average demand household:")
    print(avg_demand_df.tail(1))

    print()
    print("Lowest 10 average demand households:")
    print(avg_demand_df.head(10))

    print()
    print("Highest 10 average demand households:")
    print(avg_demand_df.tail(10))