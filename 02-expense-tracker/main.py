import csv
def add():
    try:
      open("expenses.csv", "r")
    except FileNotFoundError:
      with open("expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["amount", "category"]) #once file created with these row headers
    amount=int(input("Enter amount: "))
    category= input("Enter category: ")
    with open("expenses.csv", "a", newline="") as f:
       writer = csv.writer(f)
       writer.writerow([amount, category])

def view():
    with open("expenses.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            print(f"Amount: {row[0]} | Category: {row[1]}")

def totals():
    totals = {}
    with open("expenses.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[1] in totals:# checking for each row, if category in totals
               totals[row[1]] += int(row[0])
            else:
               totals[row[1]] = int(row[0])
        for category, amount in totals.items():
            print(f"{category}: {amount}")

def main():
    while True:
        print("\n1. Add expense")
        print("2. View all expenses")
        print("3. View totals by category")
        print("4. Quit")
        choice = int(input("Enter choice: "))
        if choice == 1:
            add()
        elif choice == 2:
            view()
        elif choice == 3:
            totals()
        elif choice == 4:
            break

main()
