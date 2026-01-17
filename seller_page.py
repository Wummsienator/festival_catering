from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from elements import PlaceholderEntry

class SellerPage():
    def __init__(self, root, database, style_1):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._seller_page = None
        self._stand = None

    def get_page(self):
        if not self._seller_page:
            #page
            seller_page = Frame(self._root)

            self._create_columns(seller_page)
            self._create_rows(seller_page)
            self._load_images()
            self._create_order_table(seller_page)
            self._create_product_table(seller_page)
            self._create_product_combo_box(seller_page)

            #labels
            self._stand_label = Label(seller_page, text="Stand Nr.: 1", font=self._style_1)
            self._stand_label.grid(row=0, column=1)

            Label(seller_page, image=self._logo_img, font=self._style_1).grid(row=6, column=7)

            #buttons
            Button(seller_page, text="Status weiterschalten", command=lambda: self._on_change_status(), font=self._style_1, background="#75E6DA").grid(row=2, column=1, columnspan=2)

            self._seller_page = seller_page
        return self._seller_page
    
    def _create_columns(self, seller_page):
        seller_page.grid_columnconfigure(0, weight=1)
        seller_page.grid_columnconfigure(1, weight=1)
        seller_page.grid_columnconfigure(2, weight=1)
        seller_page.grid_columnconfigure(3, weight=1)
        seller_page.grid_columnconfigure(4, weight=1)
        seller_page.grid_columnconfigure(5, weight=1)
        seller_page.grid_columnconfigure(6, weight=1)
        seller_page.grid_columnconfigure(7, weight=1)
        seller_page.grid_columnconfigure(8, weight=1)

    def _create_rows(self, seller_page):
        seller_page.grid_rowconfigure(0, weight=1)
        seller_page.grid_rowconfigure(1, weight=1)
        seller_page.grid_rowconfigure(2, weight=1)
        seller_page.grid_rowconfigure(3, weight=1)
        seller_page.grid_rowconfigure(4, weight=1)
        seller_page.grid_rowconfigure(5, weight=1)
        seller_page.grid_rowconfigure(6, weight=1)

    def _load_images(self):
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

    def _create_order_table(self, seller_page):
        #frames
        form_frame = Frame(seller_page)
        form_frame.grid(row=1, column=1, columnspan=7)

        #title label
        title = Label(
            form_frame,
            text="Offene Bestellungen:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        #define table columns
        columns = ("Bestellung Nr.", "Zeitstempel", "Status", "Priorisiert")
        self._table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        #define headings
        for col in columns:
            self._table.heading(col, text=col)
            self._table.column(col, anchor="center", width=180)

        #style rows
        style = ttk.Style(seller_page)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table.grid(row=1, column=0, sticky="nsew")

        #vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self._table.bind("<Double-1>", self._open_popup)

    def _create_product_table(self, seller_page):
        #frames
        form_frame = Frame(seller_page)
        form_frame.grid(row=3, column=1, columnspan=7)

        #title label
        title = Label(
            form_frame,
            text="Bestandsanzeige:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=45
        )
        title.grid(row=0, column=0)

        #define table columns
        columns = ("Name", "Menge", "Warnung",)
        self._table_2 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        #define headings
        for col in columns:
            self._table_2.heading(col, text=col)
            self._table_2.column(col, anchor="center", width=180)

        #style rows
        style = ttk.Style(seller_page)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table_2.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table_2.grid(row=1, column=0, sticky="nsew")

        #vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table_2.yview)
        self._table_2.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self._table_2.bind("<<TreeviewSelect>>", self._disable_selection)

    def _disable_selection(self, event=None):
        event.widget.selection_remove(event.widget.selection())

    def fill_order_table_rows(self, stand):
        #clear existing rows
        self._table.delete(*self._table.get_children())
        #insert sample data
        data = []
        orders = self._database.get_orders_for_stand(stand)

        for order in orders:
            data.append( (order["ID"], order["timestamp"], order["status_desc"],  order["prioritized"]) )

        for i, row in enumerate(data):
            self._table.insert("", END, values=row, tags=("row",))

        #update stand
        self._stand = stand

    def fill_product_table_rows(self, stand):
        #clear existing rows
        self._table_2.delete(*self._table_2.get_children())
        #insert sample data
        data = []
        products = self._database.get_products_for_stand(stand)

        for product in products:
            warning = ""
            if int(product["quantity"]) < 10:
                warning = "!!!"
            data.append( (product["name"], product["quantity"], warning) )

        for i, row in enumerate(data):
            self._table_2.insert("", END, values=row, tags=("row",))

    def _create_product_combo_box(self, seller_page):
        #get products
        products = self._database.get_products()
        options = {}
        for product in products:
            options[product["ID"]] = product["name"]

        #create combobox values
        display_values = [f"{v} ({k})" for k, v in options.items()]

        #style
        style = ttk.Style(seller_page)
        style.theme_use("default")

        #create combobox
        self._product_combo = ttk.Combobox(seller_page, values=display_values, state="readonly", font=self._style_1) 
        self._product_combo.grid(row=4, column=1)
        self._product_combo.set("Produkt wählen")

        #quantity input
        _validate_int = (seller_page.register(self._validate_int), "%P")  
        self._quantity_val = StringVar()
        quantity_ipt = PlaceholderEntry(seller_page, "Menge", "grey", font=self._style_1, bg="#D4F1F4", textvariable=self._quantity_val, validate="key", validatecommand=_validate_int)
        quantity_ipt.grid(row=4, column=2)

        #button
        Button(seller_page, text="Bestand hinzufügen", command=lambda: self._on_add_product(), font=self._style_1, background="#75E6DA").grid(row=4, column=6)

    def _validate_int(self, new_value):
        if new_value == "" or new_value == "Menge":   # allow empty string and placeholder value
            return True
        return new_value.isdigit()

    def _on_add_product(self, event=None):
        display = self._product_combo.get()
        quantity = self._quantity_val.get()
        if not display or not quantity or quantity == "Menge":
            return

        key = display.split("(", 1)[1].strip(")")   #extract key from display string

        #update data
        self._database.add_product_for_stand(self._stand, key, int(quantity))
        self.fill_product_table_rows(self._stand)

        #clear fields
        self._product_combo.set("Produkt wählen")
        self._quantity_val.set("")

    def _open_popup(self, event=None):
        #get selection
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        #create a popup window
        popup = Toplevel(self._seller_page)
        popup.title("Bestellung: " + selected_order[0])
        popup.geometry("400x300")

        #title label
        title = Label(
            popup,
            text="Positionen:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=30
        )
        title.grid(row=0, column=0)

        #define table columns
        columns = ("Name", "Menge")
        table = ttk.Treeview(popup, columns=columns, show="headings", selectmode="browse", height=4)

        #define headings
        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=120)

        #style rows
        style = ttk.Style(popup)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        table.tag_configure("row", background="#D4F1F4")   # baby blue

        table.grid(row=1, column=0, sticky="nsew")

        #vertical scrollbar
        vsb = ttk.Scrollbar(popup, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        #fill rows
        data = []
        positions, special_requests = self._database.get_positions_for_order(selected_order[0])

        for position in positions:
            data.append( (position["name"], position["quantity"]) )

        for i, row in enumerate(data):
            table.insert("", END, values=row, tags=("row",))

        #special requests label
        Label(popup, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0)
        Label(popup, text=special_requests, font=self._style_1).grid(row=3, column=0)

    def _on_change_status(self, event=None):
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        #update data
        self._database.change_status_for_order(selected_order[0])
        self.fill_order_table_rows(self._stand)