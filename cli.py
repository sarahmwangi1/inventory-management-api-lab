import requests


BASE_URL = "http://127.0.0.1:5000"


def view_items():
    response = requests.get(f"{BASE_URL}/items")

    if response.status_code == 200:
        items = response.json()

        print("\n===== INVENTORY =====")

        if not items:
            print("Inventory is empty.")
            return

        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Category: {item['category']} | "
                f"Price: {item['price']} | "
                f"Quantity: {item['quantity']} | "
                f"Barcode: {item['barcode']}"
            )
    else:
        print("Error retrieving inventory.")


def view_item():
    item_id = input("Enter item ID: ")

    response = requests.get(
        f"{BASE_URL}/items/{item_id}"
    )

    if response.status_code == 200:
        item = response.json()

        print("\n===== ITEM =====")
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Category: {item['category']}")
        print(f"Price: {item['price']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Barcode: {item['barcode']}")

    else:
        print("Item not found.")


def add_item():
    print("\n===== ADD ITEM =====")

    name = input("Name: ")
    category = input("Category: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))
    barcode = input("Barcode: ")

    item = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "barcode": barcode
    }

    response = requests.post(
        f"{BASE_URL}/items",
        json=item
    )

    if response.status_code == 201:
        print("\nItem added successfully!")
        print(response.json())

    else:
        print("\nError adding item:")
        print(response.json())


def update_item():
    print("\n===== UPDATE ITEM =====")

    item_id = input("Enter item ID: ")

    print("Leave a field blank if you don't want to change it.")

    name = input("New name: ")
    category = input("New category: ")
    price = input("New price: ")
    quantity = input("New quantity: ")
    barcode = input("New barcode: ")

    data = {}

    if name:
        data["name"] = name

    if category:
        data["category"] = category

    if price:
        data["price"] = float(price)

    if quantity:
        data["quantity"] = int(quantity)

    if barcode:
        data["barcode"] = barcode

    if not data:
        print("No changes entered.")
        return

    response = requests.patch(
        f"{BASE_URL}/items/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("\nItem updated successfully!")
        print(response.json())

    else:
        print("\nError updating item:")
        print(response.json())


def delete_item():
    print("\n===== DELETE ITEM =====")

    item_id = input("Enter item ID: ")

    response = requests.delete(
        f"{BASE_URL}/items/{item_id}"
    )

    if response.status_code == 200:
        print("\nItem deleted successfully!")

    else:
        print("\nError deleting item:")
        print(response.json())


def search_product():
    print("\n===== SEARCH OPENFOODFACTS =====")

    barcode = input("Enter product barcode: ")

    response = requests.get(
        f"{BASE_URL}/search",
        params={"barcode": barcode}
    )

    if response.status_code == 200:
        product = response.json()

        print("\n===== PRODUCT FOUND =====")
        print(f"Product: {product['product_name']}")
        print(f"Brands: {product['brands']}")
        print(f"Categories: {product['categories']}")
        print(f"Quantity: {product['quantity']}")
        print(f"Barcode: {product['barcode']}")

    else:
        print("\nProduct not found.")


def import_product():
    print("\n===== IMPORT PRODUCT =====")

    barcode = input("Enter product barcode: ")

    response = requests.post(
        f"{BASE_URL}/import/{barcode}"
    )

    if response.status_code == 201:
        result = response.json()

        print("\nProduct imported successfully!")

        item = result["item"]

        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Category: {item['category']}")
        print(f"Price: {item['price']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Barcode: {item['barcode']}")

    else:
        print("\nProduct could not be imported.")
        print(response.json())


def main():
    print("\nWelcome to the Inventory Management System!")
    while True:
        print("\n")
        print("================================")
        print("   INVENTORY MANAGEMENT SYSTEM")
        print("================================")
        print("1. View all inventory")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search OpenFoodFacts")
        print("7. Import OpenFoodFacts product")
        print("8. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            view_items()

        elif choice == "2":
            view_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            search_product()

        elif choice == "7":
            import_product()

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()