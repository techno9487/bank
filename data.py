class Customer:
    def __init__(self,name,address,dob):
        self.name = name
        self.address = address
        self.dob = dob
        self.accounts = []

class Transaction:
    def __init__(self,id,amount,note):
        self.to = id
        self.amt = amount
        self.reason = note
        self.date = None

class Account:
    def __init__(self):
        self.balance = 0
        self.overdraftLimit = 0
        self.id = ""
        self.transactions = []