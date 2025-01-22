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

# Download stock data
tickers = ['^CNXIT', '^NSEI']
stock_data = yf.download(tickers, start='2023-01-01', end='2024-11-30', interval='1mo')['Adj Close']

# Merge inflation data with stock data
merged_df = stock_data.copy()
merged_df['Inflation'] = inflation_df.set_index('Date')['Inflation']
merged_df.dropna(inplace=True)

# Calculate percentage change
merged_df['Inflation_Change'] = merged_df['Inflation'].pct_change()
merged_df['CNXIT_Change'] = merged_df['^CNXIT'].pct_change()
merged_df['NSEI_Change'] = merged_df['^NSEI'].pct_change()

# Drop the first row as it contains NaN values due to pct_change()
merged_df = merged_df.dropna()

# Display the merged DataFrame
st.write("Merged DataFrame with Inflation and Stock Data:")
st.dataframe(merged_df)

# Correlation analysis
correlation_matrix = merged_df[['Inflation_Change', 'CNXIT_Change', 'NSEI_Change']].corr()
st.write("Correlation Matrix:")
st.write(correlation_matrix)

# Plotting
st.write("Inflation and Stock Performance Over Time:")
fig, ax1 = plt.subplots(figsize=(14, 7))

ax2 = ax1.twinx()
ax1.plot(merged_df.index, merged_df['Inflation'], 'g-')
ax2.plot(merged_df.index, merged_df['^CNXIT'], 'b-')
ax2.plot(merged_df.index, merged_df['^NSEI'], 'r-')

ax1.set_xlabel('Date')
ax1.set_ylabel('Inflation Rate', color='g')
ax2.set_ylabel('Stock Index Value', color='b')

ax1.legend(['Inflation'], loc='upper left')
ax2.legend(['^CNXIT', '^NSEI'], loc='upper right')

st.pyplot(fig)

# Seaborn heatmap for correlation matrix
st.write("Correlation Matrix Heatmap:")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)
