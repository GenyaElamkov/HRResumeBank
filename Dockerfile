FROM python:3.11-slim

# Не создает *.pyc файлы
ENV PYTHONDONTWRITEBYTECODE 1
# Не создает буфиризацию, логи показываются сразу
ENV PYTHONUNBUFFERED 1


WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    libpq-dev \
    nmap && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh
