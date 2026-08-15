inventory = [
    {
        "id": 1,
        "name": "Milk",
        "category": "Dairy",
        "price": 120.00,
        "quantity": 20,
        "barcode": "123456789"
    },
    {
        "id": 2,
        "name": "Bread",
        "category": "Bakery",
        "price": 80.00,
        "quantity": 15,
        "barcode": "987654321"
    }
]


def get_next_id():
    if not inventory:
        return 1

    return max(item["id"] for item in inventory) + 1