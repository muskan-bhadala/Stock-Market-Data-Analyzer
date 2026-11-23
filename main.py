"""main.py - run the whole pipeline.

Usage:
    python main.py                          # AAPL, last 2 years
    python main.py --ticker TCS.NS --start 2023-01-01 --end 2025-01-01
"""
import argparse
import os
from datetime import date, timedelta

from src.analysis import add_indicators, summarize
from src.cleaner import clean_data
from src.data_loader import get_stock_data
from src.report import save_report
from src.visualize import make_all_charts

BASE = os.path.dirname(os.path.abspath(__file__))


def parse_args():
    default_end = date.today()
    default_start = default_end - timedelta(days=730)
    p = argparse.ArgumentParser(description="Stock Market Data Analyzer")
    p.add_argument("--ticker", default="AAPL", help="e.g. AAPL, MSFT, TCS.NS, RELIANCE.NS")
    p.add_argument("--start", default=str(default_start), help="YYYY-MM-DD")
    p.add_argument("--end", default=str(default_end), help="YYYY-MM-DD")
    return p.parse_args()


def run(ticker, start, end):
    raw, source = get_stock_data(ticker, start, end)
    df = clean_data(raw)
    df = add_indicators(df)
    stats = summarize(df, ticker)
    make_all_charts(df, ticker, os.path.join(BASE, "images"))
    text = save_report(stats, source, df, os.path.join(BASE, "reports"), os.path.join(BASE, "outputs"))
    print("\n" + text)
    return df, stats, source


if __name__ == "__main__":
    a = parse_args()
    run(a.ticker.upper(), a.start, a.end)
