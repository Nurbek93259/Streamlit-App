import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.graph_objs as go
from datetime import datetime

# Set up the Streamlit page configuration
st.set_page_config(layout="wide", page_title="Financial News & Stock Analysis Platform")

# Sidebar inputs
st.sidebar.title("Search for a Stock")
symbol = st.sidebar.text_input("Enter stock symbol (e.g., AAPL):", "AAPL").upper()

# Define the date range for historical data
start_date = st.sidebar.date_input("Start Date", datetime(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())

# API key for news data
news_api_key = "YOUR_NEWS_API_KEY"  # Replace with your actual NewsAPI key

# Fetch stock data
st.title(f"📈 Financial Analysis for {symbol}")
stock = yf.Ticker(symbol)

try:
    # Display company information
    info = stock.info
    col1, col2, col3 = st.columns(3)
    col1.metric("Sector", info.get("sector", "N/A"))
    col2.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
    col3.metric("52-Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
    col1.metric("52-Week Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
    col2.metric("Dividend Yield", f"{info.get('dividendYield', 'N/A'):.2%}")
    col3.metric("Beta", info.get("beta", "N/A"))

    # Fetch historical data for the selected date range
    data = stock.history(start=start_date, end=end_date)

    # Plot historical price data
    st.subheader("Stock Price History")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode="lines", name="Close Price"))
    fig.update_layout(
        title=f"{symbol} Stock Price",
        xaxis_title="Date",
        yaxis_title="Close Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Display technical indicators (Moving Averages)
    st.subheader("Technical Indicators")
    data["SMA_50"] = data["Close"].rolling(window=50).mean()  # 50-day Simple Moving Average
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()  # 20-day Exponential Moving Average
    
    fig_indicators = go.Figure()
    fig_indicators.add_trace(go.Scatter(x=data.index, y=data['Close'], mode="lines", name="Close Price"))
    fig_indicators.add_trace(go.Scatter(x=data.index, y=data["SMA_50"], mode="lines", name="50-Day SMA"))
    fig_indicators.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], mode="lines", name="20-Day EMA"))
    fig_indicators.update_layout(
        title=f"{symbol} with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig_indicators, use_container_width=True)

    # Show historical data as a table
    st.subheader("Historical Data")
    st.dataframe(data[['Open', 'High', 'Low', 'Close', 'Volume']])

except Exception as e:
    st.error(f"An error occurred while fetching stock data: {e}")

# Fetch financial news articles
st.header("📰 Latest Financial News")

try:
    news_url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={news_api_key}&sortBy=publishedAt"
    response = requests.get(news_url)
    news_data = response.json()

    if news_data["status"] == "ok":
        articles = news_data["articles"][:5]  # Display top 5 articles
        for article in articles:
            st.subheader(article["title"])
            st.write(article["description"])
            st.markdown(f"[Read more]({article['url']})")
            st.write("---")
    else:
        st.error("Failed to fetch news articles.")

except Exception as e:
    st.error(f"An error occurred while fetching news: {e}")
