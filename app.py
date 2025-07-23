from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_praemie

app = Flask(__name__)
CORS(app)  # Erlaubt Cross-Origin Requests von deinem Webflow-Frontend

# Health‑Check für Render: liefert 200 OK für GET und HEAD auf "/"
@app.route('/', methods=['GET', 'HEAD'])
def health_check():
    return 'OK', 200

# Dein eigentlicher API‑Endpoint
@app.route('/run-bot', methods=['POST'])
def run_bot():
    data = request.get_json()
    price = scrape_praemie(
        profile  = data.get('profile'),
        datum    = data.get('datum'),
        fahrzeug = data.get('fahrzeug'),
        leasing  = data.get('leasing')
    )
    if price:
        return jsonify({ 'status': 'ok', 'price': price })
    else:
        return jsonify({ 'status': 'error', 'message': 'Preis nicht gefunden' }), 500

if __name__ == '__main__':
    # Bindet an alle Interfaces auf Port 5000
    app.run(host='0.0.0.0', port=5000)
