import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
from fetch_data import fetch_stock_data, get_stock_info
import streamlit.components.v1 as components

st.set_page_config(page_title="Market Analysis", layout="wide", page_icon="📊")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');
.stApp { background-color: #0a0a0a; color: #e0e0e0; font-family: 'IBM Plex Sans', sans-serif; }
[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #ff6600; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stSidebar"] input { background-color: #1a1a1a !important; color: #ffffff !important; border: 1px solid #ff6600 !important; border-radius: 2px !important; font-family: 'IBM Plex Mono', monospace !important; }
[data-testid="stSidebar"] .stButton button { background-color: #ff6600 !important; color: #000000 !important; font-family: 'IBM Plex Mono', monospace !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 2px !important; border: none !important; border-radius: 2px !important; width: 100% !important; }
h1 { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 24px !important; text-transform: uppercase !important; letter-spacing: 3px !important; border-bottom: 1px solid #ff6600; padding-bottom: 10px; }
h2, h3 { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; text-transform: uppercase !important; letter-spacing: 2px !important; }
hr { border-color: #222222 !important; }
.stTabs [data-baseweb="tab-list"] { background-color: #111111; border-bottom: 1px solid #ff6600; }
.stTabs [data-baseweb="tab"] { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
.stTabs [aria-selected="true"] { color: #ff6600 !important; border-bottom: 2px solid #ff6600 !important; }
.stSelectbox > div > div { background-color: #1a1a1a !important; border: 1px solid #333333 !important; color: #e0e0e0 !important; border-radius: 2px !important; }
.stSuccess { background-color: #0a1f0a !important; border-left: 3px solid #00ff88 !important; color: #00ff88 !important; }
.stError { background-color: #1f0a0a !important; border-left: 3px solid #ff4444 !important; }
[data-testid="stMetric"] { background-color: #111111; border: 1px solid #222222; padding: 10px; border-radius: 2px; }
[data-testid="stMetricLabel"] { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'IBM Plex Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Market Analysis")

# --- Sidebar ---
st.sidebar.header("🔍 Search Stocks")
ticker_input = st.sidebar.text_input("Enter Ticker Symbols (comma separated)", value="AAPL, MSFT, NVDA")
period = st.sidebar.selectbox("Select Time Period", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
analyze_btn = st.sidebar.button("Analyze", use_container_width=True)

tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

if analyze_btn or tickers:
    all_data = []
    failed = []

    with st.spinner("Fetching live data..."):
        for ticker in tickers:
            df, error = fetch_stock_data(ticker, period=period)
            if error:
                failed.append(ticker)
            else:
                all_data.append(df)

    if failed:
        st.warning(f"Could not find data for: {', '.join(failed)}")

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)

        # --- Company Cards ---
        st.subheader("🏢 Company Overview")
        cards_html = """
        <style>
        .card-container { display: flex; flex-direction: row; overflow-x: auto; gap: 16px; padding: 12px 4px; scrollbar-width: thin; }
        .card { min-width: 180px; max-width: 180px; background-color: #111111; border: 1px solid #333; border-left: 3px solid #ff6600; border-radius: 2px; padding: 16px; flex-shrink: 0; }
        .card-ticker { font-size: 22px; font-weight: bold; color: #ff6600; font-family: IBM Plex Mono, monospace; }
        .card-price { font-size: 20px; font-weight: bold; color: white; margin: 4px 0 10px 0; font-family: IBM Plex Mono, monospace; }
        .card-label { font-size: 10px; color: #666; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; font-family: IBM Plex Mono, monospace; }
        .card-value { font-size: 13px; color: #ccc; font-family: IBM Plex Mono, monospace; }
        </style>
        <div class="card-container">
        """
        for ticker in tickers:
            if ticker not in failed:
                info = get_stock_info(ticker)
                if info:
                    cards_html += f"""
                    <div class="card">
                        <div class="card-ticker">{ticker}</div>
                        <div class="card-price">${info['current_price']}</div>
                        <div class="card-label">Company</div>
                        <div class="card-value">{info['name'][:20]}</div>
                        <div class="card-label">Sector</div>
                        <div class="card-value">{info['sector']}</div>
                        <div class="card-label">P/E Ratio</div>
                        <div class="card-value">{info['pe_ratio']}</div>
                        <div class="card-label">52W High</div>
                        <div class="card-value">${info['52w_high']}</div>
                        <div class="card-label">52W Low</div>
                        <div class="card-value">${info['52w_low']}</div>
                    </div>
                    """
        cards_html += "</div>"
        components.html(cards_html, height=280, scrolling=False)
        st.divider()

        # --- Price Chart ---
        st.subheader("📊 Closing Price Over Time")
        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor('#0a0a0a')
        ax.set_facecolor('#111111')
        for ticker in tickers:
            df = combined[combined["ticker"] == ticker]
            ax.plot(df["date"], df["close"], label=ticker, linewidth=2)
        ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='#ccc')
        ax.set_xlabel("Date", color='#888')
        ax.set_ylabel("Price ($)", color='#888')
        ax.tick_params(colors='#888888')
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        for spine in ax.spines.values():
            spine.set_edgecolor('#333333')
        fig.autofmt_xdate()
        st.pyplot(fig)
        st.divider()

        # --- Performance Summary ---
        st.subheader("📈 Performance Summary")
        perf_html = """
        <style>
        .perf-container { display: flex; flex-direction: row; overflow-x: auto; gap: 16px; padding: 12px 4px; scrollbar-width: thin; }
        .perf-card { min-width: 160px; max-width: 160px; background-color: #111111; border: 1px solid #333; border-radius: 2px; padding: 16px; flex-shrink: 0; }
        .perf-ticker { font-size: 14px; color: #888; margin-bottom: 4px; font-family: IBM Plex Mono, monospace; text-transform: uppercase; }
        .perf-price { font-size: 22px; font-weight: bold; color: white; margin-bottom: 8px; font-family: IBM Plex Mono, monospace; }
        .perf-positive { font-size: 14px; font-weight: bold; color: #00ff88; font-family: IBM Plex Mono, monospace; }
        .perf-negative { font-size: 14px; font-weight: bold; color: #ff4444; font-family: IBM Plex Mono, monospace; }
        </style>
        <div class="perf-container">
        """
        for ticker in tickers:
            df = combined[combined["ticker"] == ticker].sort_values("date")
            if not df.empty:
                start_price = df.iloc[0]["close"]
                end_price = df.iloc[-1]["close"]
                change_pct = ((end_price - start_price) / start_price) * 100
                color_class = "perf-positive" if change_pct >= 0 else "perf-negative"
                arrow = "▲" if change_pct >= 0 else "▼"
                perf_html += f"""
                <div class="perf-card">
                    <div class="perf-ticker">{ticker}</div>
                    <div class="perf-price">${end_price:.2f}</div>
                    <div class="{color_class}">{arrow} {change_pct:.2f}%</div>
                </div>
                """
        perf_html += "</div>"
        components.html(perf_html, height=160, scrolling=False)
        st.divider()

        # --- Volatility ---
        st.subheader("⚡ Volatility")
        vol_data = combined.groupby("ticker").apply(lambda x: (x["high"] - x["low"]).mean()).reset_index()
        vol_data.columns = ["ticker", "avg_daily_range"]
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        fig2.patch.set_facecolor('#0a0a0a')
        ax2.set_facecolor('#111111')
        ax2.bar(vol_data["ticker"], vol_data["avg_daily_range"], color="#ff6600")
        ax2.tick_params(colors='#888888')
        ax2.set_ylabel("Avg Daily Range ($)", color='#888')
        for spine in ax2.spines.values():
            spine.set_edgecolor('#333333')
        st.pyplot(fig2)
        st.divider()

        # --- Volume ---
        st.subheader("📦 Trading Volume")
        fig3, ax3 = plt.subplots(figsize=(12, 3))
        fig3.patch.set_facecolor('#0a0a0a')
        ax3.set_facecolor('#111111')
        for ticker in tickers:
            df = combined[combined["ticker"] == ticker]
            ax3.fill_between(df["date"], df["volume"], alpha=0.4, label=ticker)
        ax3.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='#ccc')
        ax3.tick_params(colors='#888888')
        ax3.set_ylabel("Volume", color='#888')
        ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        for spine in ax3.spines.values():
            spine.set_edgecolor('#333333')
        fig3.autofmt_xdate()
        st.pyplot(fig3)
        st.divider()

        # --- Raw Data ---
        st.subheader("🗃️ Raw Data")
        selected = st.selectbox("Select ticker", tickers)
        st.dataframe(combined[combined["ticker"] == selected].sort_values("date", ascending=False), use_container_width=True)