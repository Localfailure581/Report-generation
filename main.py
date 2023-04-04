import sqlite3

def close_all_connections():
    for conn in sqlite3._connections.values():
        conn.close()
    sqlite3.close_all()

# Get the net income
while True:
    print("Welcome to funding report creator, a process created to generate funding reports based on user input via terminal")
    income = input("How much did the parent company make this month? ")
    try:
        income = float(income)
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Confirm the net income
while True:
    confirmation = input(f"Ok, so the server pulled in ${income:.2f}? [Y/N] ")
    if confirmation.upper() == "Y":
        break

# Get the expenses
while True:
    expense_name = input("Enter an expense name (or 'done' if finished): ")
    if expense_name.lower() == "done":
        break
    expense_value = input(f"Enter the value for '{expense_name}': ")
    try:
        expense_value = float(expense_value)
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    with sqlite3.connect('expenses.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, name TEXT, value REAL)')
        conn.execute('INSERT INTO expenses (name, value) VALUES (?, ?)', (expense_name, expense_value))

# Get the current savings
while True:
    current_savings = input("How much is currently saved? ")
    try:
        current_savings = float(current_savings)
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# Calculate the total expenses
with sqlite3.connect('expenses.db') as conn:
    expenses = conn.execute('SELECT name, value FROM expenses').fetchall()
total_expenses = sum([expense[1] for expense in expenses])

# Calculate the amount used from savings
amount_used = max(0, total_expenses - income)

# Update the current savings
current_savings -= amount_used

# Save the current savings to the database
with sqlite3.connect('expenses.db') as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS savings (id INTEGER PRIMARY KEY, value REAL)')
    conn.execute('INSERT INTO savings (value) VALUES (?)', (current_savings,))

# Print the report
print(f"NVS February funding\n"
      f"+${income:.2f} incoming (patrons)\n"
      f"-${total_expenses:.2f} total expenses\n"
      f"Used from NVS savings: ${amount_used:.2f}\n"
      f"Current savings: ${current_savings:.2f}")

# clear the contents of the tables and close all connections
with sqlite3.connect('expenses.db') as conn:
    conn.execute('DELETE FROM expenses')
    conn.execute('DELETE FROM savings')
conn.close()