FROM python:3.11-slim

WORKDIR /app

# 复制 requirements.txt 并安装依赖（提前复制以利用 Docker 缓存）
COPY ./app/requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["python", "ui.py"]
