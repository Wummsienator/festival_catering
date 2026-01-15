from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class VisitorPage():
    def __init__(self, root, database, style_1):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._visitor_page = None
        self._ticket = "1234567"

        self._order_page = None

    def get_page(self):
        if not self._visitor_page:
            #page
            visitor_page = Frame(self._root)

            self._create_columns(visitor_page)
            self._create_rows(visitor_page)
            self._load_images()
            self._create_order_table(visitor_page)
            self._create_notification_table(visitor_page)

            #frames
            form_frame = Frame(visitor_page)
            form_frame.grid(row=2, column=6, columnspan=2)

            #labels
            self._ticket_label = Label(visitor_page, text="Ticket: 1234567", font=self._style_1)
            self._ticket_label.grid(row=0, column=1)
            self._credit_label = Label(visitor_page, text="Guthaben: 222€", font=self._style_1)
            self._credit_label.grid(row=0, column=6)

            Label(form_frame, text="Ticket Freund:", font=self._style_1).grid(row=0, column=0)

            Label(visitor_page, image=self._qr_img, font=self._style_1).grid(row=3, column=1)

            Label(visitor_page, image=self._logo_img, font=self._style_1).grid(row=6, column=7)

            #buttons
            Button(visitor_page, text="€▷", command=lambda: self._add_credit(), font=self._style_1, background="#75E6DA").grid(row=0, column=7)
            Button(visitor_page, text="Bestellung aufnehmen", command=lambda: self._on_go_to_order_page(), font=self._style_1, background="#75E6DA").grid(row=2, column=1)
            Button(form_frame, text="Bestellung freischalten", command=lambda: self._unlock_ticket_for_friend(), font=self._style_1, background="#75E6DA").grid(row=2, column=1)

            #input fields
            self._friend_ticket_val = StringVar()
            Entry(form_frame, font=self._style_1, bg="#D4F1F4", textvariable=self._friend_ticket_val).grid(row=0, column=1)

            self._visitor_page  = visitor_page
        return self._visitor_page
    
    def _create_columns(self, visitor_page):
        visitor_page.grid_columnconfigure(0, weight=1)
        visitor_page.grid_columnconfigure(1, weight=1)
        visitor_page.grid_columnconfigure(2, weight=1)
        visitor_page.grid_columnconfigure(3, weight=1)
        visitor_page.grid_columnconfigure(4, weight=1)
        visitor_page.grid_columnconfigure(5, weight=1)
        visitor_page.grid_columnconfigure(6, weight=1)
        visitor_page.grid_columnconfigure(7, weight=1)
        visitor_page.grid_columnconfigure(8, weight=1)

    def _create_rows(self, visitor_page):
        visitor_page.grid_rowconfigure(0, weight=1)
        visitor_page.grid_rowconfigure(1, weight=1)
        visitor_page.grid_rowconfigure(2, weight=1)
        visitor_page.grid_rowconfigure(3, weight=1)
        visitor_page.grid_rowconfigure(4, weight=1)
        visitor_page.grid_rowconfigure(5, weight=1)
        visitor_page.grid_rowconfigure(6, weight=1)
    
    def _load_images(self):
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        qr_pil = Image.open("img/QR_Code.png")
        qr_pil = qr_pil.resize((150, 150), Image.Resampling.LANCZOS)
        self._qr_img = ImageTk.PhotoImage(qr_pil)
    
    def _create_order_table(self, visitor_page):
        #frames
        form_frame = Frame(visitor_page)
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
        columns = ("Stand", "Wartezeit", "Status", "Bestellungsnummer")
        self._table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        #define headings
        for col in columns:
            self._table.heading(col, text=col)
            self._table.column(col, anchor="center", width=180)

        #style rows
        style = ttk.Style(visitor_page)
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
    
    def fill_order_table_rows(self, ticket):
        #clear existing rows
        self._table.delete(*self._table.get_children())
        #insert sample data
        data = []
        orders = self._database.get_orders_for_ticket(ticket)
        for order in orders:
            data.append( (order["stand"], order["time"], order["status_desc"], order["ID"]) )

        for i, row in enumerate(data):
            self._table.insert("", END, values=row, tags=("row",))

        #check vip
        is_vip = self._database.check_vip(ticket)

        ticket_txt = "Ticket: " + ticket
        if is_vip:
            ticket_txt = ticket_txt + " ☆"
        self._ticket_label.config(text=ticket_txt) 
        credit_txt = "Guthaben: " + str(self._database.get_credit_for_ticket(ticket)) + "€"
        self._credit_label.config(text=credit_txt) 

        #update ticket
        self._ticket = ticket

    def _create_notification_table(self, visitor_page):
        #define table columns
        column = "Benachrichtigungen:"
        self._table2 = ttk.Treeview(visitor_page, columns=column, show="headings", selectmode="browse", height=3)

        #define headings
        self._table2.heading(column, text=column)
        self._table2.column(column, anchor="center", width=600)

        #insert sample data
        data = [("Deine Bestellung kann in 20 Minuten an Stand 1 abgeholt werden.", ), ("Deine Bestellung an Stand 3 ist abholbereit", )]
        for i, row in enumerate(data):
            self._table2.insert("", END, values=row, tags=("row",))

        #style rows
        style = ttk.Style(visitor_page)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table2.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table2.grid(row=5, column=1, columnspan=7)

        self._table2.bind("<<TreeviewSelect>>", self._disable_selection)

    def _on_go_to_order_page(self):
        self._order_page_management.setTicket(self._ticket)
        self._order_page_management.get_page().tkraise()

    def _disable_selection(self, event=None):
        event.widget.selection_remove(event.widget.selection())

    def set_order_page_management(self, order_page_management):
        self._order_page_management = order_page_management

    def _add_credit(self):
        self._database.add_credit_for_ticket(self._ticket, 10)

        credit_txt = "Guthaben: " + str(self._database.get_credit_for_ticket(self._ticket)) + "€"
        self._credit_label.config(text=credit_txt) 
    
    
    def _unlock_ticket_for_friend(self):
        selected = self._table.focus()
        if not selected:
            return
        values = self._table.item(selected, "values")
        friend_ticket = self._friend_ticket_val.get()

        self._database.connect_order_to_ticket(values[3], friend_ticket)

    def _open_popup(self, event=None):
        #get selection
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        #create a popup window
        popup = Toplevel(self._visitor_page)
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
        self._table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        #fill rows
        data = []
        positions = self._database.get_positions_for_order(selected_order[3])
        special_requests = self._database.get_special_requests_for_order(selected_order[3])

        for position in positions:
            data.append( (position["name"], position["quantity"]) )

        for i, row in enumerate(data):
            table.insert("", END, values=row, tags=("row",))

        #special requests label
        Label(popup, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0)
        Label(popup, text=special_requests, font=self._style_1).grid(row=3, column=0)
