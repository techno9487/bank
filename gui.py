import tkinter as tk
from tkinter import ttk,messagebox
import logging
from bank_system import BankSystem

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
        addr = []
        for a in self.addr.get(1.0,tk.END).split('\n'):
            if a != "":
                addr.append(a)
        cus = bank.create_customer(self.name.get(),self.pwd.get(),addr)
        if cus == None:
            messagebox.showerror("Register","a customer with that info already exists")
            return
        
        self.parent.destroy()

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

            transfer_monies = ttk.Button(acc_frame,text="Transfer Money",command=lambda acc=acc: self.open_transfer(acc))
            transfer_monies.grid(row=2,column=0,sticky=tk.E)

            deposit_monies = ttk.Button(acc_frame,text="Deposit",command=lambda acc=acc:self.deposit(acc))
            deposit_monies.grid(row=2,column=1)

            withdraw = ttk.Button(acc_frame,text="Withdraw",command=lambda acc=acc:self.withdraw(acc))
            withdraw.grid(row=2,column=2)

            acc_frame.pack()
    def open_account(self):
        self.customer.open_account()
        bank .save_bank_data()
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
        self.cus_search.grid()
        self.draw_search(self.cus_search)
    def draw_search(self,frame):
        frame.config( highlightbackground="green", highlightcolor="green", highlightthickness=1,bd=0)

        title = tk.Label(frame,text="Customer Search")
        title.grid(columnspan=2)

        name_label = tk.Label(frame,text="Name:")
        name_label.grid(row=1,sticky=tk.W)

        name = ttk.Entry(frame)
        name.grid(row=1,column=1)

        search = ttk.Button(frame,text="Search")
        search.grid(row=2,columnspan=2)

bank = BankSystem()

root = tk.Tk()
root.title('Bank System')
app = MainAppliation(root)
root.mainloop()