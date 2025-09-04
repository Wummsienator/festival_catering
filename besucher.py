from tkinter import *
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
from database import Database

class BesucherPage():
    def __init__(self, root, database, style1):
        self._root = root
        self._database = database
        self._style1 = style1
        self._besucherPage = ""

    def getPage(self):
        if not self._besucherPage:
            #page
            besucherPage = Frame(self._root)

            self.loadLogoImg()
            self.createOrderTable(besucherPage)

            self._besucherPage  = besucherPage
        return self._besucherPage
    
    def loadLogoImg(self):
        #logo
        logo_pil = Image.open("logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)

        self._logo_img = ImageTk.PhotoImage(logo_pil)

    
    def createOrderTable(self, besucherPage):
        # Title label
            title = Label(
                besucherPage,
                text="Offene Bestellungen:",
                font=("Arial", 14, "bold"),
                bg="#05445E",   # dark teal background
                fg="white"
            )
            title.pack(fill="x")

            # Define table columns
            columns = ("Stand", "Wartezeit", "Status", "Bestellungsnummer")
            self.table = ttk.Treeview(besucherPage, columns=columns, show="headings", selectmode="browse")

            # Define headings
            for col in columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center", width=140)

            # Insert sample data
            data = []
            orders = self._database.getOrdersForTicket("1234567")
            for order in orders:
                data.append( (order["stand"], order["time"], order["status_desc"], order["order"]) )

            for i, row in enumerate(data):
                # tag = "evenrow" if i % 2 == 0 else "oddrow"
                # table.insert("", END, values=row, tags=(tag,))
                self.table.insert("", END, values=row, tags=("evenrow",))

            # Style rows
            style = ttk.Style(besucherPage)
            style.theme_use("default")

            # Header style
            style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

            # Row styles
            style.configure("Treeview", font=("Arial", 11), rowheight=25)
            self.table.tag_configure("evenrow", background="#D4F1F4")   # baby blue
            # table.tag_configure("oddrow", background="white")

            # Pack table
            self.table.pack(expand=True, fill="both", padx=5, pady=5)

            self.table.bind("<<TreeviewSelect>>", self.on_select)
    
    def on_select(self, event):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        print("Selected row:", values)
