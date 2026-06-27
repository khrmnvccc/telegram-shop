import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("DELETE FROM products")

cursor.execute("""
INSERT INTO products(name, price, image)
VALUES
('Erkaklar futbolkasi', '120000', 'https://picsum.photos/300?random=1')
""")

cursor.execute("""
INSERT INTO products(name, price, image)
VALUES
('Ayollar ko'ylagi', '250000', 'https://picsum.photos/300?random=2')
""")

cursor.execute("""
INSERT INTO products(name, price, image)
VALUES
('Jinsi shim', '320000', 'https://picsum.photos/300?random=3')
""")

db.commit()
db.close()

print("3 ta mahsulot qo'shildi!")