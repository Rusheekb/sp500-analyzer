import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from fetch_data import fetch_stock_data, get_stock_info
from portfolio import load_portfolio, get_portfolio_value
from ai_analysis import generate_portfolio_analysis

st.set_page_config(page_title="AI Analysis", layout="wide", page_icon="🤖")

from styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)

st.title("🤖 AI Portfolio Analysis")
st.markdown("""
<div style='font-family: IBM Plex Mono, monospace; color: #888; font-size: 12px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;'>
    Powered by Llama 3.3 via Groq — analyzes your portfolio or any custom set of tickers
</div>
""", unsafe_allow_html=True)

# --- Mode selector ---
mode = st.radio(
    "Analyze:",
    ["My Portfolio", "Custom Tickers"],
    horizontal=True
)

st.divider()

if mode == "My Portfolio":
    portfolio = load_portfolio()

    if not portfolio:
        st.info("No portfolio positions found. Add stocks on the Portfolio page first.")
    else:
        st.markdown("#### 📋 Current Positions")
        for ticker, pos in portfolio.items():
            st.markdown(f"""
            <div style='font-family: IBM Plex Mono, monospace; font-size: 12px; color: #ccc; padding: 4px 0;'>
                <span style='color: #ff6600;'>{ticker}</span> — {pos['shares']} shares @ ${pos['avg_cost']:.2f} avg cost
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        period = st.selectbox("Analysis Period", ["1mo", "3mo", "6mo", "1y"], index=0)

        if st.button("Generate AI Analysis", use_container_width=False):
            with st.spinner("Fetching data and generating analysis..."):
                rows = []
                for ticker, position in portfolio.items():
                    df, error = fetch_stock_data(ticker, period=period)
                    if not error and df is not None and len(df) >= 2:
                        start = df.iloc[0]["close"]
                        end = df.iloc[-1]["close"]
                        change_pct = ((end - start) / start) * 100
                        info = get_stock_info(ticker)
                        current_price = info["current_price"] if info else end
                        current_value = position["shares"] * float(current_price) if current_price != "N/A" else 0
                        profit_loss = current_value - position["invested"]
                        rows.append({
                            "ticker": ticker,
                            "shares": position["shares"],
                            "avg_cost": position["avg_cost"],
                            "invested": position["invested"],
                            "start": round(start, 2),
                            "end": round(end, 2),
                            "change_pct": round(change_pct, 2),
                            "current_value": round(current_value, 2),
                            "profit_loss": round(profit_loss, 2)
                        })

                if rows:
                    try:
                        analysis = generate_portfolio_analysis(rows)
                        st.markdown(f"""
                        <div style='background:#111;border:1px solid #333;border-left:3px solid #ff6600;padding:24px;border-radius:2px;font-family:IBM Plex Sans,sans-serif;color:#e0e0e0;line-height:1.8;'>
                            {analysis.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")

else:
    # --- Custom Tickers ---
    ticker_input = st.text_input("Enter Ticker Symbols (comma separated)", value="AAPL, MSFT, NVDA")
    period = st.selectbox("Analysis Period", ["1mo", "3mo", "6mo", "1y"], index=0)
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

    if st.button("Generate AI Analysis", use_container_width=False):
        with st.spinner("Fetching data and generating analysis..."):
            rows = []
            for ticker in tickers:
                df, error = fetch_stock_data(ticker, period=period)
                if not error and df is not None and len(df) >= 2:
                    start = df.iloc[0]["close"]
                    end = df.iloc[-1]["close"]
                    change_pct = ((end - start) / start) * 100
                    rows.append({
                        "ticker": ticker,
                        "start": round(start, 2),
                        "end": round(end, 2),
                        "change_pct": round(change_pct, 2),
                        "invested": round(start, 2),
                        "profit_loss": round(end - start, 2)
                    })

            if rows:
                try:
                    analysis = generate_portfolio_analysis(rows)
                    st.markdown(f"""
                    <div style='background:#111;border:1px solid #333;border-left:3px solid #ff6600;padding:24px;border-radius:2px;font-family:IBM Plex Sans,sans-serif;color:#e0e0e0;line-height:1.8;'>
                        {analysis.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating analysis: {str(e)}")