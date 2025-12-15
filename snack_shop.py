# ======================================================
# SNACKY – SWIGGY-STYLE SNACK SHOP (LOGIN-FIRST)
# Customer UI + Admin Partner Dashboard
# Login Screen FIRST (Skip option)
# Swiggy-style Checkout UI
# Handling Fee: ₹15 (FREE above ₹100)
# ======================================================

from flask import Flask, request, redirect, url_for, session, render_template_string
from datetime import datetime

app = Flask(__name__)
app.secret_key = "snacky-super-secret"

# ---------------- PRODUCTS ----------------
products = {
    1: {"name": "Lays", "price": 20, "img": "https://i.imgur.com/Wz4FQzC.png", "cat": "chips"},
    2: {"name": "Kurkure", "price": 20, "img": "https://i.imgur.com/9XnQZQZ.png", "cat": "chips"},
    3: {"name": "Too Yumm", "price": 25, "img": "https://i.imgur.com/yX5JQyE.png", "cat": "chips"},
    4: {"name": "Frooti", "price": 30, "img": "https://i.imgur.com/6tF5Y8E.png", "cat": "drinks"},
    5: {"name": "Appy Fizz", "price": 35, "img": "https://i.imgur.com/Hm0mK5M.png", "cat": "drinks"},
    6: {"name": "Bisleri Water", "price": 20, "img": "https://i.imgur.com/0hQZ6xP.png", "cat": "water"},
}

orders = []
ADMIN_PASS = "admin123"

# ---------------- HELPERS ----------------
def cart_total():
    total = sum(products[int(pid)]["price"] * qty for pid, qty in session.get("cart", {}).items())
    handling = 0 if total >= 100 else 15
    return total, handling

# ---------------- LOGIN FIRST ----------------
@app.route("/", methods=["GET","POST"])
def login_first():
    if request.method == "POST":
        if request.form.get("skip"):
            session['user'] = 'Guest'
            return redirect('/home')
        session['user'] = request.form['name']
        return redirect('/home')

    html = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Welcome to Snacky</title>
