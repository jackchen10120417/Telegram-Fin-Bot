# 使用 Python 輕量映像檔
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製檔案並安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 設定環境變數 (Cloud Run 會自動帶入 PORT)
ENV PORT=8080

# 使用 Gunicorn 啟動 Flask 應用
# main:app 代表執行 main.py 中的 app 物件
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
