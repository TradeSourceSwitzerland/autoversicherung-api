# Playwright‑Basis‑Image mit passenden Browsern für Version 1.48.0
FROM mcr.microsoft.com/playwright:v1.48.0-focal

WORKDIR /app

# Installiere pip für Python3
USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Installiere nur deine Python‑Dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest deines Codes
COPY . .

# Exponiere den Port
EXPOSE 5000

# Starte deine Flask‑App
CMD ["python3", "app.py"]
