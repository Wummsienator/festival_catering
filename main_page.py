from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from database import Database
from login import LoginPage

root = Tk()
database = Database()
style1 = font.Font(size=20)

#columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

#rows
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

#pages
loginPage = LoginPage(root, database, style1).getPage()
loginPage.grid(row=1, column=1, sticky="nsew")

#settings
loginPage.tkraise()
root.geometry("750x750")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()