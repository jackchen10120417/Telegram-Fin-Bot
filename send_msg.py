import os
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta

def calculate_kd(df, n=9):
    low_n_series = df['Low'].squeeze().rolling(window=n).min()
    high_n_series = df['High'].squeeze().rolling(window=n).max()
    close_series = df['Close'].squeeze()
    rsv = (close_series - low_n_series) / (high_n_series - low_n_series) * 100
    
    k_values, d_values = [50.0], [50.0]
    for i in range(1, len(rsv)):
        current_rsv_value = rsv.iloc[i]
        if pd.isna(current_rsv_value):
            k_values.append(50.0); d_values.append(50.0)
        else:
            k = (2/3 * k_values[-1]) + (1/3 * current_rsv_value)
            d = (2/3 * d_values[-1]) + (1/3 * k)
            k_values.append(k); d_values.append(d)
    df['K'], df['D'] = k_values, d_values
    return df

def get_other_stock_prices(tickers):  # 個股
    result_lines = []
    for t in tickers:
        try:
            stock_data = yf.download(t, period='5d', progress=False)
            if isinstance(stock_data.columns, pd.MultiIndex):
                stock_data.columns = stock_data.columns.get_level_values(0)
            
            latest_close = stock_data['Close'].iloc[-1]
            prev_close = stock_data['Close'].iloc[-2]
            change = latest_close - prev_close
            change_pct = (change / prev_close) * 100
            
            arrow = "🔺" if change > 0 else ("🔻" if change < 0 else "➖")
            line = f"{t}: {latest_close:.2f} {arrow} {change:+.2f} ({change_pct:+.2f}%)"
            result_lines.append(line)
        except Exception as e:
            result_lines.append(f"{t}: 抓取失敗 ({e})")
    
    return "\n".join(result_lines)

def send_telegram_message():
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    # 1. 下載並計算 KD
    ticker = '0050.TW'
    other_tickers = ['2330.TW', '2454.TW', '0056.TW','00919.TW']  # 台積電、聯發科、高股息ETF、群益台灣精選高息  ---新增
    data = yf.download(ticker, start='2025-01-01', progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    df_kd = calculate_kd(data)
    
    # 2. 準備訊息內容
    taiwan_tz = timezone(timedelta(hours=8))
    time_str = datetime.now(taiwan_tz).strftime("%Y-%m-%d %H:%M:%S")
    kd_data_str = df_kd[['Close', 'K', 'D']].tail(10).to_string()
    
    other_stocks_str = get_other_stock_prices(other_tickers)   # 新增這行 個股
    
    #message = f"🚀 GITHUB ACTION 自動排程通知\n時間: {time_str}\n\n0050 KD指標 (近10日):\n{kd_data_str}"
    message = (                                                       #新增這行 個股  修改
        f"🚀 GITHUB ACTION 自動排程通知\n時間: {time_str}\n\n"
        f"0050 KD指標 (近10日):\n{kd_data_str}\n\n"
        f"📈 其他股票股價:\n{other_stocks_str}"
    )
    
    # 3. 發送
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print(f"發送成功: {time_str}")
    else:
        print(f"發送失敗: {response.text}")

if __name__ == "__main__":
    send_telegram_message()
