import requests
import pandas as pd
import ta
import xml.etree.ElementTree as ET
import os

# ✅ XML file to store RSI & Bollinger Band values
XML_FILE = "crypto_data.xml"
CONFIG_FILE = "crypto_config.txt"

# ✅ Binance API endpoint
BINANCE_URL = "https://api.binance.com/api/v3/klines"

# ✅ Function to load tokens from the config file
def load_crypto_pairs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            pairs = [line.strip() for line in f.readlines()]
            return {pair: pair.replace("USDT", "") for pair in pairs}
    return {"ETHUSDT": "Ethereum", "DOTUSDT": "Polkadot", "SEIUSDT": "Sei"}

# ✅ Function to save tokens to the config file
def save_crypto_pairs(crypto_pairs):
    with open(CONFIG_FILE, "w") as f:
        for pair in crypto_pairs.keys():
            f.write(pair + "\n")

# ✅ Function to fetch OHLCV data from Binance
def get_historical_data(symbol):
    params = {
        "symbol": symbol,
        "interval": "4h",
        "limit": 50
    }
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
        print(f"❌ Failed to fetch data for {symbol}")
        return None

# ✅ Function to calculate RSI & Bollinger Bands
def calculate_indicators(df):
    if df is None:
        return None, None, None
    
    df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
    df["BB_upper"] = bb.bollinger_hband()
    df["BB_lower"] = bb.bollinger_lband()

    return df["RSI"].iloc[-1], df["BB_upper"].iloc[-1], df["BB_lower"].iloc[-1]

# ✅ Function to save results to an XML file
def save_to_xml(crypto_data):
    root = ET.Element("CryptoData")
    
    for symbol, data in crypto_data.items():
        token = ET.SubElement(root, "Token", name=data["name"], symbol=symbol)
        ET.SubElement(token, "RSI").text = str(round(data["RSI"], 2))
        ET.SubElement(token, "BB_upper").text = str(round(data["BB_upper"], 2))
        ET.SubElement(token, "BB_lower").text = str(round(data["BB_lower"], 2))
    
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)
    print(f"✅ Data saved to {XML_FILE}")

# ✅ Main Function to Run the App
def main():
    crypto_pairs = load_crypto_pairs()

    while True:
        print("\n📊 Crypto Tracker App")
        print("1️⃣ Fetch Latest RSI & Bollinger Bands")
        print("2️⃣ Add a Cryptocurrency")
        print("3️⃣ Remove a Cryptocurrency")
        print("4️⃣ View Stored XML Data")
        print("5️⃣ Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            crypto_data = {}
            print("\nFetching 4-hour RSI & Bollinger Bands...")

            for symbol, name in crypto_pairs.items():
                df = get_historical_data(symbol)
                rsi, bb_upper, bb_lower = calculate_indicators(df)

                if rsi is not None:
                    print(f"\n🔹 {name} ({symbol})")
                    print(f"   RSI (14): {rsi:.2f}")
                    print(f"   Bollinger Bands Upper: ${bb_upper:.2f}")
                    print(f"   Bollinger Bands Lower: ${bb_lower:.2f}")

                    # ✅ Store data for XML saving
                    crypto_data[symbol] = {
                        "name": name,
                        "RSI": rsi,
                        "BB_upper": bb_upper,
                        "BB_lower": bb_lower
                    }
                else:
                    print(f"❌ Could not calculate indicators for {name}")

            # ✅ Save results to XML
            save_to_xml(crypto_data)

        elif choice == "2":
            new_symbol = input("Enter new token symbol (e.g., BTCUSDT): ").upper()
            new_name = input(f"Enter the name for {new_symbol} (e.g., Bitcoin): ")

            if new_symbol not in crypto_pairs:
                crypto_pairs[new_symbol] = new_name
                save_crypto_pairs(crypto_pairs)
                print(f"✅ {new_name} ({new_symbol}) added!")
            else:
                print("⚠️ Token already exists!")

        elif choice == "3":
            remove_symbol = input("Enter token symbol to remove (e.g., BTCUSDT): ").upper()
            
            if remove_symbol in crypto_pairs:
                del crypto_pairs[remove_symbol]
                save_crypto_pairs(crypto_pairs)
                print(f"✅ {remove_symbol} removed!")
            else:
                print("⚠️ Token not found!")

        elif choice == "4":
            if os.path.exists(XML_FILE):
                with open(XML_FILE, "r") as f:
                    print("\n📂 Stored XML Data:\n")
                    print(f.read())
            else:
                print("⚠️ No XML data found!")

        elif choice == "5":
            print("🚀 Exiting Crypto Tracker App. Goodbye!")
            break

        else:
            print("❌ Invalid choice, try again!")

# ✅ Run the program
if __name__ == "__main__":
    main()
