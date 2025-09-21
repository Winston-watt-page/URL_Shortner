import base64
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    if not long_url:
        return jsonify(error="No URL provided"), 400

    encoded = base64.urlsafe_b64encode(long_url.encode()).decode()
    base_url = f"https://{request.host}/"
    short_url = f"{base_url}go/{encoded}"
    return jsonify(short_url=short_url)

@app.route("/go/<encoded>")
def redirect_encoded(encoded):
    try:
        long_url = base64.urlsafe_b64decode(encoded.encode()).decode()
        return redirect(long_url)
    except Exception:
        return "Invalid or corrupted URL", 400
