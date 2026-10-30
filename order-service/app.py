
from flask import Flask, jsonify, request
import os
import requests
import uuid

app = Flask(__name__)

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://localhost:5001"
)

orders = []

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Order service running"})

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    product_id = data.get("product_id")

    if product_id is None:
        return jsonify({"error": "product_id is required"}), 400

    try:
        response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{int(product_id)}",
            timeout=5
        )
    except requests.RequestException:
        return jsonify({"error": "Product service unavailable"}), 503

    if response.status_code == 404:
        return jsonify({"error": "Product not found"}), 404

    if not response.ok:
        return jsonify({"error": "Product lookup failed"}), 502

    product = response.json()

    order = {
        "order_id": str(uuid.uuid4()),
        "product_id": product["id"],
        "product_name": product["name"],
        "price": product["price"],
        "status": "CREATED"
    }

    orders.append(order)

    return jsonify(order), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
