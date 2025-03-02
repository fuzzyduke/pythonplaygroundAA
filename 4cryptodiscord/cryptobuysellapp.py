import requests
import pandas as pd
import ta
import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# ✅ File Paths
XML_FILE = "crypto_data.xml"
CONFIG_FILE = "crypto_config.txt"

# ✅ Binance API Endpoint
BINANCE_URL = "https://api.binance.com/api/v3/klines"

# ✅ Load Crypto Pairs from Config
def load_crypto_pairs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            pairs = [line.strip() for line in f.readlines()]
            return {pair: pair.replace("USDT", "") for pair in pairs}
    return {"BTCUSDT": "Bitcoin"}  # Default Pair: BTC

# ✅ Save Crypto Pairs to Config
def save_crypto_pairs(crypto_pairs):
    with open(CONFIG_FILE, "w") as f:
        for pair in crypto_pairs.keys():
            f.write(pair + "\n")

# ✅ Fetch OHLCV Data from Binance
def get_historical_data(symbol):
    params = {"symbol": symbol, "interval": "4h", "limit": 50}
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
        return None, None, None

    df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()

    return df["RSI"].iloc[-1], df["BB_upper"].iloc[-1], df["BB_lower"].iloc[-1]

# ✅ Save Data to XML
def save_to_xml(crypto_data):
    root = ET.Element("CryptoData")
    
    for symbol, data in crypto_data.items():
        token = ET.SubElement(root, "Token", name=data["name"], symbol=symbol)
        ET.SubElement(token, "RSI").text = str(round(data["RSI"], 2))
        ET.SubElement(token, "BB_upper").text = str(round(data["BB_upper"], 2))
        ET.SubElement(token, "BB_lower").text = str(round(data["BB_lower"], 2))
    
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)
    messagebox.showinfo("Success", f"Data saved to {XML_FILE}")

# ✅ GUI Functions
def fetch_data():
    global crypto_pairs
    crypto_data = {}
    result_text.delete(1.0, tk.END)  # Clear previous results
    result_text.insert(tk.END, "Fetching 4-hour RSI & Bollinger Bands...\n")

    for symbol, name in crypto_pairs.items():
        df = get_historical_data(symbol)
        rsi, bb_upper, bb_lower = calculate_indicators(df)

        if rsi is not None:
            result_text.insert(tk.END, f"\n🔹 {name} ({symbol})\n")
            result_text.insert(tk.END, f"   RSI (14): {rsi:.2f}\n")
            result_text.insert(tk.END, f"   Bollinger Bands Upper: ${bb_upper:.2f}\n")
            result_text.insert(tk.END, f"   Bollinger Bands Lower: ${bb_lower:.2f}\n")

            crypto_data[symbol] = {"name": name, "RSI": rsi, "BB_upper": bb_upper, "BB_lower": bb_lower}
    
    save_to_xml(crypto_data)

def add_token():
    global crypto_pairs
    new_symbol = simpledialog.askstring("Add Token", "Enter token symbol (e.g., ETHUSDT):").upper()
    new_name = simpledialog.askstring("Add Token", f"Enter the name for {new_symbol} (e.g., Ethereum):")

    if new_symbol and new_name:
        if new_symbol not in crypto_pairs:
            crypto_pairs[new_symbol] = new_name
            save_crypto_pairs(crypto_pairs)
            token_listbox.insert(tk.END, f"{new_name} ({new_symbol})")
            messagebox.showinfo("Success", f"{new_name} ({new_symbol}) added!")
        else:
            messagebox.showwarning("Warning", "Token already exists!")

def remove_token():
    global crypto_pairs
    selected = token_listbox.curselection()

    if selected:
        index = selected[0]
        symbol = list(crypto_pairs.keys())[index]
        del crypto_pairs[symbol]
        save_crypto_pairs(crypto_pairs)
        token_listbox.delete(index)
        messagebox.showinfo("Success", f"{symbol} removed!")

def view_xml():
    if os.path.exists(XML_FILE):
        with open(XML_FILE, "r") as f:
            xml_content = f.read()
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, xml_content)
    else:
        messagebox.showwarning("Warning", "No XML data found!")

# ✅ Initialize GUI
root = tk.Tk()
root.title("Crypto RSI & Bollinger Bands Tracker")
root.geometry("500x500")

crypto_pairs = load_crypto_pairs()

# ✅ Buttons
tk.Button(root, text="Fetch Data", command=fetch_data).pack(pady=5)
tk.Button(root, text="Add Token", command=add_token).pack(pady=5)
tk.Button(root, text="Remove Token", command=remove_token).pack(pady=5)
tk.Button(root, text="View Stored XML", command=view_xml).pack(pady=5)

# ✅ Listbox for Token List
token_listbox = tk.Listbox(root, height=6)
token_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# ✅ Load Initial Token List
for symbol, name in crypto_pairs.items():
    token_listbox.insert(tk.END, f"{name} ({symbol})")

# ✅ Text Box to Show Results
result_text = tk.Text(root, height=10)
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# ✅ Run the App
root.mainloop()
