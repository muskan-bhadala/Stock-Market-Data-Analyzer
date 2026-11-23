"""app.py - optional Streamlit dashboard.   Run: streamlit run app.py"""
from datetime import date, timedelta

import matplotlib.pyplot as plt
import streamlit as st

from src.analysis import add_indicators, risk_level, summarize
from src.cleaner import clean_data
from src.data_loader import get_stock_data

st.set_page_config(page_title="Stock Market Data Analyzer", layout="wide")
st.title("📈 Stock Market Data Analyzer")
st.caption("Educational project - not financial advice.")

ticker = st.sidebar.text_input("Ticker", "AAPL").upper()
start = st.sidebar.date_input("Start", date.today() - timedelta(days=730))
end = st.sidebar.date_input("End", date.today())

if st.sidebar.button("Analyze"):
    raw, source = get_stock_data(ticker, str(start), str(end))
    df = add_indicators(clean_data(raw))
    s = summarize(df, ticker)
    if source == "demo":
        st.warning("Showing DEMO data (could not fetch real data).")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total return", f"{s['total_return_pct']:.1f}%")
    c2.metric("Annual volatility", f"{s['annual_volatility_pct']:.1f}%", risk_level(s["annual_volatility_pct"]))
    c3.metric("Max drawdown", f"{s['max_drawdown_pct']:.1f}%")
    c4.metric("Trend", s["trend"])

    st.subheader("Close price & moving averages")
    st.line_chart(df[["Close", "SMA_20", "SMA_50", "SMA_200"]])

    st.subheader("Daily return distribution")
    fig, ax = plt.subplots()
    ax.hist(df["Daily_Return"].dropna() * 100, bins=40)
    ax.set_xlabel("Daily return (%)")
    st.pyplot(fig)

    st.subheader("Data preview")
    st.dataframe(df.tail(20))
else:
    st.info("Pick a ticker and dates in the sidebar, then click Analyze.")
