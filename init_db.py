import sqlite3

conn = sqlite3.connect('users.db')

print("Opened database successfully")
conn.execute('CREATE TABLE users (name TEXT, email TEXT, password TEXT, phone TEXT, age TEXT)')

