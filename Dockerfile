FROM python:3.10-slim

# System-Dependencies für Playwright
RUN apt-get update && \
    apt-get install -y wget gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 \
                       libcups2 libxkbcommon0 libxcomposite1 libxdamage1 \
                       libxrandr2 libasound2 libpangocairo-1.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
