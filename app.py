import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
import requests
import plotly.graph_objs as go

# Set page configuration
st.set_page_config(layout="wide", page_title="Enhanced Stock & Market Data App")

# Sidebar for user inputs
st.sidebar.title("Data Explorer")

# Input: Ticker symbol and date range
symbol = st.sidebar.text_input("Enter stock symbol:", "AAPL").upper()
start_date = st.sidebar.date_input("Start Date", datetime.date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Display options for different stock data and indicators
st.sidebar.subheader("Stock Data to Display")
show_volume = st.sidebar.checkbox("Show Volume")
show_moving_average = st.sidebar.checkbox("Show Moving Averages (SMA & EMA)")
show_rsi = st.sidebar.checkbox("Show RSI (Relative Strength Index)")

# Section for additional features
st.sidebar.subheader("Additional Features")
show_weather = st.sidebar.checkbox("Show Weather Info")
show_currency = st.sidebar.checkbox("Show JPY-USD Exchange Rate")

# Ticker data fetch
stock = yf.Ticker(symbol)

# Display stock information
st.title(f"Stock Data for {symbol}")

try:
    # Display Company Information
    info = stock.info
    col1, col2, col3 = st.columns(3)
    col1.metric("Sector", info.get("sector", "N/A"))
    col2.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
    col3.metric("52-Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
    col1.metric("52-Week Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
    col2.metric("Dividend Yield", f"{info.get('dividendYield', 'N/A'):.2%}")
    col3.metric("Beta", info.get("beta", "N/A"))

    # Fetch historical data
    data = stock.history(start=start_date, end=end_date)

    # Plot stock price and volume
    fig = go.Figure()

    # Line for Close Price
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode="lines", name="Close Price"))

    # Plot volume as a separate bar chart if selected
    if show_volume:
        fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume", yaxis="y2"))
        fig.update_layout(
            yaxis2=dict(
                title="Volume",
                overlaying="y",
                side="right",
                showgrid=False,
            )
        )

    # Add moving averages if selected
    if show_moving_average:
        data["SMA_50"] = data["Close"].rolling(window=50).mean()
        data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
        fig.add_trace(go.Scatter(x=data.index, y=data["SMA_50"], mode="lines", name="50-Day SMA"))
        fig.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], mode="lines", name="20-Day EMA"))

    # Add RSI indicator if selected
    if show_rsi:
        delta = data["Close"].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        data["RSI"] = rsi
        fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI"))
        fig.update_yaxes(range=[0, 100], secondary_y=True)

    # Final layout adjustments
    fig.update_layout(
        title=f"Stock Price Data for {symbol}",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        template="plotly_white",
    )

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

    # Display data table
    st.subheader("Historical Data")
    st.dataframe(data)

    # Download data as CSV
    st.download_button(
        label="Download Data as CSV",
        data=data.to_csv().encode("utf-8"),
        file_name=f"{symbol}_data.csv",
        mime="text/csv",
    )

except Exception as e:
    st.error(f"An error occurred while fetching stock data: {e}")

# Show weather information if selected
if show_weather:
    st.header("Weather Information")
    location = st.sidebar.text_input("Enter City Name", "New York")
    weather_api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your OpenWeatherMap API key

    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        weather_data = requests.get(weather_url).json()
        
        if weather_data.get("cod") != 200:
            st.error(f"Error fetching weather data: {weather_data.get('message')}")
        else:
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            weather = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]

            col1, col2 = st.columns(2)
            col1.metric("Temperature", f"{temp} °C")
            col2.metric("Feels Like", f"{feels_like} °C")
            col1.metric("Weather", weather.capitalize())
            col2.metric("Humidity", f"{humidity}%")
    except Exception as e:
        st.error(f"An error occurred while fetching weather data: {e}")

# Show JPY-USD exchange rate if selected
if show_currency:
    st.header("JPY-USD Exchange Rate")
    currency_api_key = "YOUR_EXCHANGERATE_API_KEY"  # Replace with your ExchangeRate API key

    try:
        currency_url = f"https://v6.exchangerate-api.com/v6/{currency_api_key}/pair/JPY/USD"
        currency_data = requests.get(currency_url).json()

        if currency_data.get("result") != "success":
            st.error("Error fetching exchange rate data.")
        else:
            exchange_rate = currency_data["conversion_rate"]
            st.metric("JPY to USD", f"{exchange_rate} USD")
    except Exception as e:
        st.error(f"An error occurred while fetching currency data: {e}")
