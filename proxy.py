from flask import Flask, jsonify, request
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://open.bymadata.com.ar/",
    "Origin": "https://open.bymadata.com.ar",
    "Accept": "application/json, text/plain, */*",
}

ENDPOINTS = {
    "acciones": "https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/leading-equity",
    "cedears":  "https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/cedears",
    "bonos":    "https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/government-bonds",
}

ALLOWED = ["open.bymadata.com.ar"]

@app.route("/market/<market>")
def get_market(market):
    if market not in ENDPOINTS:
        return jsonify({"error": f"Mercado desconocido: {market}"}), 400
    try:
        r = requests.get(ENDPOINTS[market], headers=HEADERS, timeout=10, verify=False)
        r.raise_for_status()
        return (r.content, r.status_code, {"Content-Type": "application/json"})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

@app.route("/proxy")
def proxy():
    url = request.args.get("url", "")
    if not url:
        return jsonify({"error": "Falta parametro url"}), 400
    if not any(domain in url for domain in ALLOWED):
        return jsonify({"error": "Dominio no permitido"}), 403
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        r.raise_for_status()
        return (r.content, r.status_code, {"Content-Type": "application/json"})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
