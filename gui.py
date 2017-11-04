import tkinter as tk
from tkinter import ttk
import logging

class MainAppliation(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        idLabel = tk.Label(self.parent,text="User ID:",justify=tk.LEFT)
        idLabel.grid(column=0)

        self.e = ttk.Entry(self.parent,width=30)
        self.e.grid(row=0,column=1,columnspan = 5)

        pwdLabel = tk.Label(self.parent,text="Password:")
        pwdLabel.grid(row=1,column=0)

        self.pwd = ttk.Entry(self.parent,width=30,show='*')
        self.pwd.grid(row=1,column=1)

        login = ttk.Button(self.parent,text='Login',command=self.try_login)
        login.grid(row = 2,column=1,sticky=tk.E)
    def try_login(self):
        pass

root = tk.Tk()
root.title('Bank System')
app = MainAppliation(root)
root.mainloop()