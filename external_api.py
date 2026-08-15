import requests


OPENFOODFACTS_URL = "https://world.openfoodfacts.org/api/v2/product"

HEADERS = {
    "User-Agent": "InventoryManagementAPI/1.0 (student-project)"
}


def get_product_by_barcode(barcode):
    url = f"{OPENFOODFACTS_URL}/{barcode}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    return data.get("product")