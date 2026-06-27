from flask import Flask, render_template, session, redirect, request 
import sqlite3
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "123456789"

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/")
def home():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("SELECT id, name, price, image FROM products")
    products = cursor.fetchall()

    print(products)

    db.close()

    return render_template("index.html", products=products)

@app.route("/add/<int:product_id>")
def add(product_id):

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    cart.append(product_id)
    session["cart"] = cart

    return redirect("/")

@app.route("/cart")
def show_cart():

    ids = session.get("cart", [])

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    products = []
    total = 0

    for product_id in ids:
        cursor.execute(
            "SELECT id, name, price, image FROM products WHERE id=?",
            (product_id,)
        )

        product = cursor.fetchone()

        if product:
            products.append(product)
            total += int(product[2])

    db.close()

    return render_template(
        "cart.html",
        products=products,
        total=total
    )
 
@app.route("/remove/<int:product_id>")
def remove(product_id):

    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    session["cart"] = cart

    return redirect("/cart")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/add_product", methods=["POST"])
def add_product():

    name = request.form["name"]
    price = request.form["price"]
    image = request.form["image"]

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO products(name, price, image)
        VALUES (?, ?, ?)
        """,
        (name, price, image)
    )

    db.commit()
    db.close()

    return redirect("/")

@app.route("/delete/<int:product_id>")
def delete_product(product_id):

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )

    db.commit()
    db.close()

    return redirect("/")

@app.route("/edit/<int:product_id>")
def edit_product(product_id):

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, name, price, image FROM products WHERE id=?",
        (product_id,)
    )

    product = cursor.fetchone()

    db.close()

    return render_template("edit.html", product=product)

@app.route("/update/<int:product_id>", methods=["POST"])
def update_product(product_id):

    name = request.form["name"]
    price = request.form["price"]
    image = request.form["image"]

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name=?, price=?, image=?
        WHERE id=?
        """,
        (name, price, image, product_id)
    )

    db.commit()
    db.close()

    return redirect("/")

@app.route("/finish_order", methods=["POST"])
def finish_order():

    name = request.form["name"]
    phone = request.form["phone"]
    address = request.form["address"]

    return f"""
    <h2>Rahmat, {name}!</h2>
    <p>Telefon: {phone}</p>
    <p>Manzil: {address}</p>
    """

@app.route("/order")
def order():

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    ids = session.get("cart", [])

    text = "🛒 Yangi buyurtma!\n\n"
    total = 0

    for product_id in ids:
        cursor.execute(
            "SELECT name, price FROM products WHERE id=?",
            (product_id,)
        )

        product = cursor.fetchone()

        if product:
            text += f"📦 {product[0]}\n"
            text += f"💰 {product[1]} so'm\n\n"
            total += int(product[1])

    db.close()

    text += f"💵 Jami: {total} so'm"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    session["cart"] = []

    return """
    <h1>✅ Buyurtmangiz qabul qilindi!</h1>
    <a href="/">🏠 Bosh sahifaga qaytish</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
