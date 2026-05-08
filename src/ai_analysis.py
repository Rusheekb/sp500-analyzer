from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_portfolio_analysis(portfolio_data: list) -> str:
    portfolio_summary = "\n".join([
        f"- {row['ticker']}: ${row['start']:.2f} → ${row['end']:.2f} ({row['change_pct']:+.2f}%)"
        for row in portfolio_data
    ])

    total_avg = sum(row['change_pct'] for row in portfolio_data) / len(portfolio_data)
    best = max(portfolio_data, key=lambda x: x['change_pct'])
    worst = min(portfolio_data, key=lambda x: x['change_pct'])

    prompt = f"""You are a financial analyst assistant. A user is tracking the following stocks over the past month:

{portfolio_summary}

Portfolio average return: {total_avg:+.2f}%
Best performer: {best['ticker']} at {best['change_pct']:+.2f}%
Worst performer: {worst['ticker']} at {worst['change_pct']:+.2f}%

Please provide:
1. A 2-3 sentence overall portfolio summary
2. A brief note on each stock (1 sentence each)
3. One actionable observation the investor should consider

Keep the tone professional but conversational. Do not give specific buy/sell advice. Focus on performance patterns and context."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    return response.choices[0].message.content