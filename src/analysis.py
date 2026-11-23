"""analysis.py - Phases 5-7: EDA, moving averages, returns, volatility, trend."""
import numpy as np
import pandas as pd

TRADING_DAYS = 252  # trading days in a year (used to annualize volatility)


def add_indicators(df):
    """Add daily return, cumulative return, SMA20/50/200, rolling volatility, drawdown."""
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
    for window in (20, 50, 200):
        df[f"SMA_{window}"] = df["Close"].rolling(window).mean()
    df["Volatility_20d"] = df["Daily_Return"].rolling(20).std() * np.sqrt(TRADING_DAYS)
    running_max = df["Close"].cummax()
    df["Drawdown"] = df["Close"] / running_max - 1
    return df


def detect_trend(df):
    """Simple trend rule using SMA20 vs SMA50 on the latest day."""
    last = df.iloc[-1]
    if pd.isna(last["SMA_50"]):
        return "Not enough data"
    if last["SMA_20"] > last["SMA_50"] and last["Close"] > last["SMA_50"]:
        return "Uptrend (Bullish)"
    if last["SMA_20"] < last["SMA_50"] and last["Close"] < last["SMA_50"]:
        return "Downtrend (Bearish)"
    return "Sideways / Mixed"


def summarize(df, ticker):
    """Return a dict of key statistics for the report."""
    ret = df["Daily_Return"].dropna()
    ann_vol = ret.std() * np.sqrt(TRADING_DAYS)
    ann_ret = ret.mean() * TRADING_DAYS
    sharpe = ann_ret / ann_vol if ann_vol else np.nan  # risk-free rate assumed 0 for simplicity
    return {
        "ticker": ticker,
        "start_date": df.index.min().date(),
        "end_date": df.index.max().date(),
        "trading_days": len(df),
        "start_price": df["Close"].iloc[0],
        "end_price": df["Close"].iloc[-1],
        "total_return_pct": df["Cumulative_Return"].iloc[-1] * 100,
        "highest_price": df["Close"].max(),
        "highest_date": df["Close"].idxmax().date(),
        "lowest_price": df["Close"].min(),
        "lowest_date": df["Close"].idxmin().date(),
        "avg_daily_return_pct": ret.mean() * 100,
        "daily_volatility_pct": ret.std() * 100,
        "annual_volatility_pct": ann_vol * 100,
        "sharpe_ratio": sharpe,
        "max_drawdown_pct": df["Drawdown"].min() * 100,
        "best_day_pct": ret.max() * 100,
        "worst_day_pct": ret.min() * 100,
        "positive_days_pct": (ret > 0).mean() * 100,
        "trend": detect_trend(df),
    }


def risk_level(annual_vol_pct):
    """Label risk from annualized volatility."""
    if annual_vol_pct < 15:
        return "Low"
    if annual_vol_pct < 30:
        return "Moderate"
    return "High"
