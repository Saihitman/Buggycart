"""Business logic for the product search feature."""


def search_products(products, query="", max_price=None):
    """Return products matching the supplied search filters.

    BUG INTENTIONALLY INTRODUCED:
    The query uses startswith() instead of checking whether the query appears
    anywhere in the product name. A search for "keyboard" works, but a search
    for "ical" incorrectly returns no result.
    """
    normalized_query = query.strip().lower()

    results = [
        product for product in products
        if not normalized_query
        or product["name"].lower().startswith(normalized_query)
    ]

    if max_price is not None:
        results = [product for product in results if product["price"] <= max_price]

    return results
