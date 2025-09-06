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
            self.createProductComboBox(seller_page)

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
        self._table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self._table.heading(col, text=col)
            self._table.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(seller_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table.grid(row=1, column=0, sticky="nsew")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self._table.bind("<Double-1>", self.open_popup)

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
        self._table_2 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self._table_2.heading(col, text=col)
            self._table_2.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(seller_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table_2.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table_2.grid(row=1, column=0, sticky="nsew")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table_2.yview)
        self._table_2.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

    def fillOrderTableRows(self, stand):
        #clear existing rows
        self._table.delete(*self._table.get_children())
        # Insert sample data
        data = []
        orders = self._database.getOrdersForStand(stand)

        for order in orders:
            data.append( (order["order"], order["timestamp"], order["status_desc"]) )

        for i, row in enumerate(data):
            self._table.insert("", END, values=row, tags=("row",))

        #update stand
        self._stand = stand

    def fillProductTableRows(self, stand):
        #clear existing rows
        self._table_2.delete(*self._table_2.get_children())
        # Insert sample data
        data = []
        products = self._database.getProductsForStand(stand)

        for product in products:
            warning = ""
            if int(product["quantity"]) < 10:
                warning = "!!!"
            data.append( (product["name"], product["quantity"], warning) )

        for i, row in enumerate(data):
            self._table_2.insert("", END, values=row, tags=("row",))

    def createProductComboBox(self, seller_page):
        #get products
        products = self._database.getProducts()
        options = {}
        for product in products:
            options[product["product"]] = product["name"]

        #create combobox values
        display_values = [f"{v} ({k})" for k, v in options.items()]

        #create combobox
        self._product_combo = ttk.Combobox(seller_page, values=display_values, state="readonly") 
        self._product_combo.grid(row=3, column=1)

    def open_popup(self, event=None):
        #get selection
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        # Create a popup window
        popup = Toplevel(self._seller_page)
        popup.title("Bestellung: " + selected_order[0])
        popup.geometry("400x300")

        # Title label
        title = Label(
            popup,
            text="Positionen:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=30
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Name", "Menge")
        table = ttk.Treeview(popup, columns=columns, show="headings", selectmode="browse", height=4)

        # Define headings
        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=120)

        # Style rows
        style = ttk.Style(popup)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        table.tag_configure("row", background="#D4F1F4")   # baby blue

        table.grid(row=1, column=0, sticky="nsew")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(popup, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        #fill rows
        data = []
        positions, special_requests = self._database.getPositionsForOrder(selected_order[0])

        for position in positions:
            data.append( (position["name"], position["quantity"]) )

        for i, row in enumerate(data):
            table.insert("", END, values=row, tags=("row",))

        #special requests label
        Label(popup, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0)
        Label(popup, text=special_requests, font=self._style_1).grid(row=3, column=0)
