import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

# ==========================
# PRODUCTS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    image TEXT,
    image2 TEXT,
    image3 TEXT,
    image4 TEXT,
    description TEXT
)
""")

# ==========================
# USERS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    phone TEXT UNIQUE,
    password TEXT
)
""")

# ==========================
# ORDERS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone TEXT,
    address TEXT,
    products TEXT,
    total INTEGER
)
""")

# ==========================
# SETTINGS
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY,
    site_name TEXT,
    banner_title TEXT,
    banner_text TEXT,
    phone TEXT,
    address TEXT,
    work_time TEXT,
    banner_image TEXT,
    logo_image TEXT
)
""")

cursor.execute("SELECT COUNT(*) FROM settings")

if cursor.fetchone()[0] == 0:
    cursor.execute("""
    INSERT INTO settings(
        id,
        site_name,
        banner_title,
        banner_text,
        phone,
        address,
        work_time,
        banner_image,
        logo_image
    )
    VALUES(
        1,
        'MyShop',
        '🔥 Bugungi Super Aksiya',
        '50 000 so''mdan yuqori buyurtmalarga bepul yetkazib berish 🚚',
        '+998 90 123 45 67',
        'Toshkent, O''zbekiston',
        '09:00 - 22:00',
        '',
        ''
    )
    """)

db.commit()
db.close()

print("✅ Database tayyor!")

