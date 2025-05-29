import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def CSS_Call(S0, X, N, r, T, sigma):
    dt = T / N  # Intervallo di tempo
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    S = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        for j in range(i + 1):
            S[j, i] = S0 * (u**j) * (d**(i - j))

    payoff = np.maximum(S[:, N] - X, 0)
    C = np.zeros((N + 1, N + 1))
    C[:, N] = payoff
    
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            C[j, i] = (p * C[j + 1, i + 1] + (1 - p) * C[j, i + 1]) * np.exp(-r * dt)
    call_value = C[0, 0]
    return call_value

# Ottieni i dati delle opzioni di Tesla
tesla = yf.Ticker("TSLA")
options = tesla.options  # Ottieni le opzioni disponibili
opt = tesla.option_chain(options[0]).calls  # Carica i dati per la prima data di scadenza disponibile

# Prezzo dell'opzione e prezzo di esercizio
price = np.array(opt['lastPrice'])  # Prezzo dell'opzione
Strike = np.array(opt['strike'])  # Prezzo di esercizio

# Tempo alla scadenza in giorni
Time_of_trade = opt['lastTradeDate']
Time_to_Maturity = np.array([(dt.datetime.strptime(options[0], "%Y-%m-%d") - dt.datetime.strptime(str(trade)[:10], "%Y-%m-%d")).days / 252
                             for trade in Time_of_trade])

# Ottieni i dati storici di Tesla
tesla_data = tesla.history(period="1y", interval="1d")

# Calcola i rendimenti giornalieri
tesla_data['Returns'] = tesla_data['Close'].pct_change()

# Calcola la volatilità storica (deviazione standard dei rendimenti)
tesla_data['Volatility'] = tesla_data['Returns'].rolling(window=21).std() * np.sqrt(252)

# Ottieni la volatilità e il valore dell'azione nel giorno di chiusura in cui è avvenuto il trade dell'opzione
volatility = []
stock_price = []

for trade_date in Time_of_trade:
    trade_date_str = str(trade_date)[:10]
    if trade_date_str in tesla_data.index:
        volatility.append(tesla_data.loc[trade_date_str, 'Volatility'])
        stock_price.append(tesla_data.loc[trade_date_str, 'Close'])
    else:
        volatility.append(np.nan)
        stock_price.append(np.nan)

volatility = np.array(volatility)
stock_price = np.array(stock_price)

# Calcola il valore dell'opzione call con CSS
N = 50
r = 0.0417  # Tasso di interesse (esempio)
call_values = []

for S0, X, T, sigma in zip(stock_price, Strike, Time_to_Maturity, volatility):
    if not np.isnan(S0) and not np.isnan(sigma):
        call_value = CSS_Call(S0, X, N, r, T, sigma)
        call_values.append(call_value)
    else:
        call_values.append(np.nan)

call_values = np.array(call_values)


# Create the final plot comparing real data and CSS model predictions
plt.figure(figsize=(12, 6))
plt.plot(Strike, call_values, 'r:', label="CSS Model Option Price",lw=2)  # Reduced marker size
plt.plot(Strike, price, 'go', label="Real Option Price",markerfacecolor='none',ms=7)  # Reduced marker size

plt.xlabel("Strike Price")
plt.ylabel("Value ($)")
plt.title("Comparison of Real Option Price and CSS Model Value")
plt.legend()
plt.grid(False)
plt.show()













