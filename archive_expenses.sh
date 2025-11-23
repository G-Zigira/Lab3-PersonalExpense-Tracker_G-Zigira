#!/bin/bash

BASE_DIR="$(dirname "$0")"
DATA_DIR="$BASE_DIR/data"
ARCHIVE_DIR="$BASE_DIR/archives"
LOG_FILE="$ARCHIVE_DIR/archive_log.txt"

# this is a checker for the  archives directory

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
fi

# this function is to  copy all expense files to archives

copy_expenses() {
    EXPENSE_FILES=("$DATA_DIR"/expenses_*.txt)

    if [ ! -e "${EXPENSE_FILES[0]}" ]; then
        echo "There were no  expense files found in $DATA_DIR."
        return
    fi

    for file in "${EXPENSE_FILES[@]}"; do
        cp "$file" "$ARCHIVE_DIR/"
    done


    echo "$(date '+%Y-%m-%d %H:%M:%S') Copied all expense files to archives" >> "$LOG_FILE"
    echo "All the expense files were copied to the archives directory successfully"
}

# this is the search function that uses date

search_archive() {
    read -p "Please enter the date  of the file you wish to search (YYYY-MM-DD): " SEARCH_DATE

    FILE="$ARCHIVE_DIR/expenses_$SEARCH_DATE.txt"

    if [ -f "$FILE" ]; then
        echo "Showing archived expenses for $SEARCH_DATE:"
        echo "+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_"
        cat "$FILE"
        echo "+_+_+_+_+_+_++_+_+_+_+_+_+_+_+_+_+_+_+_+_+_"
    else
        echo "there were no archived files found for $SEARCH_DATE."
    fi
}


echo "+_+_+_+_+_+Expense Archive System+_+_+_+_+_+_+__"
echo "1. Do you Search for an archived expense file"
echo "2. Exit"
echo "============================================"

read -p "Choose an option (1-2): " OPTION

copy_expenses
       

case $OPTION in
    1)
    search_archive
        ;;
        
    2)
    echo "Goodbye!"
        exit 0
        ;;
        
    *)
        echo "Invalid option."
        ;;
esac
