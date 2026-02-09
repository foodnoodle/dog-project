FROM python:3.12-slim

# 安裝 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 複製環境定義檔案
COPY pyproject.toml uv.lock ./

# 使用 uv 同步依賴 (不建立虛擬環境，直接裝在系統中以簡化容器邏輯)
RUN uv pip install --system -r pyproject.toml

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]