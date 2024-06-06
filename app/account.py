# creating getter and setter

class Account:
    def __init__(self,name,acc_id,balance):
        self.name = name
        self.acc_id = acc_id
        self.balance = balance
    
    def deposit(self,amount):
        # ensure deposity amount is positive
        if amount <= 0:
            raise ValueError("Deposit amount must be positive. A negative value means user will need to use withdraw")
        self.balance += amount
        return self.balance
        
    def withdraw(self,amount):  
        # ensure withdrawal amount is positive
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive. A negative value means user will need to use deposit")
        # ensure there is no overdraft. i.e, if user wants to withdraw more than its balance, the program will not allow
        if amount > self.balance:
            raise ValueError("Insufficient Fund. Withdrawal amount is larger than balance.")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance