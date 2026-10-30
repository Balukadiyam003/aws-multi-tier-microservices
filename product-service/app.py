	
from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Mobile", "price": 25000},
    {"id": 3, "name": "Headphones", "price": 2000}
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Product service running"})

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or data.get("price") is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        price = float(data["price"])
        if price < 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price"}), 400

    new_product = {
        "id": max((p["id"] for p in products), default=0) + 1,
        "name": data["name"],
        "price": price
    }

    products.append(new_product)
    return jsonify(new_product), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

