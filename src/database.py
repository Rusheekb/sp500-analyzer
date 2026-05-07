import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/stocks.db")

def load_data_to_db():
    df = pd.read_csv("data/raw_stock_data.csv")
    print("Columns:", df.columns.tolist())
    print("Sample:\n", df.head())
    
    df.to_sql("stock_prices", engine, if_exists="replace", index=False)
    print("Data loaded into stocks.db successfully!")

def run_query(query):
    with engine.connect() as conn:
        result = pd.read_sql(text(query), conn)
        return result

if __name__ == "__main__":
    load_data_to_db()
    
    print("\n--- Top 5 rows ---")
    print(run_query("SELECT * FROM stock_prices LIMIT 5"))
    
    print("\n--- Average closing price per stock ---")
    print(run_query("""
        SELECT ticker, ROUND(AVG(close), 2) as avg_close
        FROM stock_prices
        GROUP BY ticker
        ORDER BY avg_close DESC
    """))
    
    print("\n--- Highest single day close per stock ---")
    print(run_query("""
        SELECT ticker, ROUND(MAX(close), 2) as max_close
        FROM stock_prices
        GROUP BY ticker
        ORDER BY max_close DESC
    """))