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

    def getPage(self):
        if not self._visitor_page:
            #page
            visitor_page = Frame(self._root)

            self.createColumns(visitor_page)
            self.createRows(visitor_page)
            self.loadImages()
            self.createOrderTable(visitor_page)
            self.createNotificationTable(visitor_page)

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
            Button(visitor_page, text="€▷", command=lambda: self.addCredit(), font=self._style_1, background="#75E6DA").grid(row=0, column=7)
            Button(visitor_page, text="Bestellung aufnehmen", command=lambda: self.onGoToOrderPage(), font=self._style_1, background="#75E6DA").grid(row=2, column=1)
            Button(form_frame, text="Bestellung freischalten", command=lambda: self.unlockTicketForFriend(), font=self._style_1, background="#75E6DA").grid(row=2, column=1)

            #input fields
            self._friend_ticket_val = StringVar()
            Entry(form_frame, font=self._style_1, bg="#D4F1F4", textvariable=self._friend_ticket_val).grid(row=0, column=1)

            self._visitor_page  = visitor_page
        return self._visitor_page
    
    def createColumns(self, visitor_page):
        visitor_page.grid_columnconfigure(0, weight=1)
        visitor_page.grid_columnconfigure(1, weight=1)
        visitor_page.grid_columnconfigure(2, weight=1)
        visitor_page.grid_columnconfigure(3, weight=1)
        visitor_page.grid_columnconfigure(4, weight=1)
        visitor_page.grid_columnconfigure(5, weight=1)
        visitor_page.grid_columnconfigure(6, weight=1)
        visitor_page.grid_columnconfigure(7, weight=1)
        visitor_page.grid_columnconfigure(8, weight=1)

    def createRows(self, visitor_page):
        visitor_page.grid_rowconfigure(0, weight=1)
        visitor_page.grid_rowconfigure(1, weight=1)
        visitor_page.grid_rowconfigure(2, weight=1)
        visitor_page.grid_rowconfigure(3, weight=1)
        visitor_page.grid_rowconfigure(4, weight=1)
        visitor_page.grid_rowconfigure(5, weight=1)
        visitor_page.grid_rowconfigure(6, weight=1)
    
    def loadImages(self):
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        qr_pil = Image.open("img/QR_Code.png")
        qr_pil = qr_pil.resize((150, 150), Image.Resampling.LANCZOS)
        self._qr_img = ImageTk.PhotoImage(qr_pil)
    
    def createOrderTable(self, visitor_page):
        #frames
        form_frame = Frame(visitor_page)
        form_frame.grid(row=1, column=1, columnspan=7)

        # Title label
        title = Label(
            form_frame,
            text="Offene Bestellungen:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Stand", "Wartezeit", "Status", "Bestellungsnummer")
        self._table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self._table.heading(col, text=col)
            self._table.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(visitor_page)
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
    
    def fillOrderTableRows(self, ticket):
        #clear existing rows
        self._table.delete(*self._table.get_children())
        # Insert sample data
        data = []
        orders = self._database.getOrdersForTicket(ticket)
        for order in orders:
            data.append( (order["stand"], order["time"], order["status_desc"], order["order"]) )

        for i, row in enumerate(data):
            self._table.insert("", END, values=row, tags=("row",))

        #check vip
        is_vip = self._database.readData()["Tickets"][ticket]["vip"]

        ticket_txt = "Ticket: " + ticket
        if is_vip:
            ticket_txt = ticket_txt + " ☆"
        self._ticket_label.config(text=ticket_txt) 
        credit_txt = "Guthaben: " + str(self._database.getCreditForTicket(ticket)) + "€"
        self._credit_label.config(text=credit_txt) 

        #update ticket
        self._ticket = ticket

    def createNotificationTable(self, visitor_page):
        # Define table columns
        column = "Benachrichtigungen:"
        self._table2 = ttk.Treeview(visitor_page, columns=column, show="headings", selectmode="browse", height=3)

        # Define headings
        self._table2.heading(column, text=column)
        self._table2.column(column, anchor="center", width=600)

        # Insert sample data
        data = [("Deine Bestellung kann in 20 Minuten an Stand 1 abgeholt werden.", ), ("Deine Bestellung an Stand 3 ist abholbereit", )]
        for i, row in enumerate(data):
            self._table2.insert("", END, values=row, tags=("row",))

        # Style rows
        style = ttk.Style(visitor_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table2.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table2.grid(row=5, column=1, columnspan=7)

        self._table2.bind("<<TreeviewSelect>>", self.disable_selection)

    def onGoToOrderPage(self):
        self._order_page_management.setTicket(self._ticket)
        self._order_page_management.getPage().tkraise()

    def disable_selection(self, event=None):
        event.widget.selection_remove(event.widget.selection())

    def setOrderPageManagement(self, order_page_management):
        self._order_page_management = order_page_management

    def addCredit(self):
        self._database.addCreditForTicket(self._ticket, 10)

        credit_txt = "Guthaben: " + str(self._database.getCreditForTicket(self._ticket)) + "€"
        self._credit_label.config(text=credit_txt) 
    
    
    def unlockTicketForFriend(self):
        selected = self._table.focus()
        if not selected:
            return
        values = self._table.item(selected, "values")
        friend_ticket = self._friend_ticket_val.get()

        self._database.connectOrderToTicket(values[3], friend_ticket)

    def open_popup(self, event=None):
        #get selection
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        # Create a popup window
        popup = Toplevel(self._visitor_page)
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
        self._table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        #fill rows
        data = []
        positions, special_requests = self._database.getPositionsForOrder(selected_order[0])

        for position in positions:
            data.append( (position["name"], position["quantity"]) )

        for i, row in enumerate(data):
            table.insert("", END, values=row, tags=("row",))

        #special requests labe
        Label(popup, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0)
        Label(popup, text=special_requests, font=self._style_1).grid(row=3, column=0)
