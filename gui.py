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
        cus = bank.create_customer(self.name.get(),self.pwd.get(),self.addr.get(1.0,tk.END).split("\n"))
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
        navbar.grid(row=0,column=0)
        self.draw_navbar(navbar)

        account_list = tk.Frame(self.parent)
        account_list.grid(row=0,column=1)
        self.draw_accounts(account_list)
    def draw_navbar(self,frame):
        self.open_acc = ttk.Button(frame,text="Open Account",command=self.open_account)
        self.open_acc.grid(sticky=tk.N)
    def open_transfer(self,acc):
        window = tk.Toplevel()
        TransferWindow(window,acc)
        print("opening transfer window: %d" % acc.account_no)
    def draw_accounts(self,frame):
        for acc in self.customer.get_accounts():
            acc_frame = tk.Frame(frame,bd=1)

            id = tk.Label(acc_frame,text="Account Number: %d" % acc.account_no)
            id.grid()

            balance = tk.Label(acc_frame,text="Balance %.2f" % acc.balance)
            balance.grid(row=1,sticky=tk.W)

            transfer_monies = ttk.Button(acc_frame,text="Transfer Money",command=lambda: self.open_transfer(acc))
            transfer_monies.grid(row=2,column=0,sticky=tk.W)

            acc_frame.pack()
    def open_account(self):
        self.customer.open_account()
        bank .save_bank_data()
        
class TransferWindow:
    def __init__(self,parent,acc):
        self.parent = parent

        self.name_label = tk.Label(self.parent,text="Name:")
        self.name_label.grid(row=0,column=0)

        self.name = ttk.Entry(self.parent)
        self.name.grid(row=0,column=1)


bank = BankSystem()

root = tk.Tk()
root.title('Bank System')
app = MainAppliation(root)
root.mainloop()