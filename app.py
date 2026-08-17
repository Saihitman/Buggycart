from flask import Flask, render_template_string, request, redirect, url_for, session
from features.product_search.service import search_products

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory storage for cart items
PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 25.00},
    {"id": 2, "name": "Mechanical Keyboard", "price": 75.00}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BuggyCart - Shop</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .product { border-bottom: 1px solid #ccc; padding: 10px 0; }
        button { background: #28a745; color: white; border: none; padding: 8px 12px; cursor: pointer; border-radius: 4px; }
        .logout-btn { background: #dc3545; }
        .search-box { margin: 15px 0; }
        .search-box input { padding: 8px; width: 240px; }
        .empty { color: #777; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🛒 BuggyCart Store</h1>
        {% if 'username' in session %}
            <p>Welcome, <b id="welcomeUser">{{ session['username'] }}</b>! <a href="/logout"><button class="logout-btn">Logout</button></a></p>
            <h3>Shopping Cart: <span id="cartCount">{{ session.get('cart_count', 0) }}</span> items</h3>
            <h3>Total: $<span id="totalPrice">{{ "%.2f"|format(session.get('total_price', 0.0)) }}</span></h3>

            <hr>
            <h2>Find Products</h2>
            <form action="/search" method="GET" class="search-box">
                <input type="text" id="searchQuery" name="q" value="{{ search_query }}" placeholder="Search products">
                <input type="number" id="maxPrice" name="max_price" value="{{ max_price }}" placeholder="Max price" step="0.01" min="0">
                <button type="submit" id="searchBtn">Search</button>
            </form>

            {% if searched %}
                <p id="searchSummary">{{ search_results|length }} product(s) found.</p>
            {% endif %}

            {% if search_results %}
                {% for item in search_results %}
                    <div class="product">
                        <span><b>{{ item.name }}</b> - ${{ item.price }}</span>
                        <form action="/add-to-cart" method="POST" style="display:inline;">
                            <input type="hidden" name="product_id" value="{{ item.id }}">
                            <button type="submit" id="searchAddBtn{{ item.id }}">Add to Cart</button>
                        </form>
                    </div>
                {% endfor %}
            {% elif searched %}
                <p class="empty" id="noResults">No products matched your search.</p>
            {% endif %}

            <hr>
            <h2>All Products</h2>
            {% for item in products %}
                <div class="product">
                    <span><b>{{ item.name }}</b> - ${{ item.price }}</span>
                    <form action="/add-to-cart" method="POST" style="display:inline;">
                        <input type="hidden" name="product_id" value="{{ item.id }}">
                        <button type="submit" id="addBtn{{ item.id }}">Add to Cart</button>
                    </form>
                </div>
            {% endfor %}

            <hr>
            <h2>Checkout</h2>
            <form action="/apply-promo" method="POST">
                <input type="text" id="promoCode" name="promo" placeholder="Enter Promo Code">
                <button type="submit" id="applyPromoBtn">Apply Promo</button>
            </form>
            <p id="promoMsg" style="color: blue;">{{ session.get('promo_msg', '') }}</p>

        {% else %}
            <h2>Login</h2>
            <form action="/login" method="POST">
                <input type="text" id="username" name="username" placeholder="Username" required><br><br>
                <input type="password" id="password" name="password" placeholder="Password" required><br><br>
                <button type="submit" id="loginBtn">Login</button>
            </form>
            <p id="errorMsg" style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        products=PRODUCTS,
        search_results=[],
        search_query='',
        max_price='',
        searched=False,
        error=request.args.get('error', '')
    )


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    max_price_raw = request.args.get('max_price', '')

    try:
        max_price = float(max_price_raw) if max_price_raw else None
    except ValueError:
        max_price = None

    results = search_products(PRODUCTS, query, max_price)

    return render_template_string(
        HTML_TEMPLATE,
        products=PRODUCTS,
        search_results=results,
        search_query=query,
        max_price=max_price_raw,
        searched=True,
        error=''
    )


@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('username')
    pword = request.form.get('password')

    # 🐛 BUG #1: Accepts ANY password for 'user' instead of checking 'pass123'
    if uname == 'user' and pword == 'pass123':
        session['username'] = uname
        session['cart_count'] = 0
        session['total_price'] = 0.0
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index', error="Invalid Credentials"))


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    p_id = int(request.form.get('product_id'))
    product = next((p for p in PRODUCTS if p["id"] == p_id), None)

    if product:
        # 🐛 BUG #2: Increments cart count by 2 instead of 1
        session['cart_count'] = session.get('cart_count', 0) + 2
        session['total_price'] = session.get('total_price', 0.0) + product['price']

    return redirect(url_for('index'))


@app.route('/apply-promo', methods=['POST'])
def apply_promo():
    code = request.form.get('promo')
    if code == "DISCOUNT10":
        # 🐛 BUG #3: Adds $10 to total price instead of subtracting $10
        session['total_price'] = session.get('total_price', 0.0) + 10.00
        session['promo_msg'] = "Promo Code DISCOUNT10 Applied!"
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
