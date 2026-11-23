"""report.py - Phase 9: write the insights report and processed CSV."""
import os
from datetime import datetime

from src.analysis import risk_level


def build_report_text(s, source):
    risk = risk_level(s["annual_volatility_pct"])
    note = " (DEMO data - not real prices)" if source == "demo" else ""
    return f"""STOCK MARKET DATA ANALYSIS REPORT
=================================
Ticker        : {s['ticker']}{note}
Period        : {s['start_date']} to {s['end_date']} ({s['trading_days']} trading days)
Generated on  : {datetime.now():%Y-%m-%d %H:%M}

PRICE SUMMARY
-------------
Start price   : {s['start_price']:.2f}
End price     : {s['end_price']:.2f}
Total return  : {s['total_return_pct']:.2f}%
Highest close : {s['highest_price']:.2f} on {s['highest_date']}
Lowest close  : {s['lowest_price']:.2f} on {s['lowest_date']}

RETURN & RISK
-------------
Average daily return : {s['avg_daily_return_pct']:.3f}%
Daily volatility     : {s['daily_volatility_pct']:.3f}%
Annual volatility    : {s['annual_volatility_pct']:.2f}%  -> Risk level: {risk}
Sharpe ratio (rf=0)  : {s['sharpe_ratio']:.2f}
Maximum drawdown     : {s['max_drawdown_pct']:.2f}%
Best day / Worst day : {s['best_day_pct']:.2f}% / {s['worst_day_pct']:.2f}%
Positive days        : {s['positive_days_pct']:.1f}%

TREND
-----
Current trend (SMA20 vs SMA50): {s['trend']}

KEY INSIGHTS
------------
1. The stock returned {s['total_return_pct']:.1f}% over the period with {risk.lower()} risk.
2. Its worst peak-to-trough fall was {s['max_drawdown_pct']:.1f}%.
3. The latest trend signal is: {s['trend']}.
4. It closed higher on {s['positive_days_pct']:.0f}% of trading days.

DISCLAIMER: This report is for educational purposes only and is NOT financial advice.
"""


def save_report(s, source, df, reports_dir, outputs_dir):
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)
    text = build_report_text(s, source)
    report_path = os.path.join(reports_dir, f"{s['ticker']}_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(text)
    csv_path = os.path.join(outputs_dir, f"{s['ticker']}_processed.csv")
    df.to_csv(csv_path)
    print(f"[saved] {report_path}")
    print(f"[saved] {csv_path}")
    return text
