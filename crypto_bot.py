import os
from keep_alive import keep_alive
import requests
from telegram import Bot
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=TOKEN)

# Top 10 coins
coins = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT',
    'AVAXUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT'
]

# Fetch current price of the coin
def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    data = requests.get(url).json()
    return float(data['price'])

# Determine market trend using last two 5-minute candles
def get_market_trend(symbol):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=2'
    candles = requests.get(url).json()
    last_candle = candles[-2]
    open_price = float(last_candle[1])
    close_price = float(last_candle[4])
    return "BUY" if close_price > open_price else "SELL"

# Send signal message to Telegram
def send_signal(symbol, price, action):
    target = round(price * (1.02 if action == "BUY" else 0.98), 2)
    stop_loss = round(price * (0.998 if action == "BUY" else 1.002), 2)

    message = f"""📢 *{action} Signal* 📢

🪙 *Coin:* {symbol}
💰 *Action:* {action}
🔹 *Entry Price:* ${round(price, 2)}
🎯 *Target:* ${target}
🛑 *Stop Loss:* ${stop_loss}

📊 Trend-based signal | Risk Management advised!
"""
    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')

# Main loop
print("🤖 Bot is Live... Posting to Telegram")
while True:
    start_time = time.time()
    for symbol in coins:
        try:
            trend = get_market_trend(symbol)
            price = get_price(symbol)
            send_signal(symbol, price, trend)
            print(f"✅ Signal sent for {symbol}")
            time.sleep(180)  # Wait 3 mins before sending the next coin signal
        except Exception as e:
            print(f"⚠️ Error for {symbol}:", e)
            time.sleep(10)
    elapsed = time.time() - start_time
    wait_time = 300 - elapsed  # Wait remaining time to complete 5 mins round
    if wait_time > 0:
        print(f"⏳ Waiting {int(wait_time)}s before new round")
        time.sleep(wait_time)
