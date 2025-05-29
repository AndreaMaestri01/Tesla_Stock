import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Definisci il ticker e il periodo
ticker = 'TSLA'
period = '3mo'  # Ultimi 3 mesi
interval = '1d'  # Granularità giornaliera

# Scarica i dati storici
tesla_data = yf.download(ticker, period=period, interval=interval)

# Controlla i dati scaricati
print(tesla_data.head())

# Calcola i rendimenti giornalieri
tesla_data['Returns'] = tesla_data['Close'].pct_change()

# Calcola la volatilità storica (deviazione standard dei rendimenti)
tesla_data['Volatility'] = tesla_data['Returns'].rolling(window=21).std() * np.sqrt(252)

# Calcola la volatilità media
average_volatility = tesla_data['Volatility'].mean()

# Crea il grafico dei prezzi di chiusura
plt.figure(figsize=(12, 6))
plt.plot(tesla_data.index, tesla_data['Close'], '-g', label='Closing Price')
plt.title('Tesla Stock Price in the Last 3 Months')
plt.xlabel('Date')
plt.ylabel('Closing Price ($)')
plt.legend()
plt.grid(False)
plt.show()

# Crea il grafico della volatilità storica
plt.figure(figsize=(12, 6))
plt.plot(tesla_data.index, tesla_data['Volatility'], '-g', label='Historical Volatility')
plt.axhline(y=average_volatility, color='r', linestyle='--', label=f'Average Volatility: {average_volatility:.2f}')
plt.title('Historical Volatility of Tesla Stock Price in the Last 3 Months')
plt.xlabel('')
plt.ylabel('Volatility')
plt.legend()
plt.grid(False)
plt.show()

# Stampa la volatilità media
print(f'Average Volatility of Tesla Stock Price in the Last 3 Months: {average_volatility:.2f}')
