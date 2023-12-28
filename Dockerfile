# 使用 Python 官方的 Docker 映像作為基礎映像
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製應用程式程式碼到映像中的 /app 資料夾
COPY . /app/

# 安裝所需套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放 FastAPI 應用程式使用的連接埠 (預設是 8000)
EXPOSE 25001

# 執行 FastAPI 應用程式
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "25000"]