<style>
body{margin:0;font-family:-apple-system;background:#fc8019;color:white;display:flex;align-items:center;justify-content:center;height:100vh}
.box{background:white;color:black;border-radius:18px;padding:24px;width:90%;max-width:360px;text-align:center}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #ccc;margin-bottom:12px}
button{width:100%;padding:12px;border:none;border-radius:14px;background:#fc8019;color:white;font-size:16px;font-weight:800}
.skip{margin-top:10px;background:#eee;color:#333}
</style>
</head>
<body>
<div class="box">
<h2>Snacky 🍔</h2>
<p>Login to continue</p>
<form method="post">
<input name="name" placeholder="Your name" required>
<button>Continue</button>
</form>
<form method="post">
<input type="hidden" name="skip" value="1">
<button class="skip">Skip for now</button>
</form>
</div>
</body>
</html>
'''
    return render_template_string(html)

# ---------------- CUSTOMER HOME ----------------
@app.route("/home")
def home():
    session.setdefault("cart", {})
    total_qty = sum(session["cart"].values())

    html = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Snacky</title>
<style>
body{margin:0;font-family:-apple-system;background:#f5f5f5}
.header{background:white;padding:14px;font-size:22px;font-weight:800}
.banner{margin:12px;background:#ffe6d5;color:#d35400;padding:10px;border-radius:12px;font-weight:700}
.cats{display:flex;gap:10px;padding:10px;overflow-x:auto}
.cat{background:white;padding:8px 14px;border-radius:20px;box-shadow:0 2px 6px rgba(0,0,0,.1);font-weight:700}
.cards{padding-bottom:90px}
.card{background:white;margin:12px;border-radius:18px;box-shadow:0 4px 12px rgba(0,0,0,.08);display:flex;padding:12px;align-items:center}
.card img{width:80px;height:80px;border-radius:14px;object-fit:cover;margin-right:12px}
.name{font-size:18px;font-weight:800}
.price{color:#555}
.add{margin-left:auto}
.add a,.add button{background:#fc8019;color:white;border:none;border-radius:18px;padding:6px 14px;font-weight:800}
.qty{display:flex;align-items:center;gap:8px}
.qty button{width:28px;height:28px;border-radius:50%}
.cartbar{position:fixed;bottom:0;width:100%;background:#fc8019;color:white;padding:14px;text-align:center;font-size:18px;font-weight:800}
</style>
<script>
function filter(cat){document.querySelectorAll('.card').forEach(c=>{c.style.display=(cat=='all'||c.dataset.cat==cat)?'flex':'none';})}
</script>
</head>
<body>
<div class="header">Snacky</div>
<div class="banner">🎉 Free handling above ₹100</div>
<div class="cats">
  <div class="cat" onclick="filter('all')">All</div>
  <div class="cat" onclick="filter('chips')">🥔 Chips</div>
  <div class="cat" onclick="filter('drinks')">🥤 Drinks</div>
  <div class="cat" onclick="filter('water')">💧 Water</div>
</div>
<div class="cards">
{% for id,p in products.items() %}
<div class="card" data-cat="{{p.cat}}">
<img src="{{p.img}}">
<div>
<div class="name">{{p.name}}</div>
<div class="price">₹{{p.price}}</div>
</div>
<div class="add">
{% if cart.get(id|string) %}
<div class="qty">
<a href="/dec/{{id}}"><button>-</button></a>
{{cart[id|string]}}
<a href="/add/{{id}}"><button>+</button></a>
</div>
{% else %}
<a href="/add/{{id}}">ADD</a>
{% endif %}
</div>
</div>
{% endfor %}
</div>
{% if total_qty>0 %}
<a href="/checkout" style="text-decoration:none"><div class="cartbar">{{total_qty}} items • View Cart</div></a>
{% endif %}
</body>
</html>
'''
    return render_template_string(html, products=products, cart=session["cart"], total_qty=total_qty)

# ---------------- CART ACTIONS ----------------
@app.route("/add/<pid>")
def add(pid):
    cart = session.get("cart", {})
    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart
    return redirect(url_for('home'))

@app.route("/dec/<pid>")
def dec(pid):
    cart = session.get("cart", {})
    if pid in cart:
        cart[pid] -= 1
        if cart[pid] <= 0:
            del cart[pid]
    session["cart"] = cart
    return redirect(url_for('home'))

# ---------------- CHECKOUT (SWIGGY STYLE) ----------------
@app.route("/checkout")
def checkout():
    total, handling = cart_total()
    html = '''
<h2 style="padding:16px">Checkout</h2>
<div style="padding:16px">
{% for pid,qty in cart.items() %}
<p>{{products[pid|int].name}} × {{qty}}</p>
{% endfor %}
<hr>
<p>Item Total: ₹{{total}}</p>
<p>Handling Fee: ₹{{handling}}</p>
<h3>To Pay: ₹{{total+handling}}</h3>
<a href="/place" style="background:#fc8019;color:white;padding:12px 20px;border-radius:14px;display:inline-block">Place Order</a>
</div>
'''
    return render_template_string(html, cart=session["cart"], products=products, total=total, handling=handling)

@app.route("/place")
def place():
    total, handling = cart_total()
    orders.append({"user": session.get('user'), "items": dict(session["cart"]), "total": total+handling})
    session["cart"] = {}
    return "Order placed successfully 🎉"

# ---------------- ADMIN PARTNER ----------------
@app.route("/partner", methods=["GET","POST"])
def partner():
    if request.method=="POST" and request.form.get("pass")==ADMIN_PASS:
        session["admin"]=True
    if not session.get("admin"):
        return '<form method="post"><input type="password" name="pass"><button>Login</button></form>'
    return render_template_string('<h2>Orders</h2>{% for o in orders %}<div style="background:#fff;padding:10px;margin:10px;border-radius:12px">{{o}}</div>{% endfor %}', orders=orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
