# Playwright‑Basis‑Image mit Browsern
FROM mcr.microsoft.com/playwright:focal

WORKDIR /app

# Installiere nur deine Python‑Dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest deines Codes
COPY . .

EXPOSE 5000
CMD ["python3", "app.py"]
