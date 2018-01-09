
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
        def transfer(self,bank, receiver_name, receiver_account_no, amount):
                if self.balance < amount:
                        return "you don't have enough money to make this transaction"
                
                receiver = bank.search_customers_by_name(receiver_name)
                if receiver == None:
                        return "Customer can't be found"

                receiver_acc = receiver.find_account(receiver_account_no)
                if receiver_acc == None:
                        return "customer doesn't have account with that number"

                self.balance = acc.balance-amount
                receiver_acc.balance = receiver_acc.balance+amount


