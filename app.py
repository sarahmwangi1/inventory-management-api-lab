from flask import Flask, jsonify, request

from inventory import inventory, get_next_id
from external_api import get_product_by_barcode


app = Flask(__name__)


# HOME ROUTE
@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API is running!"
    })


# =========================
# CRUD ROUTES
# =========================

# GET all inventory items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(inventory)


# GET one inventory item
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({
        "error": "Item not found"
    }), 404


# CREATE a new inventory item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "name",
        "category",
        "price",
        "quantity",
        "barcode"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    new_item = {
        "id": get_next_id(),
        "name": data["name"],
        "category": data["category"],
        "price": data["price"],
        "quantity": data["quantity"],
        "barcode": data["barcode"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# UPDATE an inventory item
@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    for item in inventory:
        if item["id"] == item_id:

            if "name" in data:
                item["name"] = data["name"]

            if "category" in data:
                item["category"] = data["category"]

            if "price" in data:
                item["price"] = data["price"]

            if "quantity" in data:
                item["quantity"] = data["quantity"]

            if "barcode" in data:
                item["barcode"] = data["barcode"]

            return jsonify(item)

    return jsonify({
        "error": "Item not found"
    }), 404


# DELETE an inventory item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Item deleted successfully"
            })

    return jsonify({
        "error": "Item not found"
    }), 404


# =========================
# HELPER ROUTE
# =========================

# GET number of inventory items
@app.route("/items/count", methods=["GET"])
def get_item_count():
    return jsonify({
        "count": len(inventory)
    })


# =========================
# OPENFOODFACTS ROUTES
# =========================

# SEARCH OpenFoodFacts by barcode
@app.route("/search", methods=["GET"])
def search_product():
    barcode = request.args.get("barcode")

    if not barcode:
        return jsonify({
            "error": "Barcode is required"
        }), 400

    product = get_product_by_barcode(barcode)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify({
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "categories": product.get("categories"),
        "quantity": product.get("quantity"),
        "barcode": barcode,
        "image_url": product.get("image_url")
    })


# IMPORT OpenFoodFacts product into inventory
@app.route("/import/<barcode>", methods=["POST"])
def import_product(barcode):
    product = get_product_by_barcode(barcode)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    new_item = {
        "id": get_next_id(),
        "name": product.get("product_name", "Unknown Product"),
        "category": product.get("categories", "Unknown"),
        "price": 0,
        "quantity": 1,
        "barcode": barcode
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Product imported successfully",
        "item": new_item
    }), 201


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)