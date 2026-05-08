import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period="1y"):
    """
    Fetch real-time stock data for any ticker.
    period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return None, f"No data found for ticker: {ticker}"
        
        # Clean up
        df = df.reset_index()
        df.columns = [col.lower() for col in df.columns]
        df["ticker"] = ticker.upper()
        df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
        df = df[["date", "ticker", "open", "high", "low", "close", "volume"]]
        
        return df, None
    
    except Exception as e:
        return None, str(e)

def get_stock_info(ticker):
    """Get company info for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "name": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
        }
    except:
        return None

if __name__ == "__main__":
    # Test with a few tickers
    for ticker in ["AAPL", "NVDA", "TSLA"]:
        df, error = fetch_stock_data(ticker, period="1mo")
        if error:
            print(f"Error: {error}")
        else:
            print(f"{ticker}: {len(df)} rows fetched")
        
        info = get_stock_info(ticker)
        if info:
            print(f"Company: {info['name']}")
            print(f"Current Price: ${info['current_price']}")
            print()