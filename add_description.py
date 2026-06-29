import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("ALTER TABLE products ADD COLUMN description TEXT")

db.commit()
db.close()

print("✅ Description qo'shildi")