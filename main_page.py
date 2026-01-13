from tkinter import *
from tkinter import font
# from database import Database
from database_test import Database
from login import LoginPage
from visitor import VisitorPage
from order import OrderPage
from seller import SellerPage

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

order_page_management = OrderPage(root, database, style_1)
order_page = order_page_management.getPage()
order_page.grid(row=0, column=1, sticky="nsew")

seller_page_management = SellerPage(root, database, style_1)
seller_page = seller_page_management.getPage()
seller_page.grid(row=0, column=1, sticky="nsew")

login_page_management.setVisitorPageManagement(visitor_page_management)
login_page_management.setSellerPageManagement(seller_page_management)
visitor_page_management.setOrderPageManagement(order_page_management)
order_page_management.setVisitorPageManagement(visitor_page_management)

#settings
login_page.tkraise()
root.geometry("750x750")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()