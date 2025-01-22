import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime

# Set the title of the Streamlit app
st.title("Effect of Rising Inflation on Stock Market Sectors")

# Inflation data
inflation_data = {
    'Date': ['Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'May-23', 'Jun-23', 'Jul-23', 'Aug-23', 'Sep-23', 'Oct-23', 'Nov-23', 'Dec-23',
             'Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24', 'Nov-24'],
    'Inflation': [5.72, 6.52, 6.44, 5.66, 4.70, 4.25, 4.81, 7.44, 6.83, 5.02, 4.87, 5.55, 5.69, 5.10, 5.09, 4.85, 4.83, 4.75, 5.08, 3.54, 3.65, 3.65, 3.44]
}
inflation_df = pd.DataFrame(inflation_data)
inflation_df['Date'] = pd.to_datetime(inflation_df['Date'], format='%b-%y')
inflation_df.set_index('Date', inplace=True)

# Download stock data
tickers = ['^CNXIT', '^NSEI']
stock_data = yf.download(tickers, start='2023-01-01', end='2024-11-30', interval='1mo')

# Check if 'Adj Close' column exists
if 'Adj Close' in stock_data.columns.levels[0]:
    stock_data = stock_data['Adj Close']
else:
    st.error("Adjusted Close prices not found in the downloaded data.")
    st.stop()

# Merge inflation data with stock data
merged_df = inflation_df.join(stock_data)

# Calculate percentage changes
merged_df['Inflation_Change'] = merged_df['Inflation'].pct_change()
merged_df['CNXIT_Change'] = merged_df['^CNXIT'].pct_change()
merged_df['NSEI_Change'] = merged_df['^NSEI'].pct_change()

# Drop rows with NaN values
merged_df.dropna(inplace=True)

# Calculate correlation
correlation_matrix = merged_df[['Inflation_Change', 'CNXIT_Change', 'NSEI_Change']].corr()

# Plot correlation heatmap
fig, ax = plt.subplots()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
plt.title('Correlation Heatmap')
st.pyplot(fig)

# Plot time series data
fig, ax = plt.subplots()
merged_df[['Inflation', '^CNXIT', '^NSEI']].plot(ax=ax)
plt.title('Time Series Data')
plt.xlabel('Date')
plt.ylabel('Value')
st.pyplot(fig)

# Display the data
st.write("Merged DataFrame:")
st.dataframe(merged_df)

st.write("Correlation Matrix:")
st.dataframe(correlation_matrix)
