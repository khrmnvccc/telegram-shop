from flask import Flask, render_template, session, redirect, request
from werkzeug.utils import secure_filename
import sqlite3
import os
import requests

from config import TOKEN, ADMIN_ID

app = Flask(__name__)
app.secret_key = "123456789"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

BOT_TOKEN = TOKEN
CHAT_ID = ADMIN_ID


# ==========================
# BOSH SAHIFA
# ==========================

@app.route("/")
def home():

    search = request.args.get("search", "")

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    # Mahsulotlarni olish
    if search:
        cursor.execute(
            "SELECT id, name, price, image FROM products WHERE name LIKE ?",
            ("%" + search + "%",)
        )
    else:
        cursor.execute(
            "SELECT id, name, price, image FROM products"
        )

    products = cursor.fetchall()

    # Sayt sozlamalari
    cursor.execute("""
        SELECT
            site_name,
            banner_title,
            banner_text,
            phone,
            address,
            work_time
            banner_image,
            logo_image
        FROM settings
        WHERE id=1
    """)

    settings = cursor.fetchone()

    db.close()

    cart_count = len(session.get("cart", []))

    return render_template(
        "index.html",
        products=products,
        cart_count=cart_count,
        settings=settings
    )


     
# ==========================
# SAVATCHA
# ==========================

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

    cart = {}
    total = 0

    for product_id in ids:

        cursor.execute(
            "SELECT id, name, price, image FROM products WHERE id=?",
            (product_id,)
        )

        product = cursor.fetchone()

        if product:

            if product[0] not in cart:

                cart[product[0]] = {
                    "id": product[0],
                    "name": product[1],
                    "price": product[2],
                    "image": product[3],
                    "count": 1
                }

            else:

                cart[product[0]]["count"] += 1

            total += int(product[2])

    db.close()

    return render_template(
        "cart.html",
        products=cart.values(),
        total=total
    )




@app.route("/remove/<int:product_id>")
def remove(product_id):

    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    session["cart"] = cart

    return redirect("/cart")

@app.route("/plus/<int:product_id>")
def plus(product_id):

    cart = session.get("cart", [])

    cart.append(product_id)

    session["cart"] = cart

    return redirect("/cart")


@app.route("/minus/<int:product_id>")
def minus(product_id):

    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    session["cart"] = cart

    return redirect("/cart")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

# ==========================
# ADMIN PANEL
# ==========================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            site_name,
            banner_title,
            banner_text,
            phone,
            address,
            work_time
        FROM settings
        WHERE id=1
    """)

    settings = cursor.fetchone()

    db.close()

    return render_template(
        "admin.html",
        settings=settings
    )

 
@app.route("/update_settings", methods=["POST"])
def update_settings():

    if not session.get("admin"):
        return redirect("/login")

    site_name = request.form["site_name"]
    banner_title = request.form["banner_title"]
    banner_text = request.form["banner_text"]
    phone = request.form["phone"]
    address = request.form["address"]
    work_time = request.form["work_time"]

    banner_image = request.files["banner_image"]
    logo_image = request.files["logo_image"]

    banner_path = None
    logo_path = None

    if banner_image.filename != "":
        banner_name = secure_filename(banner_image.filename)

        banner_image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                banner_name
            )
        )

        banner_path = "/static/uploads/" + banner_name

    if logo_image.filename != "":
        logo_name = secure_filename(logo_image.filename)

        logo_image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                logo_name
            )
        )

        logo_path = "/static/uploads/" + logo_name

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
        UPDATE settings
        SET
            site_name=?,
            banner_title=?,
            banner_text=?,
            phone=?,
            address=?,
            work_time=?,
            banner_image=?,
            logo_image=?
        WHERE id=1
    """, (
        site_name,
        banner_title,
        banner_text,
        phone,
        address,
        work_time,
        banner_path,
        logo_path
    ))

    db.commit()
    db.close()

    return redirect("/admin")


  

@app.route("/add_product", methods=["POST"])
def add_product():

    if not session.get("admin"):
        return redirect("/login")

    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]

    def save_image(file):
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return "/static/uploads/" + filename
        return None

    image1 = save_image(request.files.get("image"))
    image2 = save_image(request.files.get("image2"))
    image3 = save_image(request.files.get("image3"))
    image4 = save_image(request.files.get("image4"))

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
    INSERT INTO products(
        name,
        price,
        image,
        image2,
        image3,
        image4,
        description
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    name,
    price,
    image1,
    image2,
    image3,
    image4,
    description
))

    db.commit()
    db.close()

    return redirect("/")


