# Personal Expenses Tracker

This project is a command line Personal Expenseinance Tracker built in Python that has a companion shell script for organizing and archiving the expense files.

---

## Features

1) The program allows the user to check their remaining balance
2) Allows the user to view their expenses and the details of the said expenses
3) The app allows user to add money to their expenses
4) There app calculates the remaining balance after a new expense is added and the current balance before an expense is added
5) The app performs monetary calculations of the users finances
6) the app updates the balance after every succeful expense log
6) The app allows the user to add new expenses and review and search for old expenses
7) The app createes an archive directory where it stores expense and logs them by date

---

## How to run the app

1) Make sure you have Python  installed in your device.
2) Open the project folder in your terminal.
3) Run:

   ```bash
   python expenses-tracker.py
   ```
4) The app will automatically  start the menu.

5) if you want to run the bash script end the pyhton program and run.
6) Run:

   ```bash
   ./ archive_expenses.sh
   ```

---

## Project files


expenses-tracker.py      =+ This file holds the main menu and does all the calculations
archive_expenses.sh      =+ This file creates the archive directory and organises all the expenses
balance.txt              =+ This file contains the current balance of the user 

---
## Project structure

main_dir/
│
├── expenses-tracker.py
├── archive_expenses.sh
│
├── data/
│   ├── balance.txt
│   ├── expenses_2024-11-07.txt
│   ├── expenses_2024-11-08.txt
│   └── ... (more daily expense files)
│
└── archives/
    ├── archive_log.txt
    ├── expenses_2024-11-07.txt
    ├── expenses_2024-11-08.txt
    └── ... (archived expense files)


## License

This is a free opnsource project for education and good grades
