"""cleaner.py - Phase 4: clean the raw data."""
import pandas as pd

REQUIRED = ["Date", "Open", "High", "Low", "Close", "Volume"]


def clean_data(df):
    """Fix types, sort by date, drop duplicates, fill/drop missing values."""
    df = df.copy()
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Data is missing columns: {missing}")

    df = df[REQUIRED]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for col in REQUIRED[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.drop_duplicates(subset="Date")
    df = df.sort_values("Date").set_index("Date")
    df = df.ffill().dropna()  # fill small gaps with previous day's value
    print(f"[info] Cleaned data: {df.shape[0]} rows, {df.index.min().date()} to {df.index.max().date()}")
    return df
