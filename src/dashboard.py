import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

st.set_page_config(page_title="Stock Analyzer", layout="wide", page_icon="📈")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');

.stApp {
    background-color: #0a0a0a;
    color: #e0e0e0;
    font-family: 'IBM Plex Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #ff6600;
}
h1 {
    color: #ff6600 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 3px !important;
    border-bottom: 1px solid #ff6600;
    padding-bottom: 10px;
}
h2, h3 {
    color: #ff6600 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 Real-Time Stock Analyzer")

st.markdown("""
<div style='font-family: IBM Plex Mono, monospace; color: #888; font-size: 13px; margin-bottom: 30px;'>
    A Bloomberg-inspired stock analysis tool powered by real-time market data and AI.
</div>
""", unsafe_allow_html=True)

# --- Feature Cards ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background:#111;border:1px solid #333;border-left:3px solid #ff6600;padding:20px;margin-bottom:16px;border-radius:2px;'>
        <div style='color:#ff6600;font-family:IBM Plex Mono,monospace;font-size:12px;text-transform:uppercase;letter-spacing:2px;'>📊 Market Analysis</div>
        <div style='color:#ccc;font-size:13px;margin-top:8px;'>Real-time price charts, volatility, volume and performance across any ticker.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#111;border:1px solid #333;border-left:3px solid #ff6600;padding:20px;margin-bottom:16px;border-radius:2px;'>
        <div style='color:#ff6600;font-family:IBM Plex Mono,monospace;font-size:12px;text-transform:uppercase;letter-spacing:2px;'>💼 Portfolio Builder</div>
        <div style='color:#ccc;font-size:13px;margin-top:8px;'>Track your positions, monitor P&L, and visualize your portfolio value over time.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background:#111;border:1px solid #333;border-left:3px solid #ff6600;padding:20px;margin-bottom:16px;border-radius:2px;'>
        <div style='color:#ff6600;font-family:IBM Plex Mono,monospace;font-size:12px;text-transform:uppercase;letter-spacing:2px;'>🤖 AI Analysis</div>
        <div style='color:#ccc;font-size:13px;margin-top:8px;'>AI-powered portfolio insights and personalized performance summaries.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#111;border:1px solid #333;border-left:3px solid #ff6600;padding:20px;margin-bottom:16px;border-radius:2px;'>
        <div style='color:#ff6600;font-family:IBM Plex Mono,monospace;font-size:12px;text-transform:uppercase;letter-spacing:2px;'>📰 News Feed</div>
        <div style='color:#ccc;font-size:13px;margin-top:8px;'>Latest financial news filtered by your tracked tickers.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='font-family:IBM Plex Mono,monospace;color:#444;font-size:11px;margin-top:40px;text-transform:uppercase;letter-spacing:1px;'>
    ← Use the sidebar to navigate
</div>
""", unsafe_allow_html=True)