
class AccountAttributes:
        def __init__(self,type,intrest):
                self.type = type
                self.intrest = intrest

class Account:
        def __init__(self, balance, account_no,attr):
                self.balance = float(balance)
                self.account_no = account_no
                self.attr = attr

        def deposit(self, amount):
                self.balance+=amount

        def get_balance(self):
                return self.balance

        def get_account_no(self):
                return self.account_no

        def save(self):
                return {
                        "balance":self.balance,
                        "acc_no":self.account_no,
                        "attr":{
                                "type":self.attr.type,
                                "intrest":self.attr.intrest
                        }
                }
        def load(self,obj):

                self.attr = AccountAttributes(None,None)

                self.balance = obj["balance"]
                self.account_no = obj["acc_no"]
                self.attr.intrest = obj["attr"]["intrest"]
                self.attr.type = obj['attr']['type']
        def transfer(self,bank, receiver_name, receiver_account_no, amount):
                if self.balance < amount:
                        return "you don't have enough money to make this transaction"
                
                receiver = bank.search_customers_by_name(receiver_name)
                if receiver == None:
                        return "Customer can't be found"

                receiver_acc = receiver.find_account(receiver_account_no)
                if receiver_acc == None:
                        return "customer doesn't have account with that number"

                if receiver_acc.account_no == self.account_no:
                        return "your trying to transfer to&from the same account"

                self.balance = self.balance-amount
                print(self.balance)
                receiver_acc.balance = receiver_acc.balance+amount

                print("Transaction completed %.2f transfered from %d to %d balances are now %.2f and %.2f" % (amount,self.account_no,receiver_account_no,self.balance,receiver_acc.balance))

                #if no error return None
                return None


