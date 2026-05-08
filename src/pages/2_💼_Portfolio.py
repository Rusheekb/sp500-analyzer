import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit.components.v1 as components
from fetch_data import fetch_stock_data, get_stock_info
from portfolio import load_portfolio, add_position, remove_position, get_portfolio_value

st.set_page_config(page_title="Portfolio", layout="wide", page_icon="💼")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');
.stApp { background-color: #0a0a0a; color: #e0e0e0; font-family: 'IBM Plex Sans', sans-serif; }
[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #ff6600; }
h1 { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 24px !important; text-transform: uppercase !important; letter-spacing: 3px !important; border-bottom: 1px solid #ff6600; padding-bottom: 10px; }
h2, h3, h4 { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; text-transform: uppercase !important; letter-spacing: 2px !important; }
hr { border-color: #222222 !important; }
.stSelectbox > div > div { background-color: #1a1a1a !important; border: 1px solid #333333 !important; color: #e0e0e0 !important; border-radius: 2px !important; }
[data-testid="stMetric"] { background-color: #111111; border: 1px solid #222222; padding: 10px; border-radius: 2px; }
[data-testid="stMetricLabel"] { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'IBM Plex Mono', monospace !important; }
.stButton button { background-color: #1a1a1a !important; color: #ff6600 !important; border: 1px solid #ff6600 !important; border-radius: 2px !important; font-family: 'IBM Plex Mono', monospace !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
.stButton button:hover { background-color: #ff6600 !important; color: #000000 !important; }
.stSuccess { background-color: #0a1f0a !important; border-left: 3px solid #00ff88 !important; }
.stError { background-color: #1f0a0a !important; border-left: 3px solid #ff4444 !important; }
</style>
""", unsafe_allow_html=True)

st.title("💼 Portfolio Builder")

portfolio = load_portfolio()

# --- Add Position ---
with st.expander("➕ Add / Update Position", expanded=len(portfolio) == 0):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_ticker = st.text_input("Ticker", placeholder="e.g. AAPL").upper().strip()
    with col2:
        new_shares = st.number_input("Shares", min_value=0.01, value=1.0, step=0.01)
    with col3:
        new_avg_cost = st.number_input("Avg Cost Per Share ($)", min_value=0.01, value=100.0, step=0.01)

    if st.button("Save Position"):
        if new_ticker:
            add_position(new_ticker, new_shares, new_avg_cost)
            st.success(f"✅ {new_ticker} saved to portfolio!")
            st.rerun()
        else:
            st.warning("Please enter a ticker symbol.")

if not portfolio:
    st.info("No positions yet. Add your first stock above.")
else:
    # --- Fetch current prices ---
    with st.spinner("Fetching current prices..."):
        current_prices = {}
        for ticker in portfolio.keys():
            info = get_stock_info(ticker)
            if info and info["current_price"] != "N/A":
                current_prices[ticker] = float(info["current_price"])

    summary = get_portfolio_value(portfolio, current_prices)

    # --- Summary Metrics ---
    st.markdown("#### 📊 Portfolio Summary")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Invested", f"${summary['total_invested']:,.2f}")
    with m2:
        st.metric("Current Value", f"${summary['total_value']:,.2f}")
    with m3:
        st.metric("Total P&L", f"${summary['total_profit_loss']:,.2f}",
                 delta=f"{summary['total_profit_loss_pct']:+.2f}%")
    with m4:
        st.metric("Positions", len(portfolio))

    st.divider()

    # --- Position Cards ---
    st.markdown("#### 📋 Your Positions")
    positions_html = """
    <style>
    .pos-container { display: flex; flex-direction: row;overflow-x: auto; flex-wrap: nowrap;gap: 12px; padding: 8px 4px; scrollbar-width: thin;}
    .pos-card { min-width: 200px;max-width: 200px;flex-shrink: 0;background-color: #111111; border: 1px solid #333; border-left: 3px solid #ff6600; border-radius: 2px; padding: 16px; }
    .pos-ticker { font-size: 20px; font-weight: bold; color: #ff6600; font-family: IBM Plex Mono, monospace; }
    .pos-value { font-size: 18px; color: white; font-family: IBM Plex Mono, monospace; margin: 4px 0; }
    .pos-label { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-top: 8px; font-family: IBM Plex Mono, monospace; }
    .pos-detail { font-size: 13px; color: #ccc; font-family: IBM Plex Mono, monospace; }
    .pos-positive { color: #00ff88; font-weight: bold; font-family: IBM Plex Mono, monospace; }
    .pos-negative { color: #ff4444; font-weight: bold; font-family: IBM Plex Mono, monospace; }
    </style>
    <div class="pos-container">
    """
    for pos in summary["positions"]:
        pl_class = "pos-positive" if pos["profit_loss"] >= 0 else "pos-negative"
        arrow = "▲" if pos["profit_loss"] >= 0 else "▼"
        positions_html += f"""
        <div class="pos-card">
            <div class="pos-ticker">{pos['ticker']}</div>
            <div class="pos-value">${pos['current_value']:,.2f}</div>
            <div class="{pl_class}">{arrow} ${pos['profit_loss']:,.2f} ({pos['profit_loss_pct']:+.2f}%)</div>
            <div class="pos-label">Shares</div>
            <div class="pos-detail">{pos['shares']}</div>
            <div class="pos-label">Avg Cost</div>
            <div class="pos-detail">${pos['avg_cost']:,.2f}</div>
            <div class="pos-label">Current Price</div>
            <div class="pos-detail">${pos['current_price']:,.2f}</div>
            <div class="pos-label">Invested</div>
            <div class="pos-detail">${pos['invested']:,.2f}</div>
        </div>
        """
    positions_html += "</div>"
    components.html(positions_html, height=280, scrolling=False)
    st.divider()

    # --- Allocation Pie Chart ---
    st.markdown("#### 🥧 Portfolio Allocation")

    col_pie, col_table = st.columns([1, 1])

    with col_pie:
        fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
        fig_pie.patch.set_facecolor('#0a0a0a')
        ax_pie.set_facecolor('#0a0a0a')
        labels = [p["ticker"] for p in summary["positions"]]
        sizes = [p["current_value"] for p in summary["positions"]]
        colors = ["#ff6600", "#ff8800", "#ffaa00", "#ffcc00",
                "#00ff88", "#00ccff", "#cc00ff", "#ff0066",
                "#00ffcc", "#ff3300", "#ffdd00", "#33ff00"]
        wedges, texts, autotexts = ax_pie.pie(
            sizes,
            labels=None,
            colors=colors[:len(labels)],
            autopct="%1.1f%%",
            textprops={"color": "#ccc", "fontfamily": "monospace", "fontsize": 9},
            wedgeprops={"edgecolor": "#0a0a0a", "linewidth": 2},
            pctdistance=0.75
        )
        ax_pie.legend(
            wedges, labels,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=9,
            facecolor="#111",
            edgecolor="#333",
            labelcolor="#ccc"
        )
        fig_pie.tight_layout()
        st.pyplot(fig_pie)

    with col_table:
        st.markdown("""
        <div style='font-family: IBM Plex Mono, monospace;'>
        """, unsafe_allow_html=True)
        for i, pos in enumerate(sorted(summary["positions"], key=lambda x: x["current_value"], reverse=True)):
            pct = (pos["current_value"] / summary["total_value"] * 100) if summary["total_value"] > 0 else 0
            color = colors[i % len(colors)]
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #222;'>
                <div style='display:flex;align-items:center;gap:10px;'>
                    <div style='width:10px;height:10px;background:{color};border-radius:50%;'></div>
                    <span style='color:#ff6600;font-size:13px;'>{pos['ticker']}</span>
                </div>
                <div style='text-align:right;'>
                    <span style='color:#fff;font-size:13px;'>${pos['current_value']:,.2f}</span>
                    <span style='color:#888;font-size:11px;margin-left:8px;'>{pct:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # --- Portfolio Value Over Time ---
    st.markdown("#### 📈 Portfolio Value Over Time")
    with st.spinner("Building historical chart..."):
        port_history = []
        for ticker, position in portfolio.items():
            df, error = fetch_stock_data(ticker, period="1y")
            if not error and df is not None:
                df["position_value"] = df["close"] * position["shares"]
                port_history.append(df[["date", "position_value"]])

        if port_history:
            combined_port = port_history[0].copy()
            for ph in port_history[1:]:
                combined_port = combined_port.merge(ph, on="date", suffixes=("", "_extra"))
                extra_cols = [c for c in combined_port.columns if c.endswith("_extra")]
                for col in extra_cols:
                    combined_port["position_value"] += combined_port[col]
                combined_port.drop(columns=extra_cols, inplace=True)

            fig_port, ax_port = plt.subplots(figsize=(12, 4))
            fig_port.patch.set_facecolor('#0a0a0a')
            ax_port.set_facecolor('#111111')
            ax_port.plot(combined_port["date"], combined_port["position_value"],
                        color="#ff6600", linewidth=2)
            ax_port.fill_between(combined_port["date"], combined_port["position_value"],
                                alpha=0.1, color="#ff6600")
            ax_port.tick_params(colors='#888888')
            ax_port.set_ylabel("Portfolio Value ($)", color='#888')
            for spine in ax_port.spines.values():
                spine.set_edgecolor('#333333')
            ax_port.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            fig_port.autofmt_xdate()
            st.pyplot(fig_port)

    st.divider()

    # --- Remove Position ---
    st.markdown("#### 🗑️ Remove Position")
    remove_ticker = st.selectbox("Select position to remove", list(portfolio.keys()))
    if st.button("Remove Position"):
        remove_position(remove_ticker)
        st.success(f"Removed {remove_ticker} from portfolio.")
        st.rerun()