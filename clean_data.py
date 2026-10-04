
import pandas as pd

RAW_FILE = "/content/pharmeasy_orders_raw.csv"
REGIONS_FILE = "/content/regions_master.csv"
OUTPUT_FILE = "/content/orders_clean.csv"

EXPECTED_COLUMNS = [
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "sales_inr",
    "profit_inr"
]


def validate_schema(df):
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return True


def clean_data():
    df = pd.read_csv(RAW_FILE)
    regions = pd.read_csv(REGIONS_FILE)

    validate_schema(df)

    print("Original rows:", len(df))

    # Remove duplicate order IDs
    df = df.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    # Standardize date
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # ---------------------------------------------------------
    # Standardize region names using regions_master
    # ---------------------------------------------------------
    region_map = {
        str(region).strip().lower(): region
        for region in regions["region"].dropna().unique()
    }

    df["region"] = (
        df["region"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(region_map)
    )

    # Check for regions that could not be mapped
    if df["region"].isna().any():
        unknown_regions = df.loc[
            df["region"].isna(),
            "region"
        ].unique()

        raise ValueError(
            f"Unknown region values after standardization: "
            f"{unknown_regions}"
        )

    # Fill missing categories using mode
    if df["category"].isna().sum() > 0:
        df["category"] = df["category"].fillna(
            df["category"].mode()[0]
        )

    # Fill missing profit using median
    if df["profit_inr"].isna().sum() > 0:
        df["profit_inr"] = df["profit_inr"].fillna(
            df["profit_inr"].median()
        )

    # Numeric conversions
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["sales_inr"] = pd.to_numeric(
        df["sales_inr"],
        errors="coerce"
    )

    df["profit_inr"] = pd.to_numeric(
        df["profit_inr"],
        errors="coerce"
    )

    validate_schema(df)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Cleaned rows:", len(df))
    print("Unique regions:", df["region"].nunique())
    print("Regions:", sorted(df["region"].unique()))
    print("Saved:", OUTPUT_FILE)

    return df


if __name__ == "__main__":
    clean_data()
