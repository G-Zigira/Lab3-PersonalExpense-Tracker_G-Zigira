#!/usr/bin/env python3

from pathlib import Path
import csv
from datetime import datetime
import glob
import sys

DATA_DIR = Path("data")
BALANCE_FILE = DATA_DIR / "balance.txt"
ARCHIVE_LOG = DATA_DIR / "archive_log.txt"




def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)



def read_balance():
    if not BALANCE_FILE.exists():
        return None
    try:
        text = BALANCE_FILE.read_text().strip()
        return float(text) if text else None
    except Exception:
        return None






def write_balance(amount: float):
    BALANCE_FILE.write_text(f"{amount:.2f}\n")





def initialize_balance_interactive():
    print("There wa no initial balance found Let's set an initial balance")
    while True:
        val = input("Please enter the starting balance (eg: 150000frw): ").strip()
        try:
            v = float(val)
            if v < 0:
                print("Sorry the balance must be a non negative numberm try again")
                continue
            write_balance(v)
            print(f"the balance was set to: {v:.2f} frw")
            return v
        except ValueError:
            print("Please enter a valid number")






def list_expense_files():
    pattern = str(DATA_DIR / "expenses_*.txt")
    return sorted(glob.glob(pattern))





def parse_expense_line(line: str):
    
    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 4:
        return None
    
    try:
        return {
            "id": int(parts[0]),
            "timestamp": parts[1],
            "item": parts[2],
            "amount": float(parts[3])
        }
    except Exception:
        return None






def sum_total_expenses():
    total = 0.0
    for fname in list_expense_files():
        try:
            with open(fname, newline='') as f:
                for line in f:
                    e = parse_expense_line(line)
                    if e:
                        total += e['amount']
        except Exception:
            continue
    return total




def display_balance_report():
    bal = read_balance()
    if bal is None:
        bal = initialize_balance_interactive()
    total_exp = sum_total_expenses()
    available = bal  
    print('\n' + '=' * 40)
    print('YOUR BALANCE REPORT')
    print('-' * 40)
    print(f'Your Current balance : {bal:.2f} frw')
    print(f'tour Total expenses  : {total_exp:.2f} frw')
    print(f'Available balance    : {available:.2f} frw')
    print('=' * 40 + '\n')


    choice = input('Do you want to add money to your balance?  (y / n) : ').strip().lower()
    if choice == 'y':
        while True:
            amt = input('please enter the amount to add: ').strip()
            try:
                v = float(amt)
                if v <= 0:
                    print('The new amount must be a positive number')
                    continue
                new_bal = bal + v
                write_balance(new_bal)
                print(f'your balance has been updated, The  new balance is: {new_bal:.2f}')
                break
            except ValueError:
                print('Please enter a valid amount')






def next_id_for_file(path: Path):
    if not path.exists():
        return 1
    max_id = 0
    try:
        with open(path, newline='') as f:
            for line in f:
                e = parse_expense_line(line)
                if e and e['id'] > max_id:
                    max_id = e['id']
    except Exception:
        pass
    return max_id + 1




def add_new_expense():
    bal = read_balance()
    if bal is None:
        bal = initialize_balance_interactive()

    total_exp = sum_total_expenses()
    available = bal

    print('\n' + '=' * 40)
    print(f'The available balance: {available:.2f}')
    print('=' * 40)

    
    
    
    while True:
        date_in = input('Enter thw date (YYYY-MM-DD) : ').strip()
        try:
            dt = datetime.strptime(date_in, '%Y-%m-%d')
            break
        except ValueError:
            print('Sorry the date must be in format YYYY-MM-DD.')

    item = input('please enter the name of your expense : ').strip()
    
    if not item:
        print('the expense name cannot be empty, we shall return you to the main menu')
        return

    while True:
        amt_str = input('please enter amount paid for the expense: ').strip()
        try:
            amt = float(amt_str)
            if amt <= 0:
                print('Sorry the amount must be positive')
                continue
            break
        except ValueError:
            print('Please enter a valid amount')

    
    print('\nYou entered:')
    print(f'Date : {date_in}')
    print(f'Expense : {item}')
    print(f'Amount: {amt:.2f}')
    confirm = input('Save this expense? (y/n): ').strip().lower()
    if confirm != 'y':
        print('The new expense has been discarded, now returning to the main menu')
        return


    if amt > available:
        print('the balance is insufficient therefore we cannot save the expense')
        return

    # Save expense
    fname = DATA_DIR / f'expenses_{date_in}.txt'
    eid = next_id_for_file(fname)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Append CSV line
    try:
        with open(fname, 'a', newline='') as f:
            line = f'{eid},{timestamp},{item},{amt:.2f}\n'
            f.write(line)
    except Exception as e:
        print('we failed to save expense:', e)
        return

    # Update balance (subtract expense)
    new_bal = available - amt
    write_balance(new_bal)
    print(f'The expense saved with ID {eid} the remaining balance is: {new_bal:.2f}')


def search_by_item(name_query: str):
    name_query = name_query.lower()
    results = []
    for fname in list_expense_files():
        try:
            with open(fname, newline='') as f:
                for line in f:
                    e = parse_expense_line(line)
                    if e and name_query in e['item'].lower():
                        results.append((Path(fname).name, e))
        except Exception:
            continue
    return results


def search_by_amount(amount_query: float):
    results = []
    for fname in list_expense_files():
        try:
            with open(fname, newline='') as f:
                for line in f:
                    e = parse_expense_line(line)
                    if e and abs(e['amount'] - amount_query) < 0.0001:
                        results.append((Path(fname).name, e))
        except Exception:
            continue
    return results


def view_expenses_menu():
    while True:
        print('\nVIEW EXPENSES')
        print('1. Search by item name')
        print('2. Search by amount')
        print('3. Back to main menu')
        choice = input('Choose an option: ').strip()
        if choice == '1':
            q = input('Enter expense name to search (it will be case insensitive): ').strip()
            if not q:
                print('this segment cant be ')
                continue
            res = search_by_item(q)
            if not res:
                print('there were no matching records found.')
            else:
                print(f'Found {len(res)} record(s):')
                for fname, e in res:
                    print(f'[{fname}] ID:{e["id"]} {e["timestamp"]} {e["item"]} {e["amount"]:.2f}')
        elif choice == '2':
            q = input('plwase enter the amount to search (exact match): ').strip()
            try:
                amt = float(q)
            except ValueError:
                print('please enter a valid number.')
                continue
            res = search_by_amount(amt)
            if not res:
                print('there were no matching records found.')
            else:
                print(f'Found {len(res)} record(s):')
                for fname, e in res:
                    print(f'[{fname}] ID:{e["id"]} {e["timestamp"]} {e["item"]} {e["amount"]:.2f}')
        elif choice == '3':
            return
        else:
            print('the choice you picked was invalid .')


def main_menu():
    ensure_data_dir()
    while True:
        print('\n' + '*' * 48)
        print('Welcome to Personal Finance Tracker')
        print('1. Check Remaining Balance')
        print('2. View Expenses')
        print('3. Add New Expense')
        print('4. Exit')
        print('*' * 48)
        choice = input('Select an option (1-4): ').strip()
        if choice == '1':
            display_balance_report()
        elif choice == '2':
            view_expenses_menu()
        elif choice == '3':
            add_new_expense()
        elif choice == '4':
            print('Saving and exiting , thanks and goodbye')
            sys.exit(0)
        else:
            print('your selection was , please choose between  1 and 4.')


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting the app')
        sys.exit(0)


