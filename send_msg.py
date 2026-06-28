import os
import requests
from datetime import datetime, timezone, timedelta

def send_telegram_message():
    # 這裡會自動讀取你剛剛在 Secrets 設定的值
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
 
     # 取得台灣時間 (UTC+8)新增
    taiwan_tz = timezone(timedelta(hours=8))
    now = datetime.now(taiwan_tz)
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")    
    
    # 你的訊息內容
    #message = "這是一則來自 GitHub Actions 的自動排程訊息！"

    # 訊息內容加入時間--新增
    message = f"GITHUB ACTION 自動排程通知\n現在時間: {time_str}"
    
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        #新增
        print(f"GITHUB ACTION 訊息發送成功: {time_str}")
      # print("訊息發送成功")
    else:
        print(f"GITHUB ACTION 發送失敗: {response.text}")

if __name__ == "__main__":
    send_telegram_message()
