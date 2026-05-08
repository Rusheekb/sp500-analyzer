import json
import os

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), "portfolio.json")

def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return {}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)

def add_position(ticker, shares, avg_cost):
    portfolio = load_portfolio()
    portfolio[ticker.upper()] = {
        "shares": float(shares),
        "avg_cost": float(avg_cost),
        "invested": round(float(shares) * float(avg_cost), 2)
    }
    save_portfolio(portfolio)
    return portfolio

def remove_position(ticker):
    portfolio = load_portfolio()
    if ticker.upper() in portfolio:
        del portfolio[ticker.upper()]
        save_portfolio(portfolio)
    return portfolio

def get_portfolio_value(portfolio, current_prices):
    """
    Calculate current value, profit/loss for each position.
    current_prices: dict of {ticker: current_price}
    """
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