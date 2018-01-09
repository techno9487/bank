
class Account:
        def __init__(self, balance, account_no):
                self.balance = float(balance)
                self.account_no = account_no

        def deposit(self, amount):
                self.balance+=amount

        def get_balance(self):
                return self.balance

        def get_account_no(self):
                return self.account_no

        def save(self):
                return {
                        "balance":self.balance,
                        "acc_no":self.account_no
                }
        def load(self,obj):
                self.balance = obj["balance"]
                self.account_no = obj["acc_no"]


