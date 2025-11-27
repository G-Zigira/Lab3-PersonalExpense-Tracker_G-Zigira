#!/usr/bin/env python3

from pathlib import Path
import csv
from datetime import datetime
import glob
import sys


DATA_DIR = Path("data")
BALANCE_FILE = DATA_DIR / "balance.txt"
ARCHIVE_LOG = DATA_DIR / "archive_log.txt"



# this is a function i used to make sure the data directory exists

def ensure_data_dir():
    
    DATA_DIR.mkdir(exist_ok=True)



#this function is the one responsible for getting the balance from the balance.txt and converting it to a string if the balance file exists

def read_balance():
    
    if not BALANCE_FILE.exists():
        return None
    
    try:
        text = BALANCE_FILE.read_text().strip()
        return float(text) if text else None
    
    except Exception:
        return None




#this function is what updates teh balance 

def write_balance(amount: float):
    
    BALANCE_FILE.write_text(f"{amount:.2f}\n")



#this is a function i made for when there is no value in the balace file and the user can set a value

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




#this is a function that returns a sorted lisgt of all files that start with expenses

def list_expense_files():
    
    pattern = str(DATA_DIR / "expenses_*.txt")
    return sorted(glob.glob(pattern))



# this function parses an expense line into a dictionary
#parsing is like organising data into a more detalied format

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




#a simple function that adds all the expenses from all the expense files and returns the total

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


#this function shows the balance report and promts teh user to add more money

def display_balance_report():
    
    bal = read_balance()
    if bal is None:
        bal = initialize_balance_interactive()
    total_exp = sum_total_expenses()
    available = bal  
    
    print('\n' + '=' * 40)
    print('+_+_+_+_+_YOUR BALANCE REPORT_+_+_+_+_+')
    print('-' * 40)
    print(f'Your current balance is : {bal:.2f} frw')
    print(f'Your total expenses is : {total_exp:.2f} frw')
    print(f'The available balance is : {available:.2f} frw')
    print('=' * 40 + '\n')


    choice = input('Do you want to add money to your balance?  (y / n) : ').strip().lower()
    if choice == 'y':
        while True:
            amt = input('please enter the amountyou want to add: ').strip()
            try:
                v = float(amt)
                if v <= 0:
                    print('Sorry but the new amount must be a positive number')
                    continue
                new_bal = bal + v
                write_balance(new_bal)
                print(f'your balance has been updated, The  new balance is : {new_bal:.2f}')
                break
            
            except ValueError:
                print('Please enter a valid amount')




#this function is used to determine the next id number for an expense file

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



#this function collects user input for a new expense
#it also validates it ,saves it and updates teh balance.txtfile

def add_new_expense():
    
    bal = read_balance()
    if bal is None:
        bal = initialize_balance_interactive()

    total_exp = sum_total_expenses()
    available = bal

    print('\n' + '=' * 40)
    print(f'The available balance is: {available:.2f}')
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
                print('Sorry the amount must be a positive number')
                continue
            break
        
        except ValueError:
            print('Please enter a valid amount')

    
    print('\nYou entered :')
    print(f'Date : {date_in}')
    print(f'Expense : {item}')
    print(f'Amount : {amt:.2f}')
    confirm = input('Do you want to save this expense? (y/n): ').strip().lower()
    if confirm != 'y':
        print('The new expense has been discarded, now returning to the main menu')
        return


    if amt > available:
        print('the balance you have is insufficient therefore we cannot save the expense')
        return


    fname = DATA_DIR / f'expenses_{date_in}.txt'
    eid = next_id_for_file(fname)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    try:
        with open(fname, 'a', newline='') as f:
            line = f'{eid},{timestamp},{item},{amt:.2f}\n'
            f.write(line)
    except Exception as e:
        print('we failed to save expense:', e)
        return


    new_bal = available - amt
    write_balance(new_bal)
    print(f'The expense was saved with ID {eid} the remaining balance is: {new_bal:.2f}')



#this function searches for an expense across all expense files by using its name
#bye teh way its case insensitive

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



#this function searches for an expense across all expense files by using the amount

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




#this function holds the menu for expense searching

def view_expenses_menu():
    
    while True:
        print('\nVIEW EXPENSES')
        print('1) Search by use of expense name')
        print('2) Search by use of expense amount')
        print('3) Go back to the main menu')
        
        choice = input('Choose an option from (1-3) : ').strip()
        if choice == '1':
            q = input('Enter the expense name to search (it will be case insensitive) : ').strip()
            
            if not q:
                print('this segment cant be empty please enter something')
                continue
            res = search_by_item(q)
            if not res:
                print('there were no matching records found')
            else:
                print(f'Found {len(res)} record(s):')
                for fname, e in res:
                    print(f'[{fname}] ID:{e["id"]} {e["timestamp"]} {e["item"]} {e["amount"]:.2f}')
        elif choice == '2':
            q = input('plwase enter the amount of teh expense : ').strip()
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


#this function holds the main menu that runs the entoire app

def main_menu():
    ensure_data_dir()
    while True:
        print('\n' + '*' * 48)
        print('Welcome to your Personal Expense Tracker')
        print('*' * 48)
        print('1) Check the remaining balance')
        print('2) View all your expenses')
        print('3) Add a new expense')
        print('4) Exit')
        print('*' * 48)
        choice = input('Choose an option from (1-4): ').strip()
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
            print('your selection was invalid , please choose between  1 and 4')



#this block of code makes it so that the app can only be ran by the main file and not imported
# it also allows a safe exit with Control + C

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nInterrupted. Exiting the app')
        sys.exit(0)


