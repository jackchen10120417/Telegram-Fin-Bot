import os
import requests
from flask import Flask
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET']) # Cloud Scheduler 呼叫此網址
def run_bot():
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    taiwan_tz = timezone(timedelta(hours=8))
    now = datetime.now(taiwan_tz)
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")    
    message = f"自動排程通知\n現在時間: {time_str}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return f"Success: {time_str}", 200
    else:
        return f"Failed: {response.text}", 500

if __name__ == "__main__":
    # Cloud Run 會使用 gunicorn 啟動，這裡僅供本地測試
    app.run(host='0.0.0.0', port=8080)
