
from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

PRODUCT_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://localhost:5001"
)

ORDER_URL = os.getenv(
    "ORDER_SERVICE_URL",
    "http://localhost:5002"
)

@app.route("/")
def home():
    try:
        products = requests.get(
            f"{PRODUCT_URL}/products",
            timeout=5
        ).json()
    except requests.RequestException:
        products = []

    return render_template("index.html", products=products)

@app.route("/health")
def health():
    return {"status": "Frontend service running"}

@app.route("/create-order/<int:product_id>")
def create_order(product_id):
    try:
        response = requests.post(
            f"{ORDER_URL}/orders",
            json={"product_id": product_id},
            timeout=5
        )
        return response.json(), response.status_code
    except requests.RequestException:
        return {"error": "Order service unavailable"}, 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
