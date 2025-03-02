import requests
import pandas as pd
import ta
import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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

# ✅ Save Data to XML
def save_to_xml(crypto_data):
    root = ET.Element("CryptoData")
    
    for symbol, data in crypto_data.items():
        token = ET.SubElement(root, "Token", name=data["name"], symbol=symbol)
        ET.SubElement(token, "Price").text = str(round(data["Price"], 2))
        ET.SubElement(token, "RSI").text = str(round(data["RSI"], 2))
        ET.SubElement(token, "BB_upper").text = str(round(data["BB_upper"], 2))
        ET.SubElement(token, "BB_lower").text = str(round(data["BB_lower"], 2))
    
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

    save_to_xml(crypto_data)

# ✅ Add Token
def add_token():
    global crypto_pairs
    new_symbol = simpledialog.askstring("Add Token", "Enter token symbol (e.g., ETHUSDT):").upper()
    new_name = simpledialog.askstring("Add Token", f"Enter the name for {new_symbol} (e.g., Ethereum):")

    if new_symbol and new_name:
        if new_symbol not in crypto_pairs:
            crypto_pairs[new_symbol] = new_name
            save_crypto_pairs(crypto_pairs)
            token_listbox.insert(tk.END, f"{new_name} ({new_symbol})")
        else:
            messagebox.showwarning("Warning", "Token already exists!")

# ✅ Remove Token
def remove_token():
    global crypto_pairs
    selected = token_listbox.curselection()

    if selected:
        index = selected[0]
        symbol = list(crypto_pairs.keys())[index]
        del crypto_pairs[symbol]
        save_crypto_pairs(crypto_pairs)
        token_listbox.delete(index)

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

# ✅ Token Listbox
tk.Label(root, text="Tracked Tokens").pack()
token_listbox = tk.Listbox(root, height=5)
token_listbox.pack(fill=tk.BOTH, expand=True)

# ✅ Populate Listbox with existing tokens
for symbol, name in crypto_pairs.items():
    token_listbox.insert(tk.END, f"{name} ({symbol})")

# ✅ Buttons for Add/Remove Tokens
tk.Button(root, text="Add Token", command=add_token).pack(pady=5)
tk.Button(root, text="Remove Token", command=remove_token).pack(pady=5)

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
