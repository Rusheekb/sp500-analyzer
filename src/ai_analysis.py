from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_portfolio_analysis(portfolio_data: list) -> str:
    """
    Generate personalized AI portfolio analysis using actual cost basis and P&L.
    """

    # --- Build rich context ---
    total_invested = sum(p.get("invested", 0) for p in portfolio_data)
    total_value = sum(p.get("current_value", p.get("end", 0)) for p in portfolio_data)
    total_pl = total_value - total_invested if total_invested > 0 else 0
    total_pl_pct = (total_pl / total_invested * 100) if total_invested > 0 else 0

    best = max(portfolio_data, key=lambda x: x.get("change_pct", 0))
    worst = min(portfolio_data, key=lambda x: x.get("change_pct", 0))

    # Build per-position breakdown
    positions_detail = ""
    for p in sorted(portfolio_data, key=lambda x: x.get("current_value", 0), reverse=True):
        ticker = p["ticker"]
        change_pct = p.get("change_pct", 0)
        pl_dollars = p.get("profit_loss", 0)
        invested = p.get("invested", 0)
        current_value = p.get("current_value", p.get("end", 0))
        shares = p.get("shares", "N/A")
        avg_cost = p.get("avg_cost", "N/A")
        current_price = p.get("current_price", p.get("end", "N/A"))
        weight = (current_value / total_value * 100) if total_value > 0 else 0

        positions_detail += f"""
        {ticker}:
        - Portfolio weight: {weight:.1f}%
        - Shares: {shares}
        - Avg cost: ${avg_cost}
        - Current price: ${current_price}
        - Amount invested: ${invested:,.2f}
        - Current value: ${current_value:,.2f}
        - P&L: ${pl_dollars:,.2f} ({change_pct:+.2f}%)
        """

    prompt = f"""You are a knowledgeable personal finance analyst reviewing someone's actual investment portfolio. 
You have access to their real position data including what they paid, what it's worth now, and their actual profit/loss.

PORTFOLIO OVERVIEW:
- Total invested: ${total_invested:,.2f}
- Current value: ${total_value:,.2f}
- Total P&L: ${total_pl:,.2f} ({total_pl_pct:+.2f}%)
- Number of positions: {len(portfolio_data)}
- Best performer: {best['ticker']} ({best.get('change_pct', 0):+.2f}%)
- Worst performer: {worst['ticker']} ({worst.get('change_pct', 0):+.2f}%)

POSITION DETAILS:
{positions_detail}

Based on this REAL data, provide a personalized analysis with:

1. **Portfolio Health** (2-3 sentences): Overall assessment using their actual dollar P&L and percentage returns. Be specific — mention actual numbers.

2. **Position Highlights** (1 sentence per position): Reference their actual cost basis and current price. For example: "You bought NVDA at $149 and it's now at $217 — a $3,737 gain on your position."

3. **Concentration & Risk**: Identify any positions that make up more than 20% of the portfolio and comment on concentration risk.

4. **One Actionable Insight**: Based on the actual data — not generic advice. For example, if one stock is down significantly from cost basis, acknowledge it specifically.

Be conversational but analytical. Use their actual numbers throughout. Do not give buy/sell advice. 
Do not use generic phrases like "it's important to diversify" without tying it to their specific portfolio."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.7
    )

    return response.choices[0].message.content