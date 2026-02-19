import streamlit as st
import math
import yfinance as yf
from fpdf import FPDF

# --- PDF GENERATOR FUNCTION ---
def create_pdf(data, high, low, title="Fibonacci Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Reference High: {high}", ln=True)
    pdf.cell(200, 10, txt=f"Reference Low: {low}", ln=True)
    pdf.ln(5)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(95, 10, "Level (%)", border=1, fill=True)
    pdf.cell(95, 10, "Price / Value", border=1, ln=True, fill=True)
    
    for item in data:
        pdf.cell(95, 10, str(item["Level"]), border=1)
        pdf.cell(95, 10, str(item["Value"]), border=1, ln=True)
        
    return pdf.output(dest='S').encode('latin-1')

# --- APP LAYOUT ---
st.set_page_config(page_title="Pro Math & Finance Hub", layout="wide")
st.sidebar.title("Navigation")
tool = st.sidebar.radio("Go to:", ["Live Nifty & Fibonacci", "Square Root & Math"])

# --- TOOL 1: LIVE NIFTY & FIBONACCI ---
if tool == "Live Nifty & Fibonacci":
    st.header("📈 Live Nifty 50 & Fibonacci Levels")
    
    # Fetch Live Nifty Data
    with st.spinner("Fetching live market data..."):
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="1d")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            st.metric("NIFTY 50 Current Price", f"₹{current_price:,.2f}")
        else:
            st.error("Could not fetch live price. Check your internet connection.")
            current_price = 0

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        high_p = st.number_input("Enter High Price", value=float(current_price))
    with col2:
        low_p = st.number_input("Enter Low Price", value=float(current_price * 0.95))

    if st.button("Calculate & Generate Report"):
        diff = high_p - low_p
        ratios = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        results = []
        
        for r in ratios:
            val = high_p - (diff * r)
            results.append({"Level": f"{r*100:.1f}%", "Value": round(val, 2)})
        
        st.table(results)

        # PDF Download Section
        pdf_data = create_pdf(results, high_p, low_p, "Nifty Fibonacci Analysis")
        st.download_button(
            label="📥 Download Fibonacci PDF",
            data=pdf_data,
            file_name="nifty_fib_report.pdf",
            mime="application/pdf"
        )

# --- TOOL 2: SQUARE ROOT & MATH ---
elif tool == "Square Root & Math":
    st.header("🧮 Advanced Math Tool")
    
    num = st.number_input("Enter number for Square & Root", value=1.0)
    
    if st.button("Calculate Math"):
        sq = num ** 2
        root = "N/A (Negative)" if num < 0 else round(math.sqrt(num), 4)
        
        c1, c2 = st.columns(2)
        c1.metric("Square", sq)
        c2.metric("Square Root", root)
        
        # Simple PDF for Math results
        math_results = [
            {"Level": "Square", "Value": sq},
            {"Level": "Square Root", "Value": root}
        ]
        pdf_math = create_pdf(math_results, num, "N/A", "Math Results Report")
        st.download_button("📥 Download Math PDF", pdf_math, "math_report.pdf", "application/pdf")
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
