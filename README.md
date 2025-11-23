Personal Finance Tracker

This project is a command-line Personal Finance Tracker built in vanilla Python, along with a companion shell script for organizing and archiving expense files.
It demonstrates practical use of file I/O, data structures, user input validation, and shell scripting for automation.

Python Application (finance_tracker.py)

A menu based Personal Finance Tracker with the following features:

1. Check Remaining Balance

Reads current balance from balance.txt

Shows:

Current balance

Total expenses

Available balance

Allows adding more money to the balance

2. Add New Expense

Shows available balance before adding

Takes:

Date (YYYY-MM-DD)

Item name

Amount spent

Validates inputs and ID numbering

Saves entry into:
data/expenses_YYYY-MM-DD.txt

Updates balance and confirms success

3. View Expenses

Search options:

By item name

By amount

Return to main menu

4. Exit

Saves all data and closes the program.

Shell Script (archive_expenses.sh)

A small menu-driven script that manages archived expense files.

Features

Ensures archives/ directory exists

Copies all expenses_*.txt files from data/ to archives/

Logs every archive operation with timestamps in:
archives/archive_log.txt

Offers a search menu:

Search for archived files using a date (YYYY-MM-DD)

Prints file contents if found

Running the Programs

python3 finance_tracker.py

./archive_expenses.sh