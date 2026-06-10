from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type):
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = datetime.now()
    
    def __str__(self):#__str__ controls what gets printed when you do print(object)
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} | {self.transaction_type} | {self.amount}"

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction(amount, "deposit"))
        print(f"Deposited {amount}. New balance: {self.balance}")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.transactions.append(Transaction(amount, "withdrawal"))
            print(f"Withdrew {amount}. New balance: {self.balance}")
    
    def get_balance(self):
        return self.balance
    
    def show_transactions(self):
        for t in self.transactions:
            print(t)

class SavingsAccount(Account):
    def __init__(self, name, balance, interest_rate):
        super().__init__(name, balance)
        self.interest_rate = interest_rate
    
    def apply_interest(self):
        interest = self.balance * self.interest_rate / 100
        self.balance += interest
        print(f"Interest applied: {interest}. New balance: {self.balance}")

# Test it
acc = Account("Tehreem", 5000)
acc.deposit(2000)
acc.withdraw(1000)
acc.show_transactions()

savings = SavingsAccount("Tehreem", 10000, 2)
savings.apply_interest()
