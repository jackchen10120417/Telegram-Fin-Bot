FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# 使用 Gunicorn 作為正式環境的伺服器
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
