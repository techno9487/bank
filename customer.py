from person import Person
from account import Account
import time

class Customer(Person):

    def __init__(self, name, password, address = [None, None, None, None]):
        super().__init__(name, password, address)
        self.accounts = []

    def open_account(self):
        acc = Account(100,int(time.time()))
        self.accounts.append(acc)

    def get_account(self):
        return self.account

    def find_account(self,acc_no):
        for acc in self.accounts:
            if acc.get_account_no() == acc_no:
                return acc

        return None

    def transfer(self,bank,sender_acc_no, receiver_name, receiver_account_no, amount):
        acc = self.find_account(sender_acc_no)
        if acc == None:
            return "your accoutn doesn't exist"

        if acc.balance < amount:
            return "you don't have enough money to make this transaction"
        
        receiver = bank.search_customers_by_name(receiver_name)
        if receiver == None:
            return "Customer can't be found"

        receiver_acc = receiver.find_account(receiver_account_no)
        if receiver_acc == None:
            return "customer doesn't have account with that number"

        acc.balance = acc.balance-amount

        receiver_acc.balance = receiver_acc.balance+amount
    def save(self):
        obj = super().save()
        obj["accounts"] = []
        for acc in self.accounts:
            obj["accounts"].append(acc.save())

        return obj