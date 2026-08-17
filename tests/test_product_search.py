from features.product_search.service import search_products


def test_search_matches_partial_product_name():
    products = [
        {"id": 1, "name": "Wireless Mouse", "price": 25.00},
        {"id": 2, "name": "Mechanical Keyboard", "price": 75.00},
    ]

    results = search_products(products, "ical")

    # This test is expected to FAIL until the intentional bug is fixed.
    assert len(results) == 1
    assert results[0]["name"] == "Mechanical Keyboard"


def test_search_respects_max_price():
    products = [
        {"id": 1, "name": "Wireless Mouse", "price": 25.00},
        {"id": 2, "name": "Mechanical Keyboard", "price": 75.00},
    ]

    results = search_products(products, "", max_price=30)

    assert len(results) == 1
    assert results[0]["name"] == "Wireless Mouse"
