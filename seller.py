from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class SellerPage():
    def __init__(self, root, database, style_1):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._seller_page = None
        self._stand = "1"

    def getPage(self):
        if not self._seller_page:
            #page
            seller_page = Frame(self._root)

            self.createColumns(seller_page)
            self.createRows(seller_page)
            self.loadImages()
            self.createOrderTable(seller_page)
            self.createProductTable(seller_page)

            #labels
            self._stand_label = Label(seller_page, text="Stand Nr.: 1", font=self._style_1)
            self._stand_label.grid(row=0, column=1)

            Label(seller_page, image=self._logo_img, font=self._style_1).grid(row=6, column=7)

            self._seller_page = seller_page
        return self._seller_page
    
    def createColumns(self, seller_page):
        seller_page.grid_columnconfigure(0, weight=1)
        seller_page.grid_columnconfigure(1, weight=1)
        seller_page.grid_columnconfigure(2, weight=1)
        seller_page.grid_columnconfigure(3, weight=1)
        seller_page.grid_columnconfigure(4, weight=1)
        seller_page.grid_columnconfigure(5, weight=1)
        seller_page.grid_columnconfigure(6, weight=1)
        seller_page.grid_columnconfigure(7, weight=1)
        seller_page.grid_columnconfigure(8, weight=1)

    def createRows(self, seller_page):
        seller_page.grid_rowconfigure(0, weight=1)
        seller_page.grid_rowconfigure(1, weight=1)
        seller_page.grid_rowconfigure(2, weight=1)
        seller_page.grid_rowconfigure(3, weight=1)
        seller_page.grid_rowconfigure(4, weight=1)
        seller_page.grid_rowconfigure(5, weight=1)
        seller_page.grid_rowconfigure(6, weight=1)

    def loadImages(self):
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

    def createOrderTable(self, seller_page):
        #frames
        form_frame = Frame(seller_page)
        form_frame.grid(row=1, column=1, columnspan=7)

        # Title label
        title = Label(
            form_frame,
            text="Offene Bestellungen:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=45
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Bestellung Nr.", "Zeitstempel", "Status",)
        self.table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(seller_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table.grid(row=1, column=0, sticky="nsew")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

    def createProductTable(self, seller_page):
        #frames
        form_frame = Frame(seller_page)
        form_frame.grid(row=2, column=1, columnspan=7)

        # Title label
        title = Label(
            form_frame,
            text="Bestandsanzeige:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=45
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Name", "Menge", "Warnung",)
        self.table_2 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self.table_2.heading(col, text=col)
            self.table_2.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(seller_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table_2.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table_2.grid(row=1, column=0, sticky="nsew")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self.table_2.yview)
        self.table_2.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

    def fillOrderTableRows(self, stand):
        #clear existing rows
        self.table.delete(*self.table.get_children())
        # Insert sample data
        data = []
        orders = self._database.getOrdersForStand(stand)

        for order in orders:
            data.append( (order["order"], order["timestamp"], order["status_desc"]) )

        for i, row in enumerate(data):
            self.table.insert("", END, values=row, tags=("row",))

        #update stand
        self._stand = stand

    def fillProductTableRows(self, stand):
        #clear existing rows
        self.table_2.delete(*self.table_2.get_children())
        # Insert sample data
        data = []
        products = self._database.getProductsForStand(stand)

        for product in products:
            warning = ""
            if int(product["quantity"]) > 10:
                warning = "!!!"
            data.append( (product["name"], product["quantity"], warning) )

        for i, row in enumerate(data):
            self.table_2.insert("", END, values=row, tags=("row",))
