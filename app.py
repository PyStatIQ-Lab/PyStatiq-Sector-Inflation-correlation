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

# Check the structure of the returned DataFrame
st.write("Stock Data Structure:")
st.write(stock_data.head())

# Ensure 'Adj Close' column exists
if 'Adj Close' in stock_data.columns.levels[0]:
    stock_data = stock_data['Adj Close']
else:
    st.error("The 'Adj Close' column is not available in the downloaded stock data.")
    st.stop()

# Calculate percentage change for inflation and stock data
inflation_df['Inflation_Change'] = inflation_df['Inflation'].pct_change()
stock_data_pct_change = stock_data.pct_change()

# Merge the dataframes
merged_df = pd.merge(inflation_df, stock_data_pct_change, left_index=True, right_index=True, how='inner')

# Plot the data
st.write("Merged Data:")
st.write(merged_df.head())

# Correlation analysis
correlation_matrix = merged_df.corr()
st.write("Correlation Matrix:")
st.write(correlation_matrix)

# Plot correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
st.pyplot(plt)

# Plot trends
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()
ax1.plot(merged_df.index, merged_df['Inflation_Change'], 'g-')
ax2.plot(merged_df.index, merged_df['^CNXIT'], 'b-')
ax2.plot(merged_df.index, merged_df['^NSEI'], 'r-')

ax1.set_xlabel('Date')
ax1.set_ylabel('Inflation Change', color='g')
ax2.set_ylabel('Stock Change', color='b')
plt.title('Inflation vs Stock Market Sectors')
st.pyplot(fig)
