from tkinter import *
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
from database import Database

root = Tk()


#styles
style1 = font.Font(size=20)

#variables
database = Database()

#logo
logo_pil = Image.open("logo.png")
logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)

logo_img = ImageTk.PhotoImage(logo_pil)

# Title label
title = Label(
    root,
    text="Offene Bestellungen:",
    font=("Arial", 14, "bold"),
    bg="#05445E",   # dark teal background
    fg="white"
)
title.pack(fill="x")

# Define table columns
columns = ("Stand", "Wartezeit", "Status", "Bestellungsnummer")
table = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")

# Define headings
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=140)

# Insert sample data
data = []
orders = database.getOrdersForTicket("1234567")
for order in orders:
    data.append( (order["stand"], order["time"], order["status_desc"], order["order"]) )

for i, row in enumerate(data):
    # tag = "evenrow" if i % 2 == 0 else "oddrow"
    # table.insert("", END, values=row, tags=(tag,))
    table.insert("", END, values=row, tags=("evenrow",))

# Style rows
style = ttk.Style(root)
style.theme_use("default")

# Header style
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

# Row styles
style.configure("Treeview", font=("Arial", 11), rowheight=25)
table.tag_configure("evenrow", background="#D4F1F4")   # baby blue
# table.tag_configure("oddrow", background="white")

# Pack table
table.pack(expand=True, fill="both", padx=5, pady=5)

# Selection highlight
def on_select(event):
    selected = table.focus()
    values = table.item(selected, "values")
    print("Selected row:", values)

table.bind("<<TreeviewSelect>>", on_select)

#settings
root.geometry("950x950")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()