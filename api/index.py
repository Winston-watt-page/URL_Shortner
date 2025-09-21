import json
import base64

def handler(request):
    path = request.path

    # 1️⃣ Shorten URL
    if path == "/api/index.py/shorten":
        try:
            body = request.json
            long_url = body.get("url")
            if not long_url:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "No URL provided"})
                }

            # Encode URL in Base64
            encoded = base64.urlsafe_b64encode(long_url.encode()).decode()
            base_url = f"https://{request.headers['host']}/api/index.py/go/"
            short_url = f"{base_url}{encoded}"

            return {
                "statusCode": 200,
                "body": json.dumps({"short_url": short_url})
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    # 2️⃣ Redirect short URL
    elif path.startswith("/api/index.py/go/"):
        encoded = path.split("/")[-1]
        try:
            long_url = base64.urlsafe_b64decode(encoded.encode()).decode()
            return {
                "statusCode": 302,
                "headers": {"Location": long_url}
            }
        except Exception:
            return {
                "statusCode": 400,
                "body": "Invalid or corrupted URL"
            }

    else:
        return {
            "statusCode": 404,
            "body": "Not found"
        }
