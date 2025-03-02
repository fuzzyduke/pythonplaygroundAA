import requests
import pandas as pd
import ta
import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ✅ Set Your Discord Webhook URL Here
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1345757150181458010/k2iqmVBrn3vUyTjUlRpumT96k5WqYtxXxZ1B9t3mGrwnOaCxlAqGN8kmQJQq7-LhY4le"

# ✅ File Paths
XML_FILE = "crypto_data.xml"
CONFIG_FILE = "crypto_config.txt"

# ✅ Binance API Endpoint
BINANCE_URL = "https://api.binance.com/api/v3/klines"

# ✅ Available Time Intervals
TIME_INTERVALS = {
    "4h": "4h",
    "8h": "8h",
    "12h": "12h",
    "1 Day": "1d",
    "1 Week": "1w"
}

# ✅ Load Crypto Pairs
def load_crypto_pairs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            pairs = [line.strip() for line in f.readlines()]
            return {pair: pair.replace("USDT", "") for pair in pairs}
    return {"BTCUSDT": "Bitcoin"}  # Default Pair: BTC

# ✅ Save Crypto Pairs
def save_crypto_pairs(crypto_pairs):
    with open(CONFIG_FILE, "w") as f:
        for pair in crypto_pairs.keys():
            f.write(pair + "\n")

# ✅ Fetch OHLCV Data
def get_historical_data(symbol, interval):
    params = {"symbol": symbol, "interval": interval, "limit": 50}
    response = requests.get(BINANCE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        return df
    else:
        messagebox.showerror("Error", f"Failed to fetch data for {symbol}")
        return None

# ✅ Calculate RSI & Bollinger Bands
def calculate_indicators(df):
    if df is None:
        return None, None, None, None

    df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()

    latest_price = df["close"].iloc[-1]
    return latest_price, df["RSI"].iloc[-1], df["BB_upper"].iloc[-1], df["BB_lower"].iloc[-1]

# ✅ Send Discord Alert
def send_discord_alert(message):
    if DISCORD_WEBHOOK_URL:
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    else:
        print("❌ Discord Webhook URL is not set!")

# ✅ Save Data to XML and Send Alerts
def save_to_xml_and_alert(crypto_data):
    root = ET.Element("CryptoData")

    for symbol, data in crypto_data.items():
        token = ET.SubElement(root, "Token", name=data["name"], symbol=symbol)
        ET.SubElement(token, "Price").text = str(round(data["Price"], 2))
        ET.SubElement(token, "RSI").text = str(round(data["RSI"], 2))
        ET.SubElement(token, "BB_upper").text = str(round(data["BB_upper"], 2))
        ET.SubElement(token, "BB_lower").text = str(round(data["BB_lower"], 2))

        # ✅ Check if RSI or Price is out of bounds and send alert
        alert_message = f"⚠️ **{data['name']} ({symbol}) Alert**\n"
        alert_triggered = False

        if data["RSI"] > 70:
            alert_message += f"🔴 RSI Overbought: {data['RSI']:.2f} (>70)\n"
            alert_triggered = True
        elif data["RSI"] < 30:
            alert_message += f"🔵 RSI Oversold: {data['RSI']:.2f} (<30)\n"
            alert_triggered = True

        if data["Price"] > data["BB_upper"]:
            alert_message += f"🚀 Price Above Bollinger Band: ${data['Price']:.2f}\n"
            alert_triggered = True
        elif data["Price"] < data["BB_lower"]:
            alert_message += f"📉 Price Below Bollinger Band: ${data['Price']:.2f}\n"
            alert_triggered = True

        if alert_triggered:
            send_discord_alert(alert_message)

    tree = ET.ElementTree(root)
    tree.write(XML_FILE)

# ✅ Fetch Data and Display in Table
def fetch_data():
    global crypto_pairs
    crypto_data = {}
    
    selected_interval = interval_var.get()
    binance_interval = TIME_INTERVALS[selected_interval]

    # Clear Table
    for row in table.get_children():
        table.delete(row)

    for symbol, name in crypto_pairs.items():
        df = get_historical_data(symbol, binance_interval)
        price, rsi, bb_upper, bb_lower = calculate_indicators(df)

        if price is not None:
            crypto_data[symbol] = {
                "name": name, "Price": price, "RSI": rsi, "BB_upper": bb_upper, "BB_lower": bb_lower
            }

            # Determine Color for Price & Indicators
            price_color = "red" if price > bb_upper or price < bb_lower else "black"
            rsi_color = "red" if rsi > 70 or rsi < 30 else "black"

            table.insert("", "end", values=(
                name, symbol, f"${price:.2f}", f"{rsi:.2f}", f"${bb_upper:.2f}", f"${bb_lower:.2f}"
            ), tags=(price_color, rsi_color))

    save_to_xml_and_alert(crypto_data)

# ✅ Initialize GUI
root = tk.Tk()
root.title("Crypto RSI & Bollinger Bands Tracker")
root.geometry("700x600")

crypto_pairs = load_crypto_pairs()

# ✅ Interval Selection
interval_var = tk.StringVar(value="4h")
interval_menu = ttk.Combobox(root, textvariable=interval_var, values=list(TIME_INTERVALS.keys()))
interval_menu.pack(pady=5)

# ✅ Buttons
tk.Button(root, text="Fetch Data", command=fetch_data).pack(pady=5)

# ✅ Table for Results
table_frame = ttk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Name", "Symbol", "Price", "RSI", "BB Upper", "BB Lower")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

table.pack(fill=tk.BOTH, expand=True)

# ✅ Color Tags for Warnings
table.tag_configure("red", foreground="red")
table.tag_configure("black", foreground="black")

# ✅ Run the App
root.mainloop()
