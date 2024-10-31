import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Set up Streamlit page configuration
st.set_page_config(layout="wide", page_title="Cryptocurrency and Stock Comparison Tool")

# Sidebar inputs for user selection
st.sidebar.title("Comparison Tool")
stock_symbol = st.sidebar.text_input("Enter stock ticker symbol (e.g., AAPL):", "AAPL").upper()
crypto_symbol = st.sidebar.text_input("Enter cryptocurrency symbol (e.g., BTC-USD):", "BTC-USD").upper()
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch stock data
st.title("📊 Cryptocurrency and Stock Comparison Tool")
st.write(f"Comparing **{stock_symbol}** (Stock) with **{crypto_symbol}** (Cryptocurrency)")

try:
    # Fetch stock data
    stock = yf.Ticker(stock_symbol)
    stock_data = stock.history(start=start_date, end=end_date)

    # Fetch cryptocurrency data
    crypto = yf.Ticker(crypto_symbol)
    crypto_data = crypto.history(start=start_date, end=end_date)

    # Check if data is retrieved
    if not stock_data.empty and not crypto_data.empty:
        # Rename columns for clarity
        stock_data = stock_data[['Close']].rename(columns={"Close": f"{stock_symbol} Close"})
        crypto_data = crypto_data[['Close']].rename(columns={"Close": f"{crypto_symbol} Close"})

        # Merge stock and crypto data on date
        combined_data = stock_data.join(crypto_data, how='inner')

        # Display combined data
        st.subheader("Historical Price Comparison")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=combined_data.index, y=combined_data[f"{stock_symbol} Close"], mode='lines', name=f"{stock_symbol} (Stock)"))
        fig.add_trace(go.Scatter(x=combined_data.index, y=combined_data[f"{crypto_symbol} Close"], mode='lines', name=f"{crypto_symbol} (Crypto)"))
        fig.update_layout(
            title="Stock vs Cryptocurrency Historical Price Comparison",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Calculate and display percentage returns
        stock_return = ((combined_data[f"{stock_symbol} Close"].iloc[-1] - combined_data[f"{stock_symbol} Close"].iloc[0]) / combined_data[f"{stock_symbol} Close"].iloc[0]) * 100
        crypto_return = ((combined_data[f"{crypto_symbol} Close"].iloc[-1] - combined_data[f"{crypto_symbol} Close"].iloc[0]) / combined_data[f"{crypto_symbol} Close"].iloc[0]) * 100

        st.subheader("Performance Comparison")
        col1, col2 = st.columns(2)
        col1.metric(f"{stock_symbol} Stock Return", f"{stock_return:.2f}%")
        col2.metric(f"{crypto_symbol} Crypto Return", f"{crypto_return:.2f}%")

        # Technical Indicators - Moving Averages
        st.subheader("Technical Indicators")
        combined_data[f"{stock_symbol} SMA_50"] = combined_data[f"{stock_symbol} Close"].rolling(window=50).mean()
        combined_data[f"{crypto_symbol} SMA_50"] = combined_data[f"{crypto_symbol} Close"].rolling(window=50).mean()

        fig_ma = go.Figure()
        fig_ma.add_trace(go.Scatter(x=combined_data.index, y=combined_data[f"{stock_symbol} Close"], mode="lines", name=f"{stock_symbol} Close"))
        fig_ma.add_trace(go.Scatter(x=combined_data.index, y=combined_data[f"{crypto_symbol} Close"], mode="lines", name=f"{crypto_symbol} Close"))
        fig_ma.add_trace(go.Scatter(x=combined_data.index, y=combined_data[f"{stock_symbol} SMA_50"], mode="lines", name=f"{stock_symbol} 50-Day SMA"))
        fig_ma.add_trace(go.Scatter(x=combined_data.index, y=combined_data[f"{crypto_symbol} SMA_50"], mode="lines", name=f"{crypto_symbol} 50-Day SMA"))

        fig_ma.update_layout(
            title="50-Day Moving Average Comparison",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig_ma, use_container_width=True)

        # Display combined data table
        st.subheader("Combined Historical Data Table")
        st.dataframe(combined_data)

    else:
        st.error("Could not retrieve data for the stock or cryptocurrency symbols provided.")

except Exception as e:
    st.error(f"An error occurred: {e}")
