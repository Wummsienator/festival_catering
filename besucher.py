from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class BesucherPage():
    def __init__(self, root, database, style1):
        self._root = root
        self._database = database
        self._style1 = style1
        self._besucherPage = ""
        self._ticket = "1234567"

        self._bestellungPage = Frame(root)

    def getPage(self):
        if not self._besucherPage:
            #page
            besucherPage = Frame(self._root)

            self.createColumns(besucherPage)
            self.createRows(besucherPage)
            self.loadImages()
            self.createOrderTable(besucherPage)
            self.createNotificationTable(besucherPage)

            #frames
            form_frame = Frame(besucherPage)
            form_frame.grid(row=2, column=6, columnspan=2)

            #labels
            self._ticketLabel = Label(besucherPage, text="Ticket: 1234567", font=self._style1)
            self._ticketLabel.grid(row=0, column=1)
            self._creditLabel = Label(besucherPage, text="Guthaben: 222€", font=self._style1)
            self._creditLabel.grid(row=0, column=6)

            Label(form_frame, text="Ticket Freund:", font=self._style1).grid(row=0, column=0)

            Label(besucherPage, image=self._qr_img, font=self._style1).grid(row=3, column=1)

            Label(besucherPage, image=self._logo_img, font=self._style1).grid(row=6, column=7)

            #buttons
            Button(besucherPage, text="€▷", command=lambda: self.addCredit(), font=self._style1, background="#75E6DA").grid(row=0, column=7)
            Button(besucherPage, text="Bestellung aufnehmen", command=lambda: self.onGoToBestellungPage(), font=self._style1, background="#75E6DA").grid(row=2, column=1)
            Button(form_frame, text="Bestellung freischalten", command=lambda: print("test"), font=self._style1, background="#75E6DA").grid(row=2, column=1)

            #input fields
            testVal = "Hallo"
            Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=testVal).grid(row=0, column=1)

            self._besucherPage  = besucherPage
        return self._besucherPage
    
    def createColumns(self, besucherPage):
        besucherPage.grid_columnconfigure(0, weight=1)
        besucherPage.grid_columnconfigure(1, weight=1)
        besucherPage.grid_columnconfigure(2, weight=1)
        besucherPage.grid_columnconfigure(3, weight=1)
        besucherPage.grid_columnconfigure(4, weight=1)
        besucherPage.grid_columnconfigure(5, weight=1)
        besucherPage.grid_columnconfigure(6, weight=1)
        besucherPage.grid_columnconfigure(7, weight=1)
        besucherPage.grid_columnconfigure(8, weight=1)

    def createRows(self, besucherPage):
        besucherPage.grid_rowconfigure(0, weight=1)
        besucherPage.grid_rowconfigure(1, weight=1)
        besucherPage.grid_rowconfigure(2, weight=1)
        besucherPage.grid_rowconfigure(3, weight=1)
        besucherPage.grid_rowconfigure(4, weight=1)
        besucherPage.grid_rowconfigure(5, weight=1)
        besucherPage.grid_rowconfigure(6, weight=1)
    
    def loadImages(self):
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        qr_pil = Image.open("img/QR_Code.png")
        qr_pil = qr_pil.resize((150, 150), Image.Resampling.LANCZOS)
        self._qr_img = ImageTk.PhotoImage(qr_pil)
    
    def createOrderTable(self, besucherPage):
        #frames
        form_frame = Frame(besucherPage)
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
        self.table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(besucherPage)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table.grid(row=1, column=0)

        self.table.bind("<<TreeviewSelect>>", self.on_select)
    
    def fillOrderTableRows(self, ticket):
        #clear existing rows
        self.table.delete(*self.table.get_children())
        # Insert sample data
        data = []
        orders = self._database.getOrdersForTicket(ticket)
        for order in orders:
            data.append( (order["stand"], order["time"], order["status_desc"], order["order"]) )

        for i, row in enumerate(data):
            self.table.insert("", END, values=row, tags=("row",))

        #check vip
        isVip = self._database.readData()["Tickets"][ticket]["vip"]

        ticketTxt = "Ticket: " + ticket
        if isVip:
            ticketTxt = ticketTxt + " ☆"
        self._ticketLabel.config(text=ticketTxt) 
        creditTxt = "Guthaben: " + str(self._database.getCreditForTicket(ticket)) + "€"
        self._creditLabel.config(text=creditTxt) 

        #update ticket
        self._ticket = ticket

    def createNotificationTable(self, besucherPage):
        # Define table columns
        column = "Benachrichtigungen:"
        self.table2 = ttk.Treeview(besucherPage, columns=column, show="headings", selectmode="browse", height=3)

        # Define headings
        self.table2.heading(column, text=column)
        self.table2.column(column, anchor="center", width=600)

        # Insert sample data
        data = [("Deine Bestellung kann in 20 Minuten an Stand 1 abgeholt werden.", ), ("Deine Bestellung an Stand 3 ist abholbereit", )]
        for i, row in enumerate(data):
            self.table2.insert("", END, values=row, tags=("row",))

        # Style rows
        style = ttk.Style(besucherPage)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table2.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table2.grid(row=5, column=1, columnspan=7)

        self.table2.bind("<<TreeviewSelect>>", self.disable_selection)
    
    def on_select(self, event):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        print("Selected row:", values)

    def onGoToBestellungPage(self):
        self._bestellungPageManagement.setTicket(self._ticket)
        self._bestellungPageManagement.getPage().tkraise()

    def disable_selection(self, event):
        event.widget.selection_remove(event.widget.selection())

    def setBestellungPageManagement(self, bestellungPageManagement):
        self._bestellungPageManagement = bestellungPageManagement

    def addCredit(self):
        self._database.addCreditForTicket(self._ticket, 10)

        creditTxt = "Guthaben: " + str(self._database.getCreditForTicket(self._ticket)) + "€"
        self._creditLabel.config(text=creditTxt) 

