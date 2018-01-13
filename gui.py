import tkinter as tk
from tkinter import ttk,messagebox
import logging
from bank_system import BankSystem
from account import AccountAttributes
from datetime import *

class MainAppliation(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.idLabel = tk.Label(self.parent,text="Name:",justify=tk.LEFT)
        self.idLabel.grid(column=0)

        self.e = ttk.Entry(self.parent,width=30)
        self.e.grid(row=0,column=1,columnspan = 5)

        pwdLabel = tk.Label(self.parent,text="Password:")
        pwdLabel.grid(row=1,column=0)

        self.pwd = ttk.Entry(self.parent,width=30,show='*')
        self.pwd.grid(row=1,column=1)

        login = ttk.Button(self.parent,text='Login',command=self.try_login)
        login.grid(row = 2,column=1,sticky=tk.E)

        register = ttk.Button(self.parent,text="Register",command=self.open_register)
        register.grid(row=2,column=1,sticky=tk.W)

        admin = ttk.Button(self.parent,text="Admin",command=self.open_admin)
        admin.grid(row=2,column=0)
    def open_admin(self):
        AdminLogin()
    def try_login(self):
        success = bank.customer_login(self.e.get(),self.pwd.get())
        if not success:
            messagebox.showerror("Login Error","No user with that name/password can be found")
        else:
            window = tk.Toplevel()
            CustomerWindow(window,bank.search_customers_by_name(self.e.get()))
    def open_register(self):
        self.register_window = tk.Toplevel()
        rp = RegisterPerson(self.register_window)
        self.register_window.title("Register")        

class RegisterPerson(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent

        self.name_label = tk.Label(self.parent,text="Name:")
        self.name_label.grid(column=0)

        self.name = ttk.Entry(self.parent,width=35)
        self.name.grid(row=0,column=1,columnspan=5)

        self.pwd_label = tk.Label(self.parent,text="Password:")
        self.pwd_label.grid(row=1,column=0)

        self.pwd = ttk.Entry(self.parent,width=35,show="*")
        self.pwd.grid(row=1,column=1,columnspan=5)

        self.addr_label = tk.Label(self.parent,text="Address:")
        self.addr_label.grid(row=2,column=0)
        
        self.addr = tk.Text(self.parent,height=5,width=25)
        self.addr.grid(row=2,column=1,columnspan=5)

        self.register = ttk.Button(self.parent,text="Register",command=self.register)
        self.register.grid(row=3,column=2,sticky=tk.E)

    def register(self):

        #check that none of them are empty
        if self.name.get() == "" or self.pwd.get() == "" or self.addr.get(1.0,tk.END) == "":
            messagebox.showerror("Registration","Please make sure all information is filled out")
            return

        addr = []
        for a in self.addr.get(1.0,tk.END).split('\n'):
            if a != "":
                addr.append(a)
        cus = bank.create_customer(self.name.get(),self.pwd.get(),addr)
        if cus == None:
            messagebox.showerror("Register","a customer with that info already exists")
            return
        
        self.parent.destroy()

class OpenAccountDiag:
    def __init__(self,customer):
        self.parent = tk.Toplevel()
        self.customer = customer

        self.intrest = tk.StringVar(self.parent)
        self.intrest.set("1.00")

        self.intrest_label = tk.Label(self.parent,text="Intrest:")
        self.intrest_label.grid()

        self.intrest_options = tk.OptionMenu(self.parent,self.intrest,"0.5","5.0")
        self.intrest_options.grid(row=0,column=1)

        self.type_label = tk.Label(self.parent,text="Type:")
        self.type_label.grid(row=1,column=0)

        self.type = tk.StringVar(self.parent)
        self.type.set("Current Account")
        self.type_option = tk.OptionMenu(self.parent,self.type,"Current Account","ISA")
        self.type_option.grid(row=1,column=1,sticky="ew")

        button = ttk.Button(self.parent,text="Open Account",command=self.parent.destroy)
        button.grid(row=2,column=0,columnspan=2)
    def show(self):
        self.parent.wait_window()
        attr = AccountAttributes(self.type.get(),self.intrest.get())
        self.customer.open_account(attr)
        
class CustomerWindow(tk.Frame):
    def __init__(self,parent,customer):
        tk.Frame.__init__(self,parent)
        self.customer = customer
        self.parent = parent
        self.parent.title("Customer: %s" % self.customer.get_name())

        navbar = tk.Frame(self.parent)
        navbar.grid(row=0,column=0,sticky=tk.N)
        self.draw_navbar(navbar)

        self.account_list = tk.Frame(self.parent)
        self.account_list.grid(row=0,column=1)
        self.draw_accounts(self.account_list)

        self.info = tk.Frame(self.parent)
        self.info.grid(row=0,column=2,sticky=tk.N)
        self.draw_info(self.info)
    def draw_navbar(self,frame):
        frame.config( highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

        self.open_acc = ttk.Button(frame,text="Open Account",command=self.open_account)
        self.open_acc.grid(sticky=tk.N)

        self.update = ttk.Button(frame,text="Update Info",command=self.update_info)
        self.update.grid(row=1)

        self.loan = ttk.Button(frame,text="Loans",command=self.open_loans)
        self.loan.grid(row=2,column=0)
    def open_loans(self):
        LoanDiag(self.customer,self).show()
    def update_info(self):
        UpdateCustomerRecordsDiag(self.customer,self).show()
    def open_transfer(self,acc):
        window = tk.Toplevel()
        TransferWindow(window,acc,self)
        print("opening transfer window: %d" % acc.account_no)
    def draw_accounts(self,frame):
        for child in frame.winfo_children():
            child.destroy()

        for acc in self.customer.get_accounts():
            acc_frame = tk.Frame(frame,bd=1)

            id = tk.Label(acc_frame,text="Account Number: %d" % acc.account_no)
            id.grid()

            balance = tk.Label(acc_frame,text="Balance: %.2f" % acc.balance)
            balance.grid(row=1,sticky=tk.W)

            acc_type = tk.Label(acc_frame,text="Type: %s" % acc.attr.type)
            acc_type.grid(row = 2,column=0,sticky=tk.W)

            acc_intrest = tk.Label(acc_frame,text="Intrest: %s" % acc.attr.intrest)
            acc_intrest.grid(row=3,column=0,sticky=tk.W)

            transfer_monies = ttk.Button(acc_frame,text="Transfer Money",command=lambda acc=acc: self.open_transfer(acc))
            transfer_monies.grid(row=4,column=0,sticky=tk.E)

            deposit_monies = ttk.Button(acc_frame,text="Deposit",command=lambda acc=acc:self.deposit(acc))
            deposit_monies.grid(row=4,column=1)

            withdraw = ttk.Button(acc_frame,text="Withdraw",command=lambda acc=acc:self.withdraw(acc))
            withdraw.grid(row=4,column=2)

            acc_frame.pack()
    def open_account(self):
        OpenAccountDiag(self.customer).show()
        bank .save_bank_data()
        self.redraw_accounts()
    def redraw_accounts(self):
        self.draw_accounts(self.account_list)
    def deposit(self,acc):
        amt = AmountDiag().show()
        acc.balance += amt
        bank.save_bank_data()
        self.redraw_accounts()
    def withdraw(self,acc):
        amt = AmountDiag().show()
        acc.balance -= amt
        bank.save_bank_data()
        self.redraw_accounts()
    def draw_info(self,frame):
        frame.config( highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

        for child in frame.winfo_children():
            child.destroy()

        name = "Name: %s" % self.customer.get_name()
        name_label = tk.Label(frame,text=name)
        name_label.grid(row=0,column=0,sticky=tk.W)

        address = "Address: "
        for a in self.customer.get_address():
            address += "%s\n" % a

        address_label = tk.Label(frame,text=address)
        address_label.grid(row=1,column=0)
    def redraw_info(self):
        self.draw_info(self.info)
    def open_transfer(self,acc):
        window = tk.Toplevel()
        TransferWindow(window,acc,self)
        print("opening transfer window: %d" % acc.account_no)

class TransferWindow:
    def __init__(self,parent,acc,window):
        self.parent = parent
        self.acc = acc
        self.window = window

        self.parent.title("Transfer from: %d" % acc.account_no)

        self.name_label = tk.Label(self.parent,text="Name:")
        self.name_label.grid(row=0,column=0)

        self.name = ttk.Entry(self.parent)
        self.name.grid(row=0,column=1)

        self.acc_no_label = tk.Label(self.parent,text="Account:")
        self.acc_no_label.grid(row=1,column=0)

        self.acc_no = ttk.Entry(self.parent)
        self.acc_no.grid(row=1,column=1)

        self.amount_label = tk.Label(self.parent,text="Amount:")
        self.amount_label.grid(row=2,column=0)

        self.amount = ttk.Entry(self.parent)
        self.amount.grid(row=2,column=1)

        self.transfer = ttk.Button(self.parent,text="Transfer",command=self.transfer)
        self.transfer.grid(row=3,column=0,columnspan=2)
    def transfer(self):
        amt = 0
        acc_no = 0
        try:
            amt = float(self.amount.get())
            acc_no = int(self.acc_no.get())
        except ValueError:
            return


        error = self.acc.transfer(bank,self.name.get(),acc_no,amt)
        if error == None:
            self.window.redraw_accounts()
            bank.save_bank_data()
            self.parent.destroy()
        else:
            messagebox.showerror("Transfer",error)

class AmountDiag:
    def __init__(self):
        self.frame = tk.Toplevel()
        self.var = tk.StringVar()

        self.amt_label = tk.Label(self.frame,text="Amount:")
        self.amt_label.grid(row=0,column=0)

        self.amt = ttk.Entry(self.frame,textvariable=self.var)
        self.amt.grid(row=0,column=1)

        self.button = ttk.Button(self.frame,text="Submit",command=self.frame.destroy)
        self.button.grid(row=1,column=1)
    def show(self):
        self.frame.wait_window()
        try:
            amt = float(self.var.get())
            return amt
        except ValueError:
            return 0

class UpdateCustomerRecordsDiag:
    def __init__(self,customer,window):
        self.parent = tk.Toplevel()
        self.customer = customer
        self.window = window

        self.name_label = tk.Label(self.parent,text="Name:")
        self.name_label.grid(column=0)

        self.name = ttk.Entry(self.parent,width=35)
        self.name.insert(0,self.customer.get_name())
        self.name.grid(row=0,column=1,columnspan=5)

        self.addr_label = tk.Label(self.parent,text="Address:")
        self.addr_label.grid(row=1,column=0)
        
        self.addr = tk.Text(self.parent,height=5,width=25)
        self.addr.grid(row=1,column=1,columnspan=5)

        address = ""
        for a in self.customer.get_address():
            address += "%s\n" % a
        self.addr.insert(tk.END,address)

        self.register = ttk.Button(self.parent,text="Update",command=self.update)
        self.register.grid(row=2,column=1)
    def show(self):
        self.parent.wait_window()
    def update(self):
        addr = []
        for a in self.addr.get(1.0,tk.END).split('\n'):
            if a != "":
                addr.append(a)
        self.customer.update(self.name.get(),addr)
        bank.save_bank_data()
        self.window.redraw_info()
        self.parent.destroy()

class AdminLogin:
    def __init__(self):
        self.parent = tk.Toplevel()

        self.idLabel = tk.Label(self.parent,text="Name:",justify=tk.LEFT)
        self.idLabel.grid(column=0)

        self.e = ttk.Entry(self.parent,width=30)
        self.e.grid(row=0,column=1,columnspan = 5)

        pwdLabel = tk.Label(self.parent,text="Password:")
        pwdLabel.grid(row=1,column=0)

        self.pwd = ttk.Entry(self.parent,width=30,show='*')
        self.pwd.grid(row=1,column=1)

        login = ttk.Button(self.parent,text='Login',command=self.try_login)
        login.grid(row = 2,column=1,sticky=tk.E)
    def try_login(self):
        admin = bank.admin_login(self.e.get(),self.pwd.get())
        if admin == None:
            messagebox.showerror("Login Error","failed to login admin")
        else:
            AdminWindow(admin)
            self.parent.destroy()

class AdminWindow:
    def __init__(self,admin):
        self.admin = admin
        self.parent = tk.Toplevel()
        self.parent.title("Admin")

        self.cus_search = tk.Frame(self.parent)
        self.cus_search.grid(sticky=tk.N)
        self.draw_search(self.cus_search)

        self.customer_operations = tk.Frame(self.parent)
        self.customer_operations.grid(row=0,column=1,sticky=tk.N)

        self.own_info = tk.Frame(self.parent)
        self.own_info.grid(row=0,column=2,sticky=tk.N)
        self.redraw_info()
    def draw_search(self,frame):
        frame.config( highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

        title = tk.Label(frame,text="Customer Search")
        title.grid(row=0,columnspan=2)

        name_label = tk.Label(frame,text="Name:")
        name_label.grid(row=1,sticky=tk.W)

        self.customer_search_name = ttk.Entry(frame)
        self.customer_search_name.grid(row=1,column=1)

        search = ttk.Button(frame,text="Search",command=self.search_customer)
        search.grid(row=2,columnspan=2)

        dump_all = ttk.Button(frame,text="Print All Customers",command=bank.dump_customers)
        dump_all.grid(row=3,column=0,columnspan=2)

        loan_report = ttk.Button(frame,text="Loan Report",command=self.show_loans)
        loan_report.grid(row=4,column=0,columnspan=2)

        loan_request = ttk.Button(frame,text="Loan Request",command=self.open_requests)
        loan_request.grid(row=5,column=0)
    def open_requests(self):
        AdminLoanReqDiag().show()
    def show_loans(self):
        LoanReportDiag().show()
    def search_customer(self):
        customer = bank.search_customers_by_name(self.customer_search_name.get())
        self.customer_search_name.delete(0,tk.END)
        if customer != None:
            CustomerOperations(self.customer_operations,customer)
    def redraw_info(self):
        frame = self.own_info
        frame.config( highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

        for child in frame.winfo_children():
            child.destroy()

        name = "Name: %s" % self.admin.get_name()
        name_label = tk.Label(frame,text=name)
        name_label.grid(row=0,column=0,sticky=tk.W)

        address = "Address: "
        for a in self.admin.get_address():
            address += "%s\n" % a

        address_label = tk.Label(frame,text=address)
        address_label.grid(row=1,column=0)

        update = ttk.Button(frame,text="Update Info",command=self.update_info)
        update.grid(row=2,column=0,columnspan=2)
    def update_info(self):
        UpdateCustomerRecordsDiag(self.admin,self).show()

class CustomerOperations:
    def __init__(self,frame,customer):
        self.parent = frame
        self.customer = customer

        self.parent.config( highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

        self.options = tk.Frame(self.parent)
        self.options.grid(sticky=tk.W)
        self.draw_options()

        self.customer_info = tk.Frame(self.parent)
        self.customer_info.grid(row=1,column=0,sticky=tk.W)
        self.redraw_info()

        self.customer_accounts = tk.Frame(self.parent)
        self.customer_accounts.grid(row=2,column=0,sticky=tk.W)
        self.redraw_accounts()
    def clear(self):
        for child in self.parent.winfo_children():
            child.destroy()
    def draw_options(self):
        self.options.config( highlightbackground="blue", highlightcolor="blue", highlightthickness=1,bd=0)

        close = ttk.Button(self.options,text="Close account",command=self.close_account)
        close.grid()

        update = ttk.Button(self.options,text="Update information",command=self.update_info)
        update.grid(column=1,row=0)

        dump = ttk.Button(self.options,text="Print Info",command=self.customer.dump_info)
        dump.grid(column=2,row=0)
    def update_info(self):
        UpdateCustomerRecordsDiag(self.customer,self).show()
    def redraw_info(self):
        for child in self.customer_info.winfo_children():
            child.destroy()

        self.customer_info.config( highlightbackground="blue", highlightcolor="blue", highlightthickness=1,bd=0)

        name = "Name: %s" % self.customer.get_name()
        name_label = tk.Label(self.customer_info,text=name)
        name_label.grid(row=0,column=0,sticky=tk.W)

        address = "Address: "
        for a in self.customer.get_address():
            address += "%s\n" % a

        address_label = tk.Label(self.customer_info,text=address)
        address_label.grid(row=1,column=0)   

        self.customer_info.columnconfigure(1, weight=1)  
    def close_account(self):
        self.clear()
        bank.remove_customer(self.customer)
    def redraw_accounts(self):
        for child in self.customer_accounts.winfo_children():
            child.destroy()

        for acc in self.customer.get_accounts():
            acc_frame = tk.Frame(self.customer_accounts,bd=1)

            id = tk.Label(acc_frame,text="Account Number: %d" % acc.account_no)
            id.grid()

            balance = tk.Label(acc_frame,text="Balance: %.2f" % acc.balance)
            balance.grid(row=1,sticky=tk.W)

            acc_type = tk.Label(acc_frame,text="Type: %s" % acc.attr.type)
            acc_type.grid(row = 2,column=0,sticky=tk.W)

            acc_intrest = tk.Label(acc_frame,text="Intrest: %s" % acc.attr.intrest)
            acc_intrest.grid(row=3,column=0,sticky=tk.W)

            transfer_monies = ttk.Button(acc_frame,text="Transfer Money",command=lambda acc=acc: self.open_transfer(acc))
            transfer_monies.grid(row=4,column=0,sticky=tk.E)

            deposit_monies = ttk.Button(acc_frame,text="Deposit",command=lambda acc=acc:self.deposit(acc))
            deposit_monies.grid(row=4,column=1)

            withdraw = ttk.Button(acc_frame,text="Withdraw",command=lambda acc=acc:self.withdraw(acc))
            withdraw.grid(row=4,column=2)

            acc_frame.pack()
    def deposit(self,acc):
        amt = AmountDiag().show()
        acc.balance += amt
        bank.save_bank_data()
        self.redraw_accounts()
    def withdraw(self,acc):
        amt = AmountDiag().show()
        acc.balance -= amt
        bank.save_bank_data()
        self.redraw_accounts()
    def open_transfer(self,acc):
        window = tk.Toplevel()
        TransferWindow(window,acc,self)
        print("opening transfer window: %d" % acc.account_no)

class LoanDiag:
    def __init__(self,customer,window):
        self.customer = customer
        self.parent = tk.Toplevel()
        self.window = window

        take_out = ttk.Button(self.parent,text="Take Out Loan",command=self.open_loan_creation)
        take_out.pack()

        pay_back = ttk.Button(self.parent,text="Payback",command=self.open_payback)
        pay_back.pack()
    def open_payback(self):
        PayLoanDiag(self.customer,self.window).show()
    def open_loan_creation(self):
        OpenLoanDiag(self.customer,self.window).show()
    def show(self):
        self.parent.wait_window()

class OpenLoanDiag:
    def __init__(self,customer,window):
        self.customer = customer
        self.parent = tk.Toplevel()
        self.window = window

        self.selected_acc = tk.IntVar()

        accs = []
        for a in self.customer.get_accounts():
            accs.append(a.account_no)

        acc_label = tk.Label(self.parent,text="Account:")
        acc_label.grid()

        self.account = tk.OptionMenu(self.parent,self.selected_acc,*accs)
        self.account.grid(row=0,column=1)

        amt_label = tk.Label(self.parent,text="Amount:")
        amt_label.grid(row=1,column=0)

        self.amt = ttk.Entry(self.parent)
        self.amt.grid(row=1,column=1)

        btn = ttk.Button(self.parent,text="Take Loan",command=self.take_loan)
        btn.grid(row=2,column=0,columnspan=2)
    def take_loan(self):
        acc = self.customer.find_account(self.selected_acc.get())
        if acc is None:
            return

        amt = 0
        try:
            amt = float(self.amt.get())
        except ValueError:
            return

        if not acc.loan is None:
            messagebox.showerror("Loan","that account already has a loan")
            return

        success = acc.take_loan(amt)
        if not success:
            success = acc.admin_request_loan(amt,bank)
            if not success:
                messagebox.showerror("Loan","Sorry failed to take out loan")
            else:
                messagebox.showinfo("Loan","your request has been passed onto the admin")
        else:
            self.parent.destroy()
            self.window.redraw_accounts()
            bank.save_bank_data()


    def show(self):
        self.parent.wait_window()

class PayLoanDiag:
    def __init__(self,customer,window):
        self.customer = customer
        self.window = window

        self.parent = tk.Toplevel()

        self.selected_acc = tk.IntVar()

        accs = []
        for a in self.customer.get_accounts():
            accs.append(a.account_no)

        acc_label = tk.Label(self.parent, text="Account:")
        acc_label.grid()

        self.account = tk.OptionMenu(self.parent, self.selected_acc, *accs)
        self.account.grid(row=0, column=1)

        amt_label = tk.Label(self.parent, text="Amount:")
        amt_label.grid(row=1, column=0)

        self.amt = ttk.Entry(self.parent)
        self.amt.grid(row=1, column=1)

        btn = ttk.Button(self.parent, text="Payback", command=self.payback)
        btn.grid(row=2, column=0, columnspan=2)
    def payback(self):
        acc = self.customer.find_account(self.selected_acc.get())
        if acc is None:
            return
        if acc.loan is None:
            return

        amt = 0
        try:
            amt = float(self.amt.get())
        except ValueError:
            return

        success = acc.payback_loan(amt)
        if not success:
            messagebox.showerror("Loan","unable to payback loan")
            return

        self.window.redraw_accounts()
        bank.save_bank_data()
        self.parent.destroy()


    def show(self):
        self.parent.wait_window()

class LoanReportDiag:
    def __init__(self):
        self.parent = tk.Toplevel()

        loan_holder = tk.Frame(self.parent)
        loan_holder.grid()

        loans = bank.get_loans()

        for loan in loans:
            self.draw_loan(loan_holder,loan)

    def draw_loan(self,parent,loan):
        frame = tk.Frame(parent)
        name = tk.Label(frame,text="Name: %s" % loan.account.customer.name)
        name.grid(sticky=tk.W)

        account_no = tk.Label(frame,text="Account: %d" % loan.account.account_no)
        account_no.grid(row=1,column=0,sticky=tk.W)

        amt = tk.Label(frame,text="Amount Due: %.2f" % loan.amt_left)
        amt.grid(row=2,column=0,sticky=tk.W)

        date = datetime.fromtimestamp(loan.due_date)

        date_label = tk.Label(frame,text="Due date: %s" % date.strftime("%d/%m/%Y"))
        date_label.grid(row=3,column=0,sticky=tk.W)

        frame.pack()

    def show(self):
        self.parent.wait_window()

class AdminLoanReqDiag:
    def __init__(self):
        self.parent = tk.Toplevel()

        self.request_holder = tk.Frame(self.parent)
        self.request_holder.grid()

        self.redraw_requests()
    def redraw_requests(self):
        for child in self.request_holder.winfo_children():
            child.destroy()

        for req in bank.loan_requests:
            self.draw_request(req)

    def draw_request(self,request):
        frame = tk.Frame(self.request_holder)

        name = tk.Label(frame,text="Customer: %s" % request.customer.name)
        name.grid(sticky=tk.W)

        acc = tk.Label(frame,text="Account: %d" % request.account.account_no)
        acc.grid(row=1,column=0,sticky=tk.W)

        amt = tk.Label(frame,text="Amount: %.2f" % request.amt)
        amt.grid(row=2,column=0,sticky=tk.W)

        reject = ttk.Button(frame,text="Reject",command=lambda r=request: self.reject_request(r))
        reject.grid(row=3,column=0,sticky=tk.W)

        accept = ttk.Button(frame,text="Accept",command=lambda r=request: self.accept_request(r))
        accept.grid(row=3,column=0,sticky=tk.E)

        frame.pack()

    def accept_request(self,req):
        req.approve()
        bank.remove_request(req)
        bank.save_bank_data()
        print("approved request of %.2f for %d" % (req.amt,req.account.account_no))
        self.redraw_requests()

    def reject_request(self,req):
        bank.remove_request(req)
        bank.save_bank_data()
        print("Rejected loan request for %d" % req.account.account_no)
        self.redraw_requests()
    def show(self):
        self.parent.wait_window()


bank = BankSystem()

root = tk.Tk()
root.title('Bank System')
app = MainAppliation(root)
root.mainloop()