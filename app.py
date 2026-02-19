import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 1. Fibonacci Levels Logic ---
def get_fibonacci_levels(high, low):
    diff = high - low
    levels = {
        "0.0% (Low)": low,
        "23.6%": high - 0.236 * diff,
        "38.2%": high - 0.382 * diff,
        "50.0% (Pivot)": high - 0.5 * diff,
        "61.8% (Golden)": high - 0.618 * diff,
        "78.6%": high - 0.786 * diff,
        "100% (High)": high
    }
    return levels

# --- 2. RVOL Calculation Logic ---
def get_rvol(ticker):
    data = yf.download(ticker, period="5d", interval="15m")
    if data.empty: return 0
    
    # Last 15-min volume vs Average of last 100 candles (approx 2-3 days)
    current_vol = data['Volume'].iloc[-1]
    avg_vol = data['Volume'].tail(100).mean()
    rvol = current_vol / avg_vol
    return round(rvol, 2)

# --- 3. Square (Gann) Simple Logic ---
def get_square_levels(price):
    # Gann Square of 9 simplified: (sqrt(price) + factor)^2
    root = np.sqrt(price)
    targets = {
        "Next Resistance": (root + 0.125)**2, # 45 degrees
        "Strong Resistance": (root + 0.25)**2, # 90 degrees
        "Next Support": (root - 0.125)**2,
        "Strong Support": (root - 0.25)**2
    }
    return targets

# --- Streamlit UI ---
st.set_page_config(page_title="Dhaval's Trading Tool", layout="wide")
st.title("📈 Advanced Stock Scanner (Fibonacci | Square | RVOL)")

symbol = st.sidebar.text_input("Enter Ticker (e.g., ITC.NS, RELIANCE.NS)", "ITC.NS")

if st.sidebar.button("Analyze"):
    # Data Fetching
    stock_data = yf.download(symbol, period="2d", interval="15m")
    
    if not stock_data.empty:
        curr_price = stock_data['Close'].iloc[-1]
        high_price = stock_data['High'].max()
        low_price = stock_data['Low'].min()
        
        # 1. RVOL Metric
        rvol_val = get_rvol(symbol)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"₹{curr_price:.2f}")
        
        # Color coding for RVOL
        if rvol_val > 1.5:
            col2.metric("RVOL (Momentum)", rvol_val, delta="High Activity", delta_color="normal")
        else:
            col2.metric("RVOL (Momentum)", rvol_val, delta="Low Activity", delta_color="inverse")
            
        col3.write(f"**Day High:** ₹{high_price:.2f}  \n**Day Low:** ₹{low_price:.2f}")

        st.divider()

        # 2. Fibonacci Section
        st.subheader("🎯 Fibonacci Retracement Levels")
        fib_levels = get_fibonacci_levels(high_price, low_price)
        st.table(pd.DataFrame(fib_levels.items(), columns=["Level", "Price"]))

        # 3. Square (Gann) Section
        st.subheader("🔳 Square of 9 Levels (Intrinsic)")
        square_levels = get_square_levels(curr_price)
        st.json(square_levels)

    else:
        st.error("Data fetch nahi ho raha hai. Please check the ticker symbol (e.g., Use .NS for Nifty).")

