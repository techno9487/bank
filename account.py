
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


