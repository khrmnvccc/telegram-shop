import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("PRAGMA table_info(settings)")
print(cursor.fetchall())

db.close()

