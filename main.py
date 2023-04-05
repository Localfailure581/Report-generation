import datetime
import os

import db
import models


def get_float_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    print("Welcome to funding report creator, a process created to generate funding reports based on user input via terminal")

    # Get the net income
    while True:
        income = get_float_input("How much did the parent company make this month? ")
        confirmation = input(f"Ok, so the server pulled in ${income:.2f}? [Y/N] ")
        if confirmation.upper() == "Y":
            break

    # Get the expenses
    expenses = []
    while True:
        expense_name = input("Enter an expense name (or 'done' if finished): ")
        if expense_name.lower() == "done":
            break
        expense_value = get_float_input(f"Enter the value for '{expense_name}': ")
        expenses.append(models.Expense(expense_name, expense_value))
        db.insert_expense(expense_name, expense_value)

    # Get the current savings
    while True:
        current_savings = get_float_input("How much is currently saved? ")
        if current_savings < 0:
            print("Invalid input. Please enter a non negative number.")
            continue
        break

    # Calculate the total expenses
    total_expenses = sum([expense.value for expense in expenses])

    # Calculate the amount used from savings
    amount_used = max(0, total_expenses - income)

    # Update the current savings
    current_savings -= amount_used

    # Save the current savings to the database
    db.insert_savings(current_savings)

    # Print the report
    report = (f"NVS February funding\n"
              f"+${income:.2f} incoming (patrons)\n"
              f"-${total_expenses:.2f} total expenses\n"
              f"Used from NVS savings: ${amount_used:.2f}\n"
              f"Current savings: ${current_savings:.2f}")
    print(report)

    # Save the report to a file with a timestamp in the file name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"archives/funding_report_{timestamp}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(report)

    # Move the report to the archives folder
    shutil.move(filename, "archives")