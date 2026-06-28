import os
import requests
import yfinance as yf
import pandas as pd
from flask import Flask
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

def calculate_kd(df, n=9):
    # KD 計算核心邏輯
    low_n = df['Low'].squeeze().rolling(window=n).min()
    high_n = df['High'].squeeze().rolling(window=n).max()
    rsv = (df['Close'].squeeze() - low_n) / (high_n - low_n) * 100
    
    k, d = [50.0], [50.0]
    for i in range(1, len(rsv)):
        val = rsv.iloc[i]
        if pd.isna(val):
            k.append(k[-1]); d.append(d[-1])
        else:
            k.append(2/3 * k[-1] + 1/3 * val)
            d.append(2/3 * d[-1] + 1/3 * k[-1])
    df['K'], df['D'] = k, d
    return df

@app.route('/', methods=['POST', 'GET'])
def run_bot():
    # 1. 計算資料
    ticker = '0050.TW'
    data = yf.download(ticker, start='2025-01-01', progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    df_kd = calculate_kd(data)
    
    # 2. 格式化訊息
    time_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    kd_str = df_kd[['Close', 'K', 'D']].tail(1).to_string()
    message = f"📊 cloud 0050 KD 排程通知\n時間: {time_str}\n\n```\n{kd_str}\n```"
    
    # 3. 發送至 Telegram
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(url, data=payload)
    return f"Status: {response.status_code}", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
