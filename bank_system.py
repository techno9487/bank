from customer import Customer
from admin import Admin
import os,json,os.path
from account import LoanRequest
	
class BankSystem(object):
    def __init__(self):
        self.data = {}
        self.customers = []
        self.admins = []
        self.loan_requests = []

        self.load_bank_data()
        
    #load bank data from disk
    def load_bank_data(self):
        if os.path.exists("data.json"):
            f = open("data.json","r")
            data = f.read()
            f.close()
            self.data = json.loads(data)

            self.load_customers()
            self.load_admins()
            self.load_requests()

    #load customers from the data
    def load_customers(self):
        for customer in self.data["customers"]:
            if customer == None:
                continue
            cus = Customer(None,None,None)
            cus.load(customer)
            print("Loaded customer: %s" % cus.get_name())
            self.customers.append(cus)

    #load admins from data
    def load_admins(self):
        for admin in self.data["admins"]:
            if admin == None:
                continue

            ad = Admin(None,None,None)
            ad.load(admin)
            self.admins.append(ad)

            print("Loaded admin: %s" % ad.get_name())

    #loads loan requests
    def load_requests(self):
        if "requests" not in self.data:
            return

        for req in self.data["requests"]:
            if req is None:
                continue

            acc = self.find_account(req["acc_no"])
            if acc is None:
                continue

            cus = self.search_customers_by_name(req["cus"])
            if cus is None:
                continue

            r = LoanRequest(req["amt"],acc,cus)
            self.loan_requests.append(r)

            print("Loaded loan request for %d" % acc.account_no)

    def remove_request(self,req):
        self.loan_requests.remove(req)
        self.save_bank_data()


    def find_account(self,acc_no):
        for c in self.customers:
            for a in c.get_accounts():
                if a.account_no == acc_no:
                    return a

        return None

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
        print("Created customer %s" % name)
        self.save_bank_data()
        return cus
    def remove_customer(self,customer):
        self.customers.remove(customer)
        self.save_bank_data()
        print("Closed account of %s" % customer.get_name())

    def get_loans(self):
        loans = []

        for c in self.customers:
            for a in c.get_accounts():
                if a.loan is not None:
                    loans.append(a.loan)
        return loans

    def admin_login(self, name, password):
        admin = self.search_admin_by_name(name)
        if admin == None:
            return None
        if admin.check_password(password) == False:
            return None

        return admin


    def search_admin_by_name(self, admin_name):
        for admin in self.admins:
            if admin.get_name() == admin_name:
                return admin
        return None

    def save_bank_data(self):
        customers_data = []
        for customer in self.customers:
            customers_data.append(customer.save())

        admnins_data = []
        for admin in self.admins:
            admnins_data.append(admin.save())

        requests = []
        for r in self.loan_requests:
            requests.append(r.save())

        data = json.dumps({
            "customers":customers_data,
            "admins":admnins_data,
            "requests":requests
        },indent=4)
        f = open("data.json","w")
        f.write(data)
        f.close()
    def dump_customers(self):
        for c in self.customers:
            if c == None:
                continue
            c.dump_info()