FROM python:3.11-slim
LABEL authors="Angelina"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# Установка зависимостей Python и Liquibase
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    unzip && \
    pip install --no-cache-dir -r requirements.txt && \
    curl -L -o liquibase.zip https://github.com/liquibase/liquibase/releases/download/v4.23.1/liquibase-4.23.1.zip && \
    unzip liquibase.zip -d /opt/liquibase && \
    chmod +x /opt/liquibase/liquibase && \
    ln -s /opt/liquibase/liquibase /usr/local/bin/liquibase && \
    rm liquibase.zip && \
    curl -L -o /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000
