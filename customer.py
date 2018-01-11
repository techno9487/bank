from person import Person
from account import Account
import time

class Customer(Person):

    def __init__(self, name, password, address = [None, None, None, None]):
        super().__init__(name, password, address)
        self.accounts = []

    def open_account(self,addr):
        acc = Account(100,int(time.time()),addr)
        self.accounts.append(acc)

    def get_accounts(self):
        return self.accounts

    def find_account(self,acc_no):
        for acc in self.accounts:
            if acc.get_account_no() == acc_no:
                return acc

        return None

        receiver_acc.balance = receiver_acc.balance+amount
    def save(self):
        obj = super().save()
        obj["accounts"] = []
        for acc in self.accounts:
            obj["accounts"].append(acc.save())

        return obj
    def load(self,obj):
        super().load(obj)
        accounts = obj["accounts"]
        for acc_data in accounts:
            acc = Account(acc_data["balance"],acc_data["acc_no"])
            self.accounts.append(acc)
    def dump_info(self):
        print("Name: %s" % self.name)

        addr = ""
        for a in self.address:
            addr += "%s\n" % a

        print("Address: %s" % addr)

        for a in self.accounts:
            print("Account Number: %d" % a.account_no)
            print("Balance: %.2f\n" % a.balance)
            print("Type: %s" % a.attr.type)
            print("Intrest: %.2f" % a.attr.intrest)


        print('------------------------------')