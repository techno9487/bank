import datetime, random

class AccountAttributes:
        def __init__(self,type,intrest):
                self.type = type
                self.intrest = intrest

class Loan:
    def __init__(self,amt,account):
        self.amt_left = amt
        self.account = account

        now = datetime.datetime.now()
        self.due_date = now+datetime.timedelta(days=21)
        self.due_date = self.due_date.timestamp()
    def save(self):
        return {
            "amt_left":self.amt_left,
            "due_date":self.due_date
        }
    def load(self,obj):
        self.amt_left = obj["amt_left"]
        self.due_date = obj["due_date"]

class Account:
        def __init__(self, balance, account_no,attr,customer):
            self.balance = float(balance)
            self.account_no = account_no
            self.attr = attr
            self.loan = None
            self.customer = customer

        def deposit(self, amount):
                self.balance+=amount

        def get_balance(self):
                return self.balance

        def get_account_no(self):
                return self.account_no

        def take_loan(self,amt):
            if amt > 15000:
                return False

            chance = random.random()
            if chance >= 0.3:
                return False

            #loan approved
            self.loan = Loan(amt,self)
            self.balance += amt
            print("granted loan to %d for %.2f" % (self.account_no,amt))
            return True

        def payback_loan(self,amt):
            if amt > self.balance:
                return False

            #if paying it all off
            if amt >= self.loan.amt_left:
                amt = self.loan.amt_left
                self.balance -= amt
                self.loan = None
                return True

            #now if paying only a bit left
            self.loan.amt_left -= amt
            self.balance -= amt
            return True

        def save(self):
            obj = {
                    "balance":self.balance,
                    "acc_no":self.account_no,
                    "attr":{
                            "type":self.attr.type,
                            "intrest":self.attr.intrest
                    }
            }

            if self.loan != None:
                obj["loan"] = self.loan.save()

            return obj
        def load(self,obj):
            self.attr = AccountAttributes(None,None)

            self.balance = obj["balance"]
            self.account_no = obj["acc_no"]
            self.attr.intrest = obj["attr"]["intrest"]
            self.attr.type = obj['attr']['type']

            if "loan" in obj:
                self.loan = Loan(0,self)
                self.loan.load(obj["loan"])

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