@app.route("/delete/<int:product_id>")
def delete_product(product_id):

    if not session.get("admin"):
        return redirect("/login")

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

    if not session.get("admin"):
        return redirect("/login")

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, name, price, image, image2, image3, image4 FROM products WHERE id=?",
        (product_id,)
    )

    product = cursor.fetchone()

    db.close()
 
    return render_template("edit.html", product=product)


@app.route("/update/<int:product_id>", methods=["POST"])
def update_product(product_id):

    if not session.get("admin"):
        return redirect("/login")

    name = request.form["name"]
    price = request.form["price"]

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    image = request.files["image"]

    if image.filename != "":

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        image_path = "/static/uploads/" + filename

    else:

        cursor.execute(
            "SELECT image FROM products WHERE id=?",
            (product_id,)
        )

        image_path = cursor.fetchone()[0]

    cursor.execute(
        """
        UPDATE products
        SET name=?, price=?, image=?
        WHERE id=?
        """,
        (
            name,
            price,
            image_path,
            product_id
        )
    )

    db.commit()
    db.close()

    return redirect("/")



@app.route("/finish_order", methods=["POST"])
def finish_order():

    name = request.form["name"]
    phone = request.form["phone"]
    address = request.form["address"]

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    ids = session.get("cart", [])

    text = f"""🛒 Yangi buyurtma!

👤 Ism: {name}
📞 Telefon: {phone}
📍 Manzil: {address}

"""

    total = 0
    products_text = ""

    for product_id in ids:

        cursor.execute(
            "SELECT name, price FROM products WHERE id=?",
            (product_id,)
        )

        product = cursor.fetchone()

        if product:
            text += f"📦 {product[0]} - {product[1]} so'm\n"
            products_text += product[0] + ", "
            total += int(product[1])

    cursor.execute(
        """
        INSERT INTO orders(customer_name, phone, address, products, total)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            address,
            products_text,
            total
        )
    )

    db.commit()
    db.close()

    text += f"\n💰 Jami: {total} so'm"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print(response.status_code)
    print(response.text)

    session["cart"] = []

    return f"""
    <h2>✅ Rahmat, {name}!</h2>
    <p>Buyurtmangiz qabul qilindi.</p>
    <a href="/">🏠 Bosh sahifa</a>
    """


# ==========================
# LOGIN
# ==========================


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():

    fullname = request.form["fullname"]
    phone = request.form["phone"]
    password = request.form["password"]

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE phone=?",
        (phone,)
    )

    user = cursor.fetchone()

    if user:
        db.close()
        return "Bu telefon raqam allaqachon ro'yxatdan o'tgan!"

    cursor.execute(
        """
        INSERT INTO users(fullname, phone, password)
        VALUES (?, ?, ?)
        """,
        (
            fullname,
            phone,
            password
        )
    )

    db.commit()
    db.close()

    return redirect("/login")



@app.route("/login")
def login():
    return render_template("login.html")



@app.route("/login", methods=["POST"])
def login_post():

    username = request.form["username"]
    password = request.form["password"]

    # Admin
    if username == "admin" and password == "12345":
        session["admin"] = True
        return redirect("/admin")

    # Oddiy foydalanuvchi
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, fullname
        FROM users
        WHERE phone=? AND password=?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    db.close()

    if user:
        session["user_id"] = user[0]
        session["fullname"] = user[1]
        return redirect("/")

    return render_template(
    "login.html",
    error="❌ Telefon yoki parol noto'g'ri!"
)



@app.route("/orders")
def orders():

    if not session.get("admin"):
        return redirect("/login")

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("""
    SELECT customer_name, phone, address, products, total
    FROM orders
    ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    db.close()

    return render_template(
        "orders.html",
        orders=orders
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, fullname, phone
        FROM users
        WHERE id=?
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    db.close()

    return render_template(
        "profile.html",
        user=user
    )




@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# MAHSULOT SAHIFASI
# ==========================

@app.route("/product/<int:product_id>")
def product(product_id):

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(
    "SELECT id, name, price, image, image2, image3, image4, description FROM products WHERE id=?",
    (product_id,)
)

    product = cursor.fetchone()

    db.close()

    return render_template(
        "product.html",
        product=product
    )


# ==========================
# DASTURNI ISHGA TUSHIRISH
# ==========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )