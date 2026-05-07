import pandas as pd
from database import engine, run_query

def analyze_stocks():

    print("--- Daily Return % per Stock ---")
    print(run_query("""
        SELECT 
            date,
            ticker,
            ROUND(close, 2) as close,
            ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
                / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) as daily_return_pct
        FROM stock_prices
        ORDER BY ticker, date
        LIMIT 20
    """))

    print("\n--- Most Volatile Stock (Avg Daily Range) ---")
    print(run_query("""
        SELECT 
            ticker,
            ROUND(AVG(high - low), 2) as avg_daily_range
        FROM stock_prices
        GROUP BY ticker
        ORDER BY avg_daily_range DESC
    """))

    print("\n--- Best Single Day % Gain per Stock ---")
    print(run_query("""
        WITH daily_returns AS (
            SELECT 
                date,
                ticker,
                ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
                    / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) as return_pct
            FROM stock_prices
        )
        SELECT ticker, MAX(return_pct) as best_day_pct
        FROM daily_returns
        GROUP BY ticker
        ORDER BY best_day_pct DESC
    """))

    print("\n--- Worst Single Day % Loss per Stock ---")
    print(run_query("""
        WITH daily_returns AS (
            SELECT 
                date,
                ticker,
                ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
                    / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) as return_pct
            FROM stock_prices
        )
        SELECT ticker, MIN(return_pct) as worst_day_pct
        FROM daily_returns
        GROUP BY ticker
        ORDER BY worst_day_pct ASC
    """))

    print("\n--- Year over Year Average Close ---")
    print(run_query("""
        SELECT 
            ticker,
            STRFTIME('%Y', date) as year,
            ROUND(AVG(close), 2) as avg_close
        FROM stock_prices
        GROUP BY ticker, year
        ORDER BY ticker, year
    """))

if __name__ == "__main__":
    analyze_stocks()