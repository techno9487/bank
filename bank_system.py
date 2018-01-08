from customer import Customer
from admin import Admin
import os,json,os.path
	
class BankSystem(object):
    def __init__(self):
        self.data = {}
        self.customers = []
        self.load_bank_data()
        
    #load bank data from disk
    def load_bank_data(self):
        if os.path.exists("data.json"):
            f = open("data.json","r")
            data = f.read()
            f.close()
            self.data = json.loads(data)

            self.load_customers()

    #load customers from the data
    def load_customers(self):
        for customer in self.data["customers"]:
            cus = Customer(None,None,None)
            cus.load(customer)
            self.customers.append(cus)

    def customer_login(self, name, password):
        #STEP A.1
        cus = self.search_customers_by_name(name)
        if cus == None:
            return False
 
        if cus.check_password(password) == False:
            return False

        return True
        
    #search for customer
    def search_customers_by_name(self, customer_name):
        #STEP A.2
        for customer in self.customers:
            if customer.get_name() == customer_name:
                return customer
        return None

    #create customer
    def create_customer(self,name,password,address):
        if self.search_customers_by_name(name) != None:
            return None

        cus = Customer(name,password,address)
        self.customers.append(cus)
        self.save_bank_data()
        return cus

    def admin_login(self, name, password):
        # STEP A.3
        pass


    def search_admin_by_name(self, admin_name):
        # STEP A.4
        pass

    def save_bank_data(self):
        customers_data = []
        for customer in self.customers:
            customers_data.append(customer.save())

        data = json.dumps({
            "customers":customers_data
        },indent=4)
        f = open("data.json","w")
        f.write(data)
        f.close()