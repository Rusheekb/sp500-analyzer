import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import yfinance as yf
from portfolio import load_portfolio

st.set_page_config(page_title="News", layout="wide", page_icon="📰")

from styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)

st.title("📰 News Feed")
st.markdown("""
<div style='font-family: IBM Plex Mono, monospace; color: #888; font-size: 12px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;'>
    Latest financial news from Yahoo Finance
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("🔍 News Settings")

portfolio = load_portfolio()
portfolio_tickers = list(portfolio.keys())

source = st.sidebar.radio(
    "Ticker Source",
    ["Custom", "From My Portfolio"],
    index=0
)

if source == "From My Portfolio" and portfolio_tickers:
    tickers = portfolio_tickers
    st.sidebar.success(f"Using {len(tickers)} portfolio tickers")
elif source == "From My Portfolio" and not portfolio_tickers:
    st.sidebar.warning("No portfolio found. Using custom tickers.")
    ticker_input = st.sidebar.text_input("Enter Tickers", value="AAPL, MSFT, NVDA")
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
else:
    ticker_input = st.sidebar.text_input("Enter Tickers", value="AAPL, MSFT, NVDA")
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

max_per_ticker = st.sidebar.slider("Max Articles Per Ticker", 1, 10, 3)
fetch_btn = st.sidebar.button("Fetch News", use_container_width=True)

# --- Fetch News ---
def get_news(tickers, max_per_ticker=3):
    seen = set()
    all_news = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            news = stock.news or []
            count = 0
            for item in news:
                content = item.get("content", {})
                title = content.get("title", "")
                url = content.get("clickThroughUrl", {}).get("url", "")
                summary = content.get("summary", "")
                source = content.get("provider", {}).get("displayName", "")
                date = content.get("displayTime", "")
                thumbnail = content.get("thumbnail", {})
                img_url = ""
                if thumbnail and "resolutions" in thumbnail and thumbnail["resolutions"]:
                    img_url = thumbnail["resolutions"][-1].get("url", "")
                elif thumbnail:
                    img_url = thumbnail.get("originalUrl", "")

                if title and url and title not in seen:
                    seen.add(title)
                    all_news.append({
                        "ticker": ticker,
                        "title": title,
                        "summary": summary,
                        "source": source,
                        "date": date[:10] if date else "",
                        "url": url,
                        "img_url": img_url
                    })
                    count += 1
                    if count >= max_per_ticker:
                        break
        except:
            pass
    return all_news

if fetch_btn or tickers:
    with st.spinner("Fetching latest news..."):
        news_items = get_news(tickers, max_per_ticker)

    if not news_items:
        st.info("No news found for selected tickers.")
    else:
        # --- Filter ---
        col1, col2 = st.columns([2, 4])
        with col1:
            news_filter = st.selectbox("Filter by ticker", ["All"] + tickers)
        
        filtered = news_items if news_filter == "All" else [n for n in news_items if n["ticker"] == news_filter]
        
        st.markdown(f"""
        <div style='font-family: IBM Plex Mono, monospace; color: #666; font-size: 11px; margin-bottom: 16px; text-transform: uppercase;'>
            Showing {len(filtered)} articles
        </div>
        """, unsafe_allow_html=True)

        for item in filtered:
            col1, col2 = st.columns([1, 4])
            with col1:
                if item["img_url"]:
                    st.image(item["img_url"], width=120)
                else:
                    st.markdown("""
                    <div style='width:120px;height:80px;background:#1a1a1a;border:1px solid #333;display:flex;align-items:center;justify-content:center;'>
                        <span style='color:#444;font-size:24px;'>📰</span>
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style='margin-bottom: 4px;'>
                    <a href='{item["url"]}' target='_blank' style='color: #ffffff; font-size: 15px; font-weight: 600; text-decoration: none; font-family: IBM Plex Sans, sans-serif;'>
                        {item["title"]}
                    </a>
                </div>
                """, unsafe_allow_html=True)
                if item["summary"]:
                    st.markdown(f"""
                    <div style='color: #888; font-size: 13px; margin-bottom: 6px; font-family: IBM Plex Sans, sans-serif;'>
                        {item["summary"][:180]}...
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style='font-family: IBM Plex Mono, monospace; font-size: 11px; color: #ff6600; text-transform: uppercase; letter-spacing: 1px;'>
                    📌 {item["ticker"]} · {item["source"]} · {item["date"]}
                </div>
                """, unsafe_allow_html=True)
            st.divider()