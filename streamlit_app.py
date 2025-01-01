import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

# Fonction pour récupérer les données de BTC
def get_btc_data(period):
    btc = yf.Ticker("BTC-USD")
    try:
        data = btc.history(period=period, interval="1h")
        if data.empty:
            raise ValueError("No data retrieved for the specified period.")
    except Exception as e:
        print(f"Error fetching data: {e}")
        data = None
    return data

# Fonction pour calculer la performance
def calculate_performance(data, hours):
    if data is None or data.empty:
        raise ValueError("Data is empty. Cannot calculate performance.")

    recent_time = data.index[-1]
    past_time = recent_time - timedelta(hours=hours)

    if past_time in data.index:
        past_price = data.loc[past_time]['Close']
    else:
        past_data = data[data.index <= past_time]
        if past_data.empty:
            raise ValueError("Not enough data to calculate performance.")
        past_price = past_data['Close'].iloc[-1]

    current_price = data.iloc[-1]['Close']
    performance = ((current_price - past_price) / past_price) * 100
    return current_price, performance

# Récupération des données
btc_data = get_btc_data("5d")  # Récupère 5 jours de données pour s'assurer de suffisamment d'informations

if btc_data is not None:
    try:
        # Calcul de la performance sur 1 heure et 24 heures
        current_price_1h, perf_1h = calculate_performance(btc_data, 1)
        current_price_24h, perf_24h = calculate_performance(btc_data, 24)

        # Affichage des résultats
        st.title(f"Prix actuel: ${current_price_1h:.2f}")
        st.title(f"Performance sur 1 heure: {perf_1h:.2f}%")
        st.title(f"Performance sur 24 heures: {perf_24h:.2f}%")

        # Création du graphique
        plt.figure(figsize=(10, 6))
        plt.plot(btc_data.index, btc_data['Close'], label="Cours du BTC")
        plt.title("Cours du Bitcoin (BTC-USD)")
        plt.xlabel("Temps")
        plt.ylabel("Prix ($)")
        plt.axhline(y=current_price_1h, color='r', linestyle='--', label=f'Prix actuel: ${current_price_1h:.2f}')
        plt.legend()
        plt.grid()
        plt.show()
    except ValueError as ve:
        print(f"Error in processing data: {ve}")
else:
    print("Failed to retrieve Bitcoin data.")