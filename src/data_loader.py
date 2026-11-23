"""data_loader.py - Phase 3: get stock data (yfinance first, CSV fallback, demo data last)."""
import os

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def fetch_from_yfinance(ticker, start, end):
    """Download daily OHLCV data from Yahoo Finance. Returns None on failure."""
    try:
        import yfinance as yf  # imported here so the project still runs without it

        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):  # newer yfinance returns 2-level columns
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        return df
    except Exception as exc:
        print(f"[warn] yfinance failed: {exc}")
        return None


def load_from_csv(ticker):
    """Load data/<TICKER>.csv (must have Date, Open, High, Low, Close, Volume)."""
    path = os.path.join(DATA_DIR, f"{ticker}.csv")
    if os.path.exists(path):
        print(f"[info] Loading CSV fallback: {path}")
        return pd.read_csv(path)
    return None


def generate_demo_data(ticker, start, end, seed=42):
    """Create realistic-looking fake prices (random walk) so the project always runs."""
    print("[info] Using generated DEMO data (not real prices).")
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, end=end)
    returns = rng.normal(0.0006, 0.015, len(dates))
    close = 150 * np.exp(np.cumsum(returns))
    open_ = close * (1 + rng.normal(0, 0.003, len(dates)))
    high = np.maximum(open_, close) * (1 + rng.uniform(0, 0.01, len(dates)))
    low = np.minimum(open_, close) * (1 - rng.uniform(0, 0.01, len(dates)))
    volume = rng.integers(20_000_000, 90_000_000, len(dates))
    return pd.DataFrame(
        {"Date": dates, "Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume}
    )


def get_stock_data(ticker, start, end):
    """Try yfinance -> CSV -> demo data. Also saves a raw copy to data/."""
    df = fetch_from_yfinance(ticker, start, end)
    source = "yfinance"
    if df is None:
        df = load_from_csv(ticker)
        source = "csv"
    if df is None:
        df = generate_demo_data(ticker, start, end)
        source = "demo"
    os.makedirs(DATA_DIR, exist_ok=True)
    if source == "yfinance":
        df.to_csv(os.path.join(DATA_DIR, f"{ticker}.csv"), index=False)
    print(f"[info] Data source: {source} | rows: {len(df)}")
    return df, source
