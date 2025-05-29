import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def CSS_Binomial_Tree_Labeled_PLOT(S):
    plt.figure(figsize=(10, 6))
    
    for i in range(N + 1):
        for j in range(i + 1):
            if i > 0:
                if j > 0:
                    plt.plot([i - 1, i], [S[j - 1, i - 1], S[j, i]], 'g-', lw=1.5)  # Connessione inferiore verde
                if j < i:
                    plt.plot([i - 1, i], [S[j, i - 1], S[j, i]], 'g-', lw=1.5)  # Connessione superiore verde

    # Aggiunta delle etichette in formato LaTeX dentro la griglia
    plt.text(0, S0+1, r'$S_0$', fontsize=16, color='green', verticalalignment='bottom', horizontalalignment='center')
    for j in range(N + 1):
        offset_x = 0.1  # Sposta le etichette leggermente a destra
        offset_y = 0 # Sposta le etichette leggermente in alto
        plt.text(N + offset_x, S[j, N] + offset_y,rf'$S_{{{N},{j}}}$', fontsize=16, color='green', verticalalignment='center', horizontalalignment='center')

    plt.title("")
    plt.xlabel(r'Time step $(\Delta t)$', fontsize=14)
    plt.ylabel(r'Stock price $(S_t)$', fontsize=14)
    plt.xticks(range(N + 1))
    plt.grid(False)
    plt.show()

def CSS_Binomial_Tree_PLOT(S):
    plt.figure(figsize=(10, 6))
    
    for i in range(N + 1):
        for j in range(i + 1):
            if i > 0:
                if j > 0:
                    plt.plot([i - 1, i], [S[j - 1, i - 1], S[j, i]], 'g-', lw=1.5)  # Connessione inferiore verde
                if j < i:
                    plt.plot([i - 1, i], [S[j, i - 1], S[j, i]], 'g-', lw=1.5)  # Connessione superiore verde
    plt.title("")
    plt.xlabel(r'Time step $(\Delta t)$', fontsize=14)
    plt.ylabel(r'Stock price $(S_t)$', fontsize=14)
    plt.grid(False)
    plt.show()

def Call_vs_N_PLOT(Ns, CSS_Call_Values, BS_Call_Value):
    plt.figure(figsize=(10, 6))
    
    # Traccia il grafico dei valori call
    plt.plot(Ns, CSS_Call_Values, 'og', lw=1, label='Cox-Ross-Rubinstein Model')
    
    # Aggiungi una linea orizzontale tratteggiata rossa
    plt.axhline(y=BS_Call_Value, color='r', linestyle='--', label=f'Black-Scholes Model')
    
    # Aggiungi titolo e etichette
    plt.title("")
    plt.xlabel(r'Number of Time steps ($N$)', fontsize=14)
    plt.ylabel(r'Call Option Value ($C$)', fontsize=14)
    
    # Aggiungi la legenda
    plt.legend(fontsize=12)
    
    # Mostra il grafico
    plt.grid(False)
    plt.show()

def Err_Call_vs_N_PLOT(Ns, CSS_Call_Values, BS_Call_Value):
    plt.figure(figsize=(10, 6))
    
    # Traccia il grafico dei valori call
    plt.plot(Ns, 100*((np.abs(CSS_Call_Values-BS_Call_Value))/BS_Call_Value), 'o-g', lw=1)
    
    
    # Aggiungi titolo e etichette
    plt.title("")
    plt.xlabel(r'Number of Time steps ($N$)', fontsize=14)
    plt.ylabel(r'Percentage Error ($\%$)', fontsize=14)
    
    # Aggiungi la legenda
    plt.legend(fontsize=12)
    
    # Mostra il grafico
    plt.grid(False)
    plt.show()

def Binomial_Matrix(S0, T, N, r, sigma):
    dt = T / N  # Intervallo di tempo
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    S = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        for j in range(i + 1):
            S[j, i] = S0 * (u**j) * (d**(i - j))
    return S

def CSS_Call(S, X, N, r, T, sigma):
    payoff = np.maximum(S[:, N] - X, 0)
    dt = T / N  # Intervallo di tempo
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    C = np.zeros((N + 1, N + 1))
    C[:, N] = payoff
    
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            C[j, i] = (p * C[j + 1, i + 1] + (1 - p) * C[j, i + 1]) * np.exp(-r * dt)
    call_value = C[0, 0]
    return call_value

def BS_Call(S, X, T, r, sigma):
    d1 = (np.log(S/X) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_value = S * norm.cdf(d1) - X * np.exp(-r*T)* norm.cdf(d2)
    return call_value




# Parametri
r = 0.05  # Tasso di interesse
sigma = 0.4  # Volatilità
T = 0.5  # Tempo a scadenza
S0 = 100  # Prezzo iniziale dell'azione
X = 105  # Strike price
Ns = np.logspace(np.log10(4), np.log10(500), num=50, dtype=int)
# Lista per memorizzare i valori della Call
CSS_Call_Values = []
BS_Call_Value = BS_Call(S0, X, T, r, sigma)

for N in Ns:
    # Creazione della matrice dell'albero binomiale
    S = Binomial_Matrix(S0, T, N, r, sigma)

    # Calcolo del valore dell'opzione Call
    C_temp = CSS_Call(S, X, N, r, T, sigma)
    CSS_Call_Values.append(C_temp)


print (BS_Call_Value)


