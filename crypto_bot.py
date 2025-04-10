import requests
from telegram import Bot
import time

TELEGRAM_BOT_TOKEN = '7592911950:AAFhKVnUjRyl7K6fH6DB9bLmtiU2MeAsjlc'
CHANNEL_ID = '@theCrypto_Industry'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

coins = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
    'ADAUSDT', 'AVAXUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT'
]

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    data = requests.get(url).json()
    return float(data['price'])

def get_market_trend(symbol):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=2'
    candles = requests.get(url).json()
    last_candle = candles[-2]
    open_price = float(last_candle[1])
    close_price = float(last_candle[4])
    return "BUY" if close_price > open_price else "SELL"

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

print("🤖 Bot is Live... Posting to Telegram")
while True:
    start_time = time.time()
    for symbol in coins:
        try:
            trend = get_market_trend(symbol)
            price = get_price(symbol)
            send_signal(symbol, price, trend)
            print(f"✅ Signal sent for {symbol}")
            time.sleep(180)
        except Exception as e:
            print(f"⚠️ Error for {symbol}:", e)
            time.sleep(10)
    elapsed = time.time() - start_time
    wait_time = 300 - elapsed
    if wait_time > 0:
        print(f"⏳ Waiting {int(wait_time)}s before new round")
        time.sleep(wait_time)
