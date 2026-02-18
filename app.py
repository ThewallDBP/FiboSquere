import streamlit as st
import math

# App Title & Styling
st.set_page_config(page_title="Maths & Finance Tool", page_icon="📈")
st.title("🧮 Logic & Level Calculator")

# Sidebar for Navigation
option = st.sidebar.selectbox(
    'Select a Tool',
    ('Square & Square Root', 'Fibonacci Retracement')
)

if option == 'Square & Square Root':
    st.header("Basic Math Calculator")
    number = st.number_input("Enter a number:", value=0.0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Square", number ** 2)
        
    with col2:
        if number >= 0:
            st.metric("Square Root", round(math.sqrt(number), 4))
        else:
            st.error("Cannot calculate square root of a negative number.")

elif option == 'Fibonacci Retracement':
    st.header("Fibonacci Retracement Levels")
    st.write("Used to identify potential support and resistance levels.")
    
    # Input for High and Low prices
    high_price = st.number_input("Recent High Price", value=100.0)
    low_price = st.number_input("Recent Low Price", value=50.0)
    
    if high_price <= low_price:
        st.warning("High price should be greater than low price for retracement calculation.")
    else:
        diff = high_price - low_price
        ratios = [0.0, 0.236, 0.382, 0.5, 0.618, 0.7]
        import streamlit as st
import math
from fpdf import FPDF

# Function to create PDF
def create_pdf(data, high, low):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Fibonacci Retracement Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"High Price: {high}", ln=True)
    pdf.cell(200, 10, txt=f"Low Price: {low}", ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(95, 10, "Fibonacci Level (%)", border=1, fill=True)
    pdf.cell(95, 10, "Price", border=1, ln=True, fill=True)
    
    # Table Body
    for item in data:
        pdf.cell(95, 10, item["Level (%)"], border=1)
        pdf.cell(95, 10, item["Price"], border=1, ln=True)
        
    return pdf.output(dest='S').encode('latin-1')

# --- Existing App Logic ---
# (Inside your Fibonacci 'if' block)

if option == 'Fibonacci Retracement':
    st.header("Fibonacci Retracement Levels")
    high_price = st.number_input("Recent High Price", value=100.0)
    low_price = st.number_input("Recent Low Price", value=50.0)
    
    if st.button('Calculate Retracements'):
        if high_price <= low_price:
            st.warning("High price must be greater than low price.")
        else:
            diff = high_price - low_price
            ratios = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
            
            results = []
            for ratio in ratios:
                level_price = high_price - (diff * ratio)
                results.append({"Level (%)": f"{ratio*100:.1f}%", "Price": f"{level_price:.2f}"})
            
            st.table(results)
            
            # Generate PDF
            pdf_bytes = create_pdf(results, high_price, low_price)
            
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_bytes,
                file_name="fibonacci_report.pdf",
                mime="application/pdf"
            )
