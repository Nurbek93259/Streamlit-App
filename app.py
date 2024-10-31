import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Set up Streamlit page configuration
st.set_page_config(layout="wide", page_title="Stock Price Prediction App")

# Sidebar inputs
st.sidebar.title("Stock Price Prediction")
symbol = st.sidebar.text_input("Enter stock symbol (e.g., AAPL):", "AAPL").upper()
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=365 * 5))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch stock data
st.title(f"📈 Stock Price Prediction for {symbol}")
stock = yf.Ticker(symbol)
data = stock.history(start=start_date, end=end_date)

if not data.empty:
    # Display Candlestick Chart
    st.subheader("Historical Price with Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    )])
    fig.update_layout(
        title=f"{symbol} Price Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Prepare data for prediction model
    data['Date'] = data.index
    data['Date_ordinal'] = data['Date'].map(datetime.toordinal)  # Convert dates to ordinal numbers

    # Define features and target
    X = data[['Date_ordinal']]
    y = data['Close']

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    # Create DataFrame with test data and predictions
    predictions = pd.DataFrame({'Date': X_test['Date_ordinal'], 'Actual': y_test, 'Predicted': y_pred})
    predictions['Date'] = predictions['Date'].map(datetime.fromordinal)
    predictions = predictions.sort_values(by="Date")

    # Display Prediction Results
    st.subheader("Model Prediction vs Actual")
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=predictions['Date'], y=predictions['Actual'], mode="lines", name="Actual Price"))
    fig_pred.add_trace(go.Scatter(x=predictions['Date'], y=predictions['Predicted'], mode="lines", name="Predicted Price"))
    fig_pred.update_layout(
        title=f"{symbol} Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig_pred, use_container_width=True)

    # Future Predictions
    st.subheader("Future Price Prediction")
    days_ahead = st.slider("Days ahead to predict:", min_value=1, max_value=365, value=30)
    future_dates = pd.date_range(end_date + timedelta(days=1), periods=days_ahead).to_list()
    future_ordinals = [[date.toordinal()] for date in future_dates]
    future_predictions = model.predict(future_ordinals)

    # Display Future Prediction Results
    future_df = pd.DataFrame({"Date": future_dates, "Predicted Price": future_predictions})
    fig_future = go.Figure()
    fig_future.add_trace(go.Scatter(x=future_df['Date'], y=future_df['Predicted Price'], mode="lines", name="Predicted Future Price"))
    fig_future.update_layout(
        title=f"Predicted Future Prices for {symbol}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig_future, use_container_width=True)

    # Display future prediction data
    st.dataframe(future_df)

else:
    st.error("No data found for the specified stock symbol and date range.")
