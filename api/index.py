from flask import Flask, request, redirect, jsonify
import string, random

urls = {}  # In-memory storage (resets on cold start)

app = Flask(__name__)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url:
        return jsonify(error="No URL provided"), 400

    code = generate_code()
    urls[code] = long_url
    return jsonify(short_url=f"{request.host_url}{code}")

@app.route('/<code>')
def redirect_url(code):
    if code in urls:
        return redirect(urls[code])
    return 'Not found', 404

# Vercel serverless handler
def handler(event, context):
    return app(event, context)

app = app
