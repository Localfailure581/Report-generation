import sqlite3

def create_expenses_table():
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, name TEXT, value REAL)')

def insert_expense(name, value):
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('INSERT INTO expenses (name, value) VALUES (?, ?)', (name, value))

def get_expenses():
    with sqlite3.connect('expenses.db') as conn:
        expenses = conn.execute('SELECT name, value FROM expenses').fetchall()
    return expenses

def create_savings_table():
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS savings (id INTEGER PRIMARY KEY, value REAL)')

def insert_savings(value):
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('INSERT INTO savings (value) VALUES (?)', (value,))