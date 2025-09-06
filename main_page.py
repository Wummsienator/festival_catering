from tkinter import *
from tkinter import font
from database import Database
from login import LoginPage
from visitor import VisitorPage
from order import OrderPage

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
login_page_management = LoginPage(root, database, style1)
login_page = login_page_management.getPage()
login_page.grid(row=0, column=1, sticky="nsew")

visitorPageManagement = VisitorPage(root, database, style1)
visitorPage = visitorPageManagement.getPage()
visitorPage.grid(row=0, column=1, sticky="nsew")

orderPageManagement = OrderPage(root, database, style1)
orderPage = orderPageManagement.getPage()
orderPage.grid(row=0, column=1, sticky="nsew")

login_page_management.setVisitorPageManagement(visitorPageManagement)
visitorPageManagement.setOrderPageManagement(orderPageManagement)
orderPageManagement.setVisitorPageManagement(visitorPageManagement)

#settings
login_page.tkraise()
root.geometry("750x750")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()