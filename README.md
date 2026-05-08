# 📈 Real-Time Stock Analyzer

A Bloomberg-inspired stock analysis platform built with Python, SQL, and AI. Search any ticker, track your portfolio, and get personalized AI-powered insights — all in real time.

## 🌐 Live Demo
👉 [stock-analyzer-project.streamlit.app](https://stock-analyzer-project.streamlit.app)

---

## 🔍 Overview

A full-stack data engineering project that pulls live market data, stores portfolio positions in a cloud PostgreSQL database, and generates personalized AI analysis using real cost basis and P&L data.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| yfinance | Real-time stock data API |
| SQLite / Neon PostgreSQL | Local and cloud database |
| SQLAlchemy | Database ORM |
| Pandas | Data manipulation |
| Matplotlib | Data visualization |
| Streamlit | Multi-page interactive dashboard |
| Groq (Llama 3.3) | AI portfolio analysis |
| Groq API | Free LLM inference |

---

## 📊 Features

### 📈 Market Analysis
- Real-time price data for any ticker symbol
- Closing price chart, volatility, and trading volume
- Scrollable company overview cards with P/E ratio, 52W high/low
- Performance summary with % return over selected period

### 🗓️ Performance by Period
- 1 Day, 1 Week, 1 Month performance tabs
- Best and worst performer highlighted per period
- Scrollable performance cards sorted by return

### 💼 Portfolio Builder
- Add positions with shares, average cost, and dollar invested
- Real-time P&L tracking per position and overall
- Portfolio allocation pie chart
- Historical portfolio value chart over 1 year
- Persistent storage via Neon PostgreSQL — survives redeployments

### 🤖 AI Portfolio Analysis
- Powered by Llama 3.3 via Groq
- References actual cost basis, current price, and dollar P&L per position
- Identifies concentration risk by portfolio weight
- Personalized actionable insight based on real data
- Works with your saved portfolio or any custom set of tickers

### 📰 News Feed
- Latest financial news via Yahoo Finance
- Filter by individual ticker or pull from your portfolio
- Adjustable articles per ticker
- Thumbnail, summary, source, and date per article

---

## 🚀 How to Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/rusheekb/sp500-analyzer.git
cd sp500-analyzer/src
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file in `src/`:**
```GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_neon_postgresql_connection_string```

**4. Launch the dashboard:**
```bash
streamlit run dashboard.py
```

---

## 📁 Project Structure

```
sp500-analyzer/
│
├── src/
│   ├── dashboard.py          # Home page
│   ├── fetch_data.py         # Real-time stock data via yfinance
│   ├── portfolio.py          # Portfolio CRUD with Neon PostgreSQL
│   ├── ai_analysis.py        # AI analysis via Groq
│   ├── styles.py             # Shared Bloomberg-themed CSS
│   ├── database.py           # Local SQLite queries
│   ├── analyze.py            # Advanced SQL analysis
│   └── pages/
│       ├── 1_📊_Market_Analysis.py
│       ├── 2_💼_Portfolio.py
│       ├── 3_🤖_AI_Analysis.py
│       └── 4_📰_News.py
│
├── requirements.txt
├── packages.txt              # System deps for Streamlit Cloud
└── README.md
```
---

## 💡 Key Technical Concepts

- Window functions (`LAG`, `PARTITION BY`) and CTEs in SQL
- Real-time API data ingestion and cleaning
- Cloud PostgreSQL with SQLAlchemy ORM
- Multi-page Streamlit app architecture
- LLM prompt engineering with real financial context
- Streamlit Cloud deployment with secrets management

---

## 👤 Author

Built by Rusheek — [LinkedIn](https://linkedin.com/in/rusheek-bajjuri) · [GitHub](https://github.com/rusheekb)