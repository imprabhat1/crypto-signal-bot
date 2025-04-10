from keep_alive import keep_alive
import requests
from telegram import Bot
import time
import os

# Start Replit web server to keep bot alive
keep_alive()

# Load secrets from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Top 10 coins
coins = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
    'ADAUSDT', 'AVAXUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT'
]

# Get latest price from Binance
def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    data = requests.get(url).json()
    return float(data['price'])

# Check 5-minute market trend
def get_market_trend(symbol):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=2'
    candles = requests.get(url).json()
    last_candle = candles[-2]
    open_price = float(last_candle[1])
    close_price = float(last_candle[4])
    return "BUY" if close_price > open_price else "SELL"

# Send message to Telegram
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

# Main bot loop
print("🤖 Bot is Live... Posting to Telegram")
while True:
    start_time = time.time()
    for symbol in coins:
        try:
            trend = get_market_trend(symbol)
            price = get_price(symbol)
            send_signal(symbol, price, trend)
            print(f"✅ Signal sent for {symbol}")
            time.sleep(180)  # 3 minutes delay per coin
        except Exception as e:
            print(f"⚠️ Error for {symbol}: {e}")
            time.sleep(10)
    elapsed = time.time() - start_time
    wait_time = 300 - elapsed  # Make sure 5 min gap between full round
    if wait_time > 0:
        print(f"⏳ Waiting {int(wait_time)}s before new round")
        time.sleep(wait_time)
