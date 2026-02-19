import yfinance as yf
import pandas as pd

def calculate_rvol(ticker_symbol, window=20):
    # 1. Stock ka data fetch karein (last 30 days takka)
    stock = yf.Ticker(ticker_symbol)
    df = stock.history(period="1mo")
    
    if len(df) < window:
        return "Not enough data"

    # 2. Pichle 'window' dino ka average volume nikalein (excluding today)
    avg_volume = df['Volume'].iloc[-window-1:-1].mean()
    
    # 3. Aaj ka current (live) volume lein
    current_volume = df['Volume'].iloc[-1]
    
    # 4. RVOL Calculate karein
    rvol = current_volume / avg_volume
    
    return round(rvol, 2)

# Example use for ITC
itc_rvol = calculate_rvol("ITC.NS")
print(f"ITC current RVOL: {itc_rvol}")
