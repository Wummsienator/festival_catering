from tkinter import *
from tkinter import font
from database import Database
from login_page import LoginPage
from visitor_page import VisitorPage
from order_page import OrderPage
from seller_page import SellerPage

root = Tk()
scaling = root.winfo_screenheight() / 1200     #pretty rough scaling 
database = Database()
style_1 = font.Font(size=round(15 * scaling))

#columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

#rows
root.grid_rowconfigure(0, weight=1)

#pages
login_page_management = LoginPage(root, database, style_1, scaling)
login_page = login_page_management.get_page()
login_page.grid(row=0, column=1, sticky="nsew")

visitor_page_management = VisitorPage(root, database, style_1, scaling)
visitor_page = visitor_page_management.get_page()
visitor_page.grid(row=0, column=1, sticky="nsew")

order_page_management = OrderPage(root, database, style_1, scaling)
order_page = order_page_management.get_page()
order_page.grid(row=0, column=1, sticky="nsew")

seller_page_management = SellerPage(root, database, style_1, scaling)
seller_page = seller_page_management.get_page()
seller_page.grid(row=0, column=1, sticky="nsew")

login_page_management.set_visitor_pageManagement(visitor_page_management)
login_page_management.set_seller_page_management(seller_page_management)
visitor_page_management.set_order_page_management(order_page_management)
order_page_management.set_visitor_pageManagement(visitor_page_management)

#settings
login_page.tkraise()
s_size = round(750 * scaling)
root.geometry(f"{s_size}x{s_size}")   
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()