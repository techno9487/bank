import tkinter as tk

class MainAppliation(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        idLabel = tk.Label(self.parent,text="User ID:",justify=tk.LEFT)
        idLabel.pack()

        e = tk.Entry(self.parent,width=50)
        e.pack()

        pwdLabel = tk.Label(self.parent,text="Password:")
        pwdLabel.pack()

        pwd = tk.Entry(self.parent,width=50,show='*')
        pwd.pack()

root = tk.Tk()
root.title('Bank System')
app = MainAppliation(root)
root.mainloop()