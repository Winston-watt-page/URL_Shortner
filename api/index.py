import string, random
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

urls = {}  # In-memory storage

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    if not long_url:
        return jsonify(error="No URL provided"), 400

    code = generate_code()
    while code in urls:
        code = generate_code()

    urls[code] = long_url
    base_url = f"https://{request.host}/"
    return jsonify(short_url=f"{base_url}{code}")

@app.route("/<code>")
def redirect_url(code):
    if code in urls:
        return redirect(urls[code])
    return "URL not found", 404
