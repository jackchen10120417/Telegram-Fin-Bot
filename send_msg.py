import os
import requests

def send_telegram_message():
    # 這裡會自動讀取你剛剛在 Secrets 設定的值
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    # 你的訊息內容
    message = "這是一則來自 GitHub Actions 的自動排程訊息！"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("訊息發送成功")
    else:
        print(f"發送失敗: {response.text}")

if __name__ == "__main__":
    send_telegram_message()
