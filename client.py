from tkinter import *
from tkinter import font
from database import Database
from login_page import LoginPage
from visitor_page import VisitorPage
from order_page import OrderPage
from seller_page import SellerPage

root = Tk()

# --- scaling ---
screen_h = root.winfo_screenheight()
scaling = screen_h / 1200
scaling = max(0.75, min(scaling, 1.6))   # clamp to something sane

database = Database()

# main font
base_font_size = int(15 * scaling)
style_1 = font.Font(family="Arial", size=base_font_size)

# --- window settings ---
s_size_h = int(750 * scaling)
s_size_v = int(825 * scaling)
root.geometry(f"{s_size_h}x{s_size_v}")
root.title("Festival Catering")
root.resizable(False, False)

# --- one container for all pages ---
container = Frame(root)
container.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# --- pages ---
login_page_management = LoginPage(container, database, style_1, scaling)
login_page = login_page_management.get_page()
login_page.grid(row=0, column=0, sticky="nsew")

visitor_page_management = VisitorPage(container, database, style_1, scaling)
visitor_page = visitor_page_management.get_page()
visitor_page.grid(row=0, column=0, sticky="nsew")

order_page_management = OrderPage(container, database, style_1, scaling)
order_page = order_page_management.get_page()
order_page.grid(row=0, column=0, sticky="nsew")

seller_page_management = SellerPage(container, database, style_1, scaling)
seller_page = seller_page_management.get_page()
seller_page.grid(row=0, column=0, sticky="nsew")

login_page_management.set_visitor_pageManagement(visitor_page_management)
login_page_management.set_seller_page_management(seller_page_management)
visitor_page_management.set_order_page_management(order_page_management)
order_page_management.set_visitor_pageManagement(visitor_page_management)

# --- start ---
login_page.tkraise()
root.mainloop()
