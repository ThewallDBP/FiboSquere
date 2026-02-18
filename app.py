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
