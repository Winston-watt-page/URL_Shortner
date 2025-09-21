import sqlite3, string, random, os
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# ✅ Create database folder dynamically
os.makedirs("database", exist_ok=True)
DB_PATH = "database/urls.db"

# ✅ SQLite connection
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS urls (
    code TEXT PRIMARY KEY,
    long_url TEXT NOT NULL
)
""")
conn.commit()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/shorten", methods=["POST"])
def shorten():
    try:
        data = request.get_json()
        long_url = data.get("url")
        if not long_url:
            return jsonify(error="No URL provided"), 400

        code = generate_code()
        while c.execute("SELECT 1 FROM urls WHERE code=?", (code,)).fetchone():
            code = generate_code()

        c.execute("INSERT INTO urls (code, long_url) VALUES (?, ?)", (code, long_url))
        conn.commit()

        base_url = f"https://{os.environ.get('VERCEL_URL', 'localhost')}/"
        return jsonify(short_url=f"{base_url}{code}")

    except Exception as e:
        # ✅ Print error for debugging
        print("ERROR:", e)
        return jsonify(error=str(e)), 500

@app.route("/<code>")
def redirect_url(code):
    row = c.execute("SELECT long_url FROM urls WHERE code=?", (code,)).fetchone()
    if row:
        return redirect(row[0])
    return "URL not found", 404
