"""visualize.py - Phase 8: save charts as PNG files into images/."""
import os

import matplotlib

matplotlib.use("Agg")  # lets charts save even without a display
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def _save(fig, folder, name):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[saved] {path}")
    return path


def plot_close_price(df, ticker, folder):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df.index, df["Close"], color="#1f77b4", label="Close")
    hi, lo = df["Close"].idxmax(), df["Close"].idxmin()
    ax.scatter([hi], [df["Close"].max()], color="green", zorder=5, label="Highest")
    ax.scatter([lo], [df["Close"].min()], color="red", zorder=5, label="Lowest")
    ax.set_title(f"{ticker} - Closing Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    return _save(fig, folder, "01_closing_price.png")


def plot_moving_averages(df, ticker, folder):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df.index, df["Close"], label="Close", alpha=0.6)
    ax.plot(df.index, df["SMA_20"], label="SMA 20")
    ax.plot(df.index, df["SMA_50"], label="SMA 50")
    ax.plot(df.index, df["SMA_200"], label="SMA 200")
    ax.set_title(f"{ticker} - Moving Averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    return _save(fig, folder, "02_moving_averages.png")


def plot_daily_returns(df, ticker, folder):
    ret = df["Daily_Return"].dropna() * 100
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(ret.index, ret, color="gray", linewidth=0.8)
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set_title("Daily Returns (%)")
    sns.histplot(ret, bins=40, kde=True, ax=axes[1], color="#ff7f0e")
    axes[1].set_title("Return Distribution")
    axes[1].set_xlabel("Daily return (%)")
    fig.suptitle(f"{ticker} - Return Analysis")
    return _save(fig, folder, "03_daily_returns.png")


def plot_volatility(df, ticker, folder):
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].plot(df.index, df["Volatility_20d"] * 100, color="purple")
    axes[0].set_title(f"{ticker} - 20-day Rolling Volatility (annualized %)")
    axes[1].fill_between(df.index, df["Drawdown"] * 100, 0, color="crimson", alpha=0.5)
    axes[1].set_title("Drawdown from Peak (%)")
    return _save(fig, folder, "04_volatility_drawdown.png")


def make_all_charts(df, ticker, folder):
    return [
        plot_close_price(df, ticker, folder),
        plot_moving_averages(df, ticker, folder),
        plot_daily_returns(df, ticker, folder),
        plot_volatility(df, ticker, folder),
    ]
