# Verwende das offizielle Playwright‑Image mit bereits installierten Browsern
FROM mcr.microsoft.com/playwright:focal

WORKDIR /app

# Installiere nur deine Python‑Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest deines Codes
COPY . .

# Exponiere den Port
EXPOSE 5000

# Starte deine Flask‑App
CMD ["python", "app.py"]
