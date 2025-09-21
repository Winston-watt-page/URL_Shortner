import os
from flask import Flask, request, redirect, jsonify
import string, random

app = Flask(__name__)
urls = {}  # in-memory, will reset on cold start

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    if not long_url:
        return jsonify(error="No URL provided"), 400
    code = generate_code()
    urls[code] = long_url
    base_url = f"https://{os.environ.get('VERCEL_URL', 'localhost')}/"
    return jsonify(short_url=f"{base_url}{code}")

@app.route("/<code>")
def redirect_url(code):
    if code in urls:
        return redirect(urls[code])
    return "Not Found", 404
