import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from fetch_data import fetch_stock_data, get_stock_info
import streamlit.components.v1 as components
from ai_analysis import generate_portfolio_analysis

st.set_page_config(page_title="Stock Analyzer", layout="wide", page_icon="📈")

# --- Header ---
st.title("📈 Real-Time Stock Analyzer")
st.markdown("Search any stock ticker and analyze its performance in real time.")

# --- Sidebar ---
st.sidebar.header("🔍 Search Stocks")

ticker_input = st.sidebar.text_input(
    "Enter Ticker Symbols (comma separated)",
    value="AAPL, MSFT, NVDA",
    placeholder="e.g. AAPL, TSLA, GOOGL"
)

period = st.sidebar.selectbox(
    "Select Time Period",
    options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

analyze_btn = st.sidebar.button("Analyze", use_container_width=True)

# --- Parse tickers ---
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

if analyze_btn or tickers:
    # --- Fetch data for all tickers ---
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

        # --- Company Info Cards ---
        st.subheader("🏢 Company Overview")

        cards_html = """
        <style>
        .card-container {
            display: flex;
            flex-direction: row;
            overflow-x: auto;
            gap: 16px;
            padding: 12px 4px;
            scrollbar-width: thin;
        }
        .card {
            min-width: 180px;
            max-width: 180px;
            background-color: #1e1e2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 16px;
            flex-shrink: 0;
        }
        .card-ticker {
            font-size: 22px;
            font-weight: bold;
            color: #00d4aa;
        }
        .card-price {
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin: 4px 0 10px 0;
        }
        .card-label {
            font-size: 11px;
            color: #888;
            margin-top: 6px;
        }
        .card-value {
            font-size: 13px;
            color: #ccc;
        }
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
        st.components.v1.html(cards_html, height=280, scrolling=False)

        # --- Daily/Weekly/Monthly Performance ---
        st.subheader("🗓️ Performance by Period")

        periods = {"1D": "1d", "1W": "5d", "1M": "1mo"}
        period_data = {}

        with st.spinner("Loading period performance..."):
            for label, p in periods.items():
                rows = []
                for ticker in tickers:
                    df, error = fetch_stock_data(ticker, period=p)
                    if not error and df is not None and len(df) >= 2:
                        start = df.iloc[0]["close"]
                        end = df.iloc[-1]["close"]
                        change_pct = ((end - start) / start) * 100
                        rows.append({
                            "ticker": ticker,
                            "start": round(start, 2),
                            "end": round(end, 2),
                            "change_pct": round(change_pct, 2)
                        })
                period_data[label] = pd.DataFrame(rows)
        # --- AI Portfolio Analysis ---
        st.subheader("🤖 AI Portfolio Analysis")

        if st.button("Generate AI Analysis", use_container_width=False):
            df_month = period_data.get("1M", pd.DataFrame())
            
            if df_month.empty:
                st.warning("Not enough data to generate analysis.")
            else:
                portfolio_list = df_month.to_dict(orient="records")
                
                with st.spinner("Analyzing your portfolio..."):
                    try:
                        analysis = generate_portfolio_analysis(portfolio_list)
                        st.markdown(analysis)
                    except Exception as e:
                        st.error(f"Error generating analysis: {str(e)}")

        st.divider()
        # --- Period tabs ---
        tab1, tab2, tab3 = st.tabs(["📅 1 Day", "📅 1 Week", "📅 1 Month"])

        for tab, label in zip([tab1, tab2, tab3], ["1D", "1W", "1M"]):
            with tab:
                df_period = period_data[label]
                if df_period.empty:
                    st.info("No data available for this period.")
                    continue

                # Best and worst
                best = df_period.loc[df_period["change_pct"].idxmax()]
                worst = df_period.loc[df_period["change_pct"].idxmin()]

                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"🏆 Best: **{best['ticker']}** at {best['change_pct']}%")
                with col2:
                    st.error(f"📉 Worst: **{worst['ticker']}** at {worst['change_pct']}%")

                # Performance table
                period_html = """
                <style>
                .period-container {
                    display: flex;
                    flex-direction: row;
                    overflow-x: auto;
                    gap: 12px;
                    padding: 12px 4px;
                    scrollbar-width: thin;
                }
                .period-card {
                    min-width: 140px;
                    max-width: 140px;
                    background-color: #1e1e2e;
                    border: 1px solid #333;
                    border-radius: 12px;
                    padding: 14px;
                    flex-shrink: 0;
                }
                .period-ticker {
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    margin-bottom: 6px;
                }
                .period-price {
                    font-size: 13px;
                    color: #888;
                    margin-bottom: 4px;
                }
                .period-positive {
                    font-size: 15px;
                    font-weight: bold;
                    color: #00d4aa;
                }
                .period-negative {
                    font-size: 15px;
                    font-weight: bold;
                    color: #ff4d4d;
                }
                </style>
                <div class="period-container">
                """

                for _, row in df_period.sort_values("change_pct", ascending=False).iterrows():
                    color_class = "period-positive" if row["change_pct"] >= 0 else "period-negative"
                    arrow = "▲" if row["change_pct"] >= 0 else "▼"
                    period_html += f"""
                    <div class="period-card">
                        <div class="period-ticker">{row['ticker']}</div>
                        <div class="period-price">${row['start']} → ${row['end']}</div>
                        <div class="{color_class}">{arrow} {row['change_pct']}%</div>
                    </div>
                    """

                period_html += "</div>"
                st.components.v1.html(period_html, height=160, scrolling=False)

        st.divider()

        # --- Price Over Time ---
        st.subheader("📊 Closing Price Over Time")
        fig, ax = plt.subplots(figsize=(12, 4))
        for ticker in tickers:
            df = combined[combined["ticker"] == ticker]
            ax.plot(df["date"], df["close"], label=ticker, linewidth=2)
        ax.legend()
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        fig.autofmt_xdate()
        st.pyplot(fig)

        st.divider()

        # --- Performance Metrics ---
        st.subheader("📈 Performance Summary")

        perf_html = """
        <style>
        .perf-container {
            display: flex;
            flex-direction: row;
            overflow-x: auto;
            gap: 16px;
            padding: 12px 4px;
            scrollbar-width: thin;
        }
        .perf-card {
            min-width: 160px;
            max-width: 160px;
            background-color: #1e1e2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 16px;
            flex-shrink: 0;
        }
        .perf-ticker {
            font-size: 14px;
            color: #888;
            margin-bottom: 4px;
        }
        .perf-price {
            font-size: 22px;
            font-weight: bold;
            color: white;
            margin-bottom: 8px;
        }
        .perf-positive {
            font-size: 14px;
            font-weight: bold;
            color: #00d4aa;
        }
        .perf-negative {
            font-size: 14px;
            font-weight: bold;
            color: #ff4d4d;
        }
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
                    <div class="perf-ticker">{ticker} Return</div>
                    <div class="perf-price">${end_price:.2f}</div>
                    <div class="{color_class}">{arrow} {change_pct:.2f}%</div>
                </div>
                """

        perf_html += "</div>"
        st.components.v1.html(perf_html, height=160, scrolling=False)

        # --- Volatility ---
        st.subheader("⚡ Volatility (Avg Daily Range)")
        vol_data = combined.groupby("ticker").apply(
            lambda x: (x["high"] - x["low"]).mean()
        ).reset_index()
        vol_data.columns = ["ticker", "avg_daily_range"]
        vol_data = vol_data.sort_values("avg_daily_range", ascending=False)

        fig2, ax2 = plt.subplots(figsize=(8, 3))
        ax2.bar(vol_data["ticker"], vol_data["avg_daily_range"], color="#ff7f0e")
        ax2.set_xlabel("Stock")
        ax2.set_ylabel("Avg Daily Range ($)")
        st.pyplot(fig2)

        st.divider()

        # --- Volume Over Time ---
        st.subheader("📦 Trading Volume Over Time")
        fig3, ax3 = plt.subplots(figsize=(12, 3))
        for ticker in tickers:
            df = combined[combined["ticker"] == ticker]
            ax3.fill_between(df["date"], df["volume"], alpha=0.4, label=ticker)
        ax3.legend()
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Volume")
        ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        fig3.autofmt_xdate()
        st.pyplot(fig3)

        st.divider()

        # --- Raw Data ---
        st.subheader("🗃️ Raw Data")
        selected = st.selectbox("Select ticker to view raw data", tickers)
        st.dataframe(
            combined[combined["ticker"] == selected].sort_values("date", ascending=False),
            use_container_width=True
        )