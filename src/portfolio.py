import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def load_portfolio(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT ticker, shares, avg_cost, invested
            FROM portfolio WHERE user_id = :user_id
        """), {"user_id": user_id})
        rows = result.fetchall()
    return {
        row[0]: {
            "shares": row[1],
            "avg_cost": row[2],
            "invested": row[3]
        }
        for row in rows
    }

def add_position(ticker, shares, avg_cost, user_id):
    invested = round(float(shares) * float(avg_cost), 2)
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO portfolio (ticker, shares, avg_cost, invested, user_id)
            VALUES (:ticker, :shares, :avg_cost, :invested, :user_id)
            ON CONFLICT (ticker, user_id) DO UPDATE SET
                shares = :shares,
                avg_cost = :avg_cost,
                invested = :invested
        """), {
            "ticker": ticker.upper(),
            "shares": float(shares),
            "avg_cost": float(avg_cost),
            "invested": invested,
            "user_id": user_id
        })
        conn.commit()
    return load_portfolio(user_id)

def remove_position(ticker, user_id):
    with engine.connect() as conn:
        conn.execute(text("""
            DELETE FROM portfolio
            WHERE ticker = :ticker AND user_id = :user_id
        """), {"ticker": ticker.upper(), "user_id": user_id})
        conn.commit()
    return load_portfolio(user_id)

def get_portfolio_value(portfolio, current_prices):
    results = []
    total_invested = 0
    total_value = 0

    for ticker, position in portfolio.items():
        current_price = current_prices.get(ticker, 0)
        current_value = position["shares"] * current_price
        profit_loss = current_value - position["invested"]
        profit_loss_pct = (profit_loss / position["invested"]) * 100 if position["invested"] > 0 else 0

        results.append({
            "ticker": ticker,
            "shares": position["shares"],
            "avg_cost": position["avg_cost"],
            "invested": position["invested"],
            "current_price": round(current_price, 2),
            "current_value": round(current_value, 2),
            "profit_loss": round(profit_loss, 2),
            "profit_loss_pct": round(profit_loss_pct, 2)
        })

        total_invested += position["invested"]
        total_value += current_value

    return {
        "positions": results,
        "total_invested": round(total_invested, 2),
        "total_value": round(total_value, 2),
        "total_profit_loss": round(total_value - total_invested, 2),
        "total_profit_loss_pct": round(((total_value - total_invested) / total_invested) * 100, 2) if total_invested > 0 else 0
    }