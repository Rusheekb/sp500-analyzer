import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import engine, run_query

st.set_page_config(page_title="S&P 500 Analyzer", layout="wide")

st.title("📈 S&P 500 Stock Performance Analyzer")
st.markdown("Analyzing **AAPL, MSFT, GOOGL, AMZN, JPM** from 2020-2024")

# --- Sidebar filters ---
st.sidebar.header("Filters")
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM"]
selected_tickers = st.sidebar.multiselect("Select Stocks", tickers, default=tickers)
selected_year = st.sidebar.selectbox("Select Year", ["All", "2020", "2021", "2022", "2023", "2024"])

# --- Build query based on filters ---
ticker_filter = "', '".join(selected_tickers)
year_filter = f"AND STRFTIME('%Y', date) = '{selected_year}'" if selected_year != "All" else ""

# --- Section 1: Price Over Time ---
st.subheader("📊 Closing Price Over Time")

price_data = run_query(f"""
    SELECT date, ticker, close
    FROM stock_prices
    WHERE ticker IN ('{ticker_filter}')
    {year_filter}
    ORDER BY date
""")

price_data["date"] = pd.to_datetime(price_data["date"])
fig, ax = plt.subplots(figsize=(12, 4))
for ticker in selected_tickers:
    df = price_data[price_data["ticker"] == ticker]
    ax.plot(df["date"], df["close"], label=ticker)
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Closing Price ($)")
ax.set_title("Stock Closing Prices")
st.pyplot(fig)

# --- Section 2: Average Close ---
st.subheader("💰 Average Closing Price")

avg_data = run_query(f"""
    SELECT ticker, ROUND(AVG(close), 2) as avg_close
    FROM stock_prices
    WHERE ticker IN ('{ticker_filter}')
    {year_filter}
    GROUP BY ticker
    ORDER BY avg_close DESC
""")

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(avg_data["ticker"], avg_data["avg_close"], color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"])
ax2.set_xlabel("Stock")
ax2.set_ylabel("Average Close ($)")
ax2.set_title("Average Closing Price by Stock")
st.pyplot(fig2)

# --- Section 3: Volatility ---
st.subheader("⚡ Volatility (Avg Daily Price Range)")

vol_data = run_query(f"""
    SELECT ticker, ROUND(AVG(high - low), 2) as avg_daily_range
    FROM stock_prices
    WHERE ticker IN ('{ticker_filter}')
    {year_filter}
    GROUP BY ticker
    ORDER BY avg_daily_range DESC
""")

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.bar(vol_data["ticker"], vol_data["avg_daily_range"], color="#ff7f0e")
ax3.set_xlabel("Stock")
ax3.set_ylabel("Avg Daily Range ($)")
ax3.set_title("Stock Volatility")
st.pyplot(fig3)

# --- Section 4: Year over Year ---
st.subheader("📅 Year Over Year Average Close")

yoy_data = run_query(f"""
    SELECT ticker, STRFTIME('%Y', date) as year, ROUND(AVG(close), 2) as avg_close
    FROM stock_prices
    WHERE ticker IN ('{ticker_filter}')
    GROUP BY ticker, year
    ORDER BY year
""")

fig4, ax4 = plt.subplots(figsize=(12, 4))
for ticker in selected_tickers:
    df = yoy_data[yoy_data["ticker"] == ticker]
    ax4.plot(df["year"], df["avg_close"], marker="o", label=ticker)
ax4.legend()
ax4.set_xlabel("Year")
ax4.set_ylabel("Avg Close ($)")
ax4.set_title("Year Over Year Performance")
st.pyplot(fig4)

# --- Section 5: Raw Data Table ---
st.subheader("🗃️ Raw Data")
st.dataframe(price_data)