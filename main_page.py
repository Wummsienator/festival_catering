from tkinter import *
from tkinter import font
from database import Database
from login import LoginPage
from visitor import VisitorPage
from order import OrderPage

root = Tk()
database = Database()
style_1 = font.Font(size=15)

#columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

#rows
root.grid_rowconfigure(0, weight=1)

#pages
login_page_management = LoginPage(root, database, style_1)
login_page = login_page_management.getPage()
login_page.grid(row=0, column=1, sticky="nsew")

visitor_page_management = VisitorPage(root, database, style_1)
visitor_page = visitor_page_management.getPage()
visitor_page.grid(row=0, column=1, sticky="nsew")

orderPageManagement = OrderPage(root, database, style_1)
orderPage = orderPageManagement.getPage()
orderPage.grid(row=0, column=1, sticky="nsew")

login_page_management.setVisitorPageManagement(visitor_page_management)
visitor_page_management.setOrderPageManagement(orderPageManagement)
orderPageManagement.setVisitorPageManagement(visitor_page_management)

#settings
login_page.tkraise()
root.geometry("750x750")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()