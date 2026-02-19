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
    # 'group_by' ticker use karne se data clean milta hai
    data = yf.download(ticker, period="5d", interval="15m", progress=False)
    if data.empty: return 0
    
    current_vol = float(data['Volume'].iloc[-1])
    avg_vol = float(data['Volume'].tail(100).mean())
    return round(current_vol / avg_vol, 2) if avg_vol > 0 else 0

# --- 3. Square (Gann) Simple Logic ---
def get_square_levels(price):
    root = np.sqrt(float(price))
    targets = {
        "Next Resistance (45°)": (root + 0.125)**2,
        "Strong Resistance (90°)": (root + 0.25)**2,
        "Next Support (45°)": (root - 0.125)**2,
        "Strong Support (90°)": (root - 0.25)**2
    }
    return targets

# --- Streamlit UI ---
st.set_page_config(page_title="Dhaval's Trading Tool", layout="wide")
st.title("📈 Advanced Stock Scanner")

# Sidebar input
symbol = st.sidebar.text_input("Enter Ticker (e.g., ITC.NS)", "ITC.NS")

if st.sidebar.button("Analyze"):
    # Data Fetching
    stock_data = yf.download(symbol, period="2d", interval="15m", progress=False)
    
    if not stock_data.empty:
        # FIX: .iloc[-1].item() use kiya hai taaki sirf single value mile
        try:
            curr_price = float(stock_data['Close'].iloc[-1])
            high_price = float(stock_data['High'].max())
            low_price = float(stock_data['Low'].min())
            
            rvol_val = get_rvol(symbol)
            
            # Metrics Display
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"₹{curr_price:.2f}")
            
            if rvol_val > 1.5:
                col2.metric("RVOL (Momentum)", rvol_val, delta="High Activity")
            else:
                col2.metric("RVOL (Momentum)", rvol_val, delta="Low Activity", delta_color="inverse")
                
            col3.metric("Day High", f"₹{high_price:.2f}")

            st.divider()

            # 2. Fibonacci Table
            st.subheader("🎯 Fibonacci Retracement Levels")
            fib_levels = get_fibonacci_levels(high_price, low_price)
            fib_df = pd.DataFrame(fib_levels.items(), columns=["Level", "Price"])
            st.table(fib_df)

            # 3. Square (Gann) Section
            st.subheader("🔳 Square of 9 Levels")
            square_levels = get_square_levels(curr_price)
            
            # Better display for Square levels
            sq_col1, sq_col2 = st.columns(2)
            sq_col1.write("**Resistances:**")
            sq_col1.write(f"R1: {square_levels['Next Resistance (45°)']:.2f}")
            sq_col1.write(f"R2: {square_levels['Strong Resistance (90°)']:.2f}")
            
            sq_col2.write("**Supports:**")
            sq_col2.write(f"S1: {square_levels['Next Support (45°)']:.2f}")
            sq_col2.write(f"S2: {square_levels['Strong Support (90°)']:.2f}")

        except Exception as e:
            st.error(f"Error processing data: {e}")
    else:
        st.error("Ticker symbol galat hai ya data nahi mil raha.")
