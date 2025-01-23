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
stock_data = yf.download(tickers, start='2023-01-01', end='2024-11-30', interval='1mo')['Close']

# Merge inflation data with stock data
merged_df = pd.merge(inflation_df, stock_data, left_index=True, right_index=True, how='inner')

# Calculate percentage changes
merged_df['Inflation_Change'] = merged_df['Inflation'].pct_change()
merged_df['^CNXIT_Change'] = merged_df['^CNXIT'].pct_change()
merged_df['^NSEI_Change'] = merged_df['^NSEI'].pct_change()

# Drop NaN values
merged_df.dropna(inplace=True)

# Calculate correlation matrix
correlation_matrix = merged_df[['Inflation_Change', '^CNXIT_Change', '^NSEI_Change']].corr()

# Plot correlation heatmap
st.subheader("Correlation Heatmap")
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
st.pyplot(plt)

# Plot time series
st.subheader("Time Series of Inflation and Stock Prices")
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Date')
ax1.set_ylabel('Inflation Rate (%)', color='tab:blue')
ax1.plot(merged_df.index, merged_df['Inflation'], color='tab:blue', label='Inflation')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Stock Prices', color='tab:green')
ax2.plot(merged_df.index, merged_df['^CNXIT'], color='tab:green', label='^CNXIT')
ax2.plot(merged_df.index, merged_df['^NSEI'], color='tab:red', label='^NSEI')
ax2.tick_params(axis='y', labelcolor='tab:green')

fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
st.pyplot(fig)

# Display data
st.subheader("Merged Data")
st.write(merged_df)

# Display correlation matrix
st.subheader("Correlation Matrix")
st.write(correlation_matrix)

st.markdown("""
    <div style="text-align: center; font-size: 14px; margin-top: 30px;">
        <p><strong>App Code:</strong> Stock-Dividend-Prediction-Jan-2025</p>
        <p>To get access to the stocks file to upload, please Email us at <a href="mailto:support@pystatiq.com">support@pystatiq.com</a>.</p>
        <p>Don't forget to add the Application code.</p>
        <p><strong>README:</strong> <a href="https://pystatiq-lab.gitbook.io/docs/python-apps/stock-dividend-predictions" target="_blank">https://pystatiq-lab.gitbook.io/docs/python-apps/stock-dividend-predictions</a></p>
    </div>
""", unsafe_allow_html=True)

# Display Footer Logo
st.markdown(f"""
    <style>
        .footer-logo {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 90px;
            padding-top: 30px;
        }}
    </style>
    <img class="footer-logo" src="https://predictram.com/images/logo.png" alt="Footer Logo">
""", unsafe_allow_html=True)
