from tkinter import *
from tkinter import font
from database import Database
from login import LoginPage
from besucher import BesucherPage

root = Tk()
database = Database()
style1 = font.Font(size=15)

#columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

#rows
root.grid_rowconfigure(0, weight=1)

#pages
loginPageManagement = LoginPage(root, database, style1)
loginPage = loginPageManagement.getPage()
loginPage.grid(row=0, column=1, sticky="nsew")

besucherPageManagement = BesucherPage(root, database, style1)
besucherPage = besucherPageManagement.getPage()
besucherPage.grid(row=0, column=1, sticky="nsew")

loginPageManagement.setBesucherPageManagement(besucherPageManagement)

#settings
loginPage.tkraise()
# besucherPage.tkraise()
root.geometry("750x750")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()