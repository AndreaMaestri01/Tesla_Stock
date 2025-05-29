import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the ticker for the 5-year US Treasury bond
ticker = '^FVX'  # Ticker for the 5-year US Treasury bond interest rate
period = '3mo'  # Last 3 months
interval = '1d'  # Daily granularity

# Download historical data
bond_data = yf.download(ticker, period=period, interval=interval)

# Check the downloaded data
print(bond_data.head())

# Calculate the average interest rate
average_interest_rate = bond_data['Close'].mean()

# Convert average_interest_rate to float
average_interest_rate_float = float(average_interest_rate)

# Create the interest rate plot
plt.figure(figsize=(12, 6))
plt.plot(bond_data.index, bond_data['Close'], '-g', label='US5Y Interest Rate')
plt.axhline(y=average_interest_rate_float, color='r', linestyle='--', label=f'Average Interest Rate: {average_interest_rate_float:.2f}%')
plt.title('US5Y Treasury Bond Interest Rate Over the Last 3 Months')
plt.xlabel('')
plt.ylabel('Interest Rate (%)')
plt.legend()
plt.grid(False)
plt.show()

# Print the average interest rate
print(f'Average 5-Year US Treasury Bond Interest Rate Over the Last Year: {average_interest_rate_float:.2f}%')