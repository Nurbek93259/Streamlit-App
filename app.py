import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import plotly.graph_objs as go
from datetime import datetime

# Set up page configuration
st.set_page_config(layout="wide", page_title="Economic Indicator Dashboard")

# Sidebar inputs for currency and stock index selection
st.sidebar.title("Dashboard Options")
currency_pair = st.sidebar.selectbox("Select Currency Pair", ["JPY-USD", "EUR-USD", "GBP-USD"])
index_selection = st.sidebar.multiselect(
    "Select Stock Indices", ["S&P 500", "NASDAQ", "DOW JONES"],
    ["S&P 500", "NASDAQ"]
)

# Define stock indices tickers (Yahoo Finance tickers)
index_tickers = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI"
}

# API keys
currency_api_key = "YOUR_EXCHANGERATE_API_KEY"  # Exchange Rate API key for currency data
# Placeholder example economic data
sample_economic_data = {
    "GDP Growth (%)": 3.2,
    "Inflation Rate (%)": 2.1,
    "Unemployment Rate (%)": 5.2,
    "Interest Rate (%)": 1.5
}

# Title for the dashboard
st.title("📈 Economic Indicator Dashboard")

# Fetch and display stock index data
st.header("📊 Stock Indices")
index_data = {}
for index in index_selection:
    ticker_symbol = index_tickers[index]
    stock_data = yf.Ticker(ticker_symbol).history(period="1y")
    index_data[index] = stock_data

    # Plot index data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode="lines", name=index))
    fig.update_layout(
        title=f"{index} - Last Year Performance",
        xaxis_title="Date",
        yaxis_title="Index Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# Fetch and display currency exchange rate data
st.header("💱 Currency Exchange Rate")
try:
    currency_url = f"https://v6.exchangerate-api.com/v6/{currency_api_key}/pair/{currency_pair.split('-')[0]}/{currency_pair.split('-')[1]}"
    currency_data = requests.get(currency_url).json()
    
    if currency_data.get("result") == "success":
        conversion_rate = currency_data["conversion_rate"]
        st.metric(f"Exchange Rate {currency_pair}", f"{conversion_rate} {currency_pair.split('-')[1]}")
    else:
        st.error("Failed to fetch currency data.")
except Exception as e:
    st.error(f"An error occurred while fetching currency data: {e}")

# Display Economic Indicators
st.header("📉 Economic Indicators")
st.write("Real-time indicators for economic health:")
col1, col2, col3, col4 = st.columns(4)
col1.metric("GDP Growth (%)", f"{sample_economic_data['GDP Growth (%)']}%")
col2.metric("Inflation Rate (%)", f"{sample_economic_data['Inflation Rate (%)']}%")
col3.metric("Unemployment Rate (%)", f"{sample_economic_data['Unemployment Rate (%)']}%")
col4.metric("Interest Rate (%)", f"{sample_economic_data['Interest Rate (%)']}%")

# Additional options for economic indicator trend plotting
st.header("📅 Economic Indicator Trends")
show_trend = st.checkbox("Show Trends for Economic Indicators (Simulated Data)")

if show_trend:
    # Simulated data for trend visualization
    date_range = pd.date_range(start="2023-01-01", end=datetime.today(), freq="M")
    gdp_growth = [3.2 + (0.1 * i) for i in range(len(date_range))]
    inflation_rate = [2.1 + (0.05 * i) for i in range(len(date_range))]
    unemployment_rate = [5.2 - (0.02 * i) for i in range(len(date_range))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_range, y=gdp_growth, mode="lines+markers", name="GDP Growth (%)"))
    fig.add_trace(go.Scatter(x=date_range, y=inflation_rate, mode="lines+markers", name="Inflation Rate (%)"))
    fig.add_trace(go.Scatter(x=date_range, y=unemployment_rate, mode="lines+markers", name="Unemployment Rate (%)"))
    
    fig.update_layout(
        title="Trends for Simulated Economic Indicators",
        xaxis_title="Date",
        yaxis_title="Percentage (%)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
