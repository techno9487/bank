from customer import Customer
from admin import Admin
from account import Account


customers_list = []
admins_list = []

	
class BankSystem(object):
    def __init__(self):
        self.customers_list = []
        self.admins_list = []
        self.load_bank_data()


    def load_bank_data(self):
        pass


    def customer_login(self, name, password):
        #STEP A.1
        pass
        
    def search_customers_by_name(self, customer_name):
        #STEP A.2
        pass


    def transferMoney(self, sender_account, receiver_name, receiver_account_no, amount):
        pass                
    def admin_login(self, name, password):
        # STEP A.3
        pass


    def search_admin_by_name(self, admin_name):
        # STEP A.4
        pass


app = BankSystem()
app.run_main_option()
