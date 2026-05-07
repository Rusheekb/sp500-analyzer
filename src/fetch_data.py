import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM"]

def fetch_stock_data(tickers, start="2020-01-01", end="2024-12-31"):
    all_data = []

    for ticker in tickers:
        print(f"Fetching {ticker}...")
        df = yf.download(ticker, start=start, end=end, auto_adjust=True)
        
        # Flatten columns if multi-level
        df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() 
                     for col in df.columns]
        
        # Reset index so Date becomes a column
        df = df.reset_index()
        df.columns = [col.lower() for col in df.columns]
        
        # Add ticker column
        df["ticker"] = ticker
        
        # Keep only what we need
        df = df[["date", "ticker", "open", "high", "low", "close", "volume"]]
        
        all_data.append(df)

    combined = pd.concat(all_data, ignore_index=True)
    combined.to_csv("data/raw_stock_data.csv", index=False)
    print(f"Done! {len(combined)} rows saved to data/raw_stock_data.csv")
    return combined

if __name__ == "__main__":
    fetch_stock_data(tickers)