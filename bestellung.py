from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class BestellungPage():
    def __init__(self, root, database, style1):
        self._root = root
        self._database = database
        self._style1 = style1
        self._bestellungPage = ""
        self._ticket = ""

    def getPage(self):
        if not self._bestellungPage:
            #page
            bestellungPage = Frame(self._root)

            #frames
            form_frame = Frame(bestellungPage)
            form_frame.grid(row=1, column=1, columnspan=2)

            self.createColumns(bestellungPage)
            self.createRows(bestellungPage)
            self.loadImages()
            self.createStandTable(bestellungPage)
            self.createBestellkarteTable(bestellungPage)

            #labels
            self._ticketLabel = Label(bestellungPage, text="Ticket: 1234567", font=self._style1)
            self._ticketLabel.grid(row=0, column=1)
            self._creditLabel = Label(bestellungPage, text="Guthaben: 222€", font=self._style1)
            self._creditLabel.grid(row=0, column=6)

            Label(bestellungPage, image=self._logo_img, font=self._style1).grid(row=6, column=7)
            Label(form_frame, text="⌕", font=self._style1).grid(row=0, column=1)

            #buttons
            Button(bestellungPage, text="€▷", command=lambda: print("test"), font=self._style1, background="#75E6DA").grid(row=0, column=7)

            #input fields
            self._stand_val = StringVar()
            self._standIpt = Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=self._stand_val)
            self._standIpt.grid(row=0, column=0)
            self._standIpt.bind("<Return>", self.onSearchStand)

            self._bestellungPage = bestellungPage
        return self._bestellungPage
    
    def createColumns(self, bestellungPage):
        bestellungPage.grid_columnconfigure(0, weight=1)
        bestellungPage.grid_columnconfigure(1, weight=1)
        bestellungPage.grid_columnconfigure(2, weight=1)
        bestellungPage.grid_columnconfigure(3, weight=1)
        bestellungPage.grid_columnconfigure(4, weight=1)
        bestellungPage.grid_columnconfigure(5, weight=1)
        bestellungPage.grid_columnconfigure(6, weight=1)
        bestellungPage.grid_columnconfigure(7, weight=1)
        bestellungPage.grid_columnconfigure(8, weight=1)

    def createRows(self, bestellungPage):
        bestellungPage.grid_rowconfigure(0, weight=1)
        bestellungPage.grid_rowconfigure(1, weight=1)
        bestellungPage.grid_rowconfigure(2, weight=1)
        bestellungPage.grid_rowconfigure(3, weight=1)
        bestellungPage.grid_rowconfigure(4, weight=1)
        bestellungPage.grid_rowconfigure(5, weight=1)
        bestellungPage.grid_rowconfigure(6, weight=1)
        bestellungPage.grid_rowconfigure(7, weight=1)
        bestellungPage.grid_rowconfigure(8, weight=1)

    def loadImages(self):
        logo_pil = Image.open("logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

    def createStandTable(self, bestellungPage):
        #frames
        form_frame = Frame(bestellungPage)
        form_frame.grid(row=2, column=1, columnspan=7)

        # Title label
        title = Label(
            form_frame,
            text="Stand Auswahl:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Nummer", "Name")
        self.table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(bestellungPage)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table.grid(row=1, column=0)

        self.table.bind("<<TreeviewSelect>>", self.onSelectStand)

    def createBestellkarteTable(self, bestellungPage):
        #frames
        form_frame = Frame(bestellungPage)
        form_frame.grid(row=3, column=1, columnspan=7)

        # Title label
        title = Label(
            form_frame,
            text="Bestellkarte:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Name", "Wartezeit", "Preis", "Lagerbestand")
        self.table2 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=4)

        # Define headings
        for col in columns:
            self.table2.heading(col, text=col)
            self.table2.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(bestellungPage)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table2.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table2.grid(row=1, column=0)

        self.table2.bind("<Double-1>", self.onAddOrderPosition)

    def setTicket(self, ticket):
        ticketTxt = "Ticket: " + ticket
        self._ticketLabel.config(text=ticketTxt) 
        creditTxt = "Guthaben: " + str(self._database.getCreditForTicket(ticket)) + "€"
        self._creditLabel.config(text=creditTxt) 

    def onSearchStand(self, event):
        standStr = self._stand_val.get()

        #clear existing rows
        self.table.delete(*self.table.get_children())
        # Insert sample data
        data = []
        stands = self._database.searchStand(standStr)

        for stand in stands:
            data.append( (stand["stand"], stand["name"]) )

        for i, row in enumerate(data):
            self.table.insert("", END, values=row, tags=("row",))

    def onSelectStand(self, event):
        selected = self.table.focus()
        selectedStand = self.table.item(selected, "values")[0]

        #clear existing rows
        self.table2.delete(*self.table2.get_children())
        # Insert sample data
        data = []
        ids = []
        products = self._database.getProductsForStand(selectedStand)

        for product in products:
            data.append( (product["name"], product["time"], product["price"], product["quantity"]) )
            ids.append(product["product"])

        for i, row in enumerate(data):
            self.table2.insert("", END, iid=ids[i], values=row, tags=("row",))

    def onAddOrderPosition(self, event):
        selected = self.table2.focus()
        selectedProduct = self.table2.item(selected, "values")

        print(selectedProduct)
