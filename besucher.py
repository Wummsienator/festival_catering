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

            self.createColumns(besucherPage)
            self.createRows(besucherPage)
            self.loadImages()
            self.createOrderTable(besucherPage)

            #frames
            form_frame = Frame(besucherPage)
            form_frame.grid(row=2, column=6, columnspan=2)

            #labels
            ticketLabel = Label(besucherPage, text="Ticket: 1234567", font=self._style1).grid(row=0, column=1)
            creditLabel = Label(besucherPage, text="Guthaben: 222€", font=self._style1).grid(row=0, column=6)

            friendTicketLabel = Label(form_frame, text="Ticket Freund:", font=self._style1).grid(row=0, column=0)

            qrLabel = Label(besucherPage, image=self._qr_img, font=self._style1).grid(row=3, column=1)

            #buttons
            creditBtn =  Button(besucherPage, text="C", command=lambda: print("test"), font=self._style1, background="#75E6DA").grid(row=0, column=7)
            orderBtn = Button(besucherPage, text="Bestellung aufnehmen", command=lambda: print("test"), font=self._style1, background="#75E6DA").grid(row=2, column=1)
            friendOrderBtn = Button(form_frame, text="Bestellung freischalten", command=lambda: print("test"), font=self._style1, background="#75E6DA").grid(row=2, column=1)

            #input fields
            testVal = "Hallo"
            friendIpt = Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=testVal).grid(row=0, column=1)

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
        logo_pil = Image.open("logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        qr_pil = Image.open("QR_Code.png")
        qr_pil = qr_pil.resize((150, 150), Image.Resampling.LANCZOS)
        self._qr_img = ImageTk.PhotoImage(qr_pil)
    
    def createOrderTable(self, besucherPage):
        # Title label
        title = Label(
            besucherPage,
            text="Offene Bestellungen:",
            font=("Arial", 14, "bold"),
            bg="#05445E",   # dark teal background
            fg="white"
        )
        #title.pack(fill="x")

        # Define table columns
        columns = ("Stand", "Wartezeit", "Status", "Bestellungsnummer")
        self.table = ttk.Treeview(besucherPage, columns=columns, show="headings", selectmode="browse", height=3)

        # Define headings
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=180)

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
        #self.table.pack(expand=True, fill="both", padx=5, pady=5)

        self.table.grid(row=1, column=1, columnspan=7)

        self.table.bind("<<TreeviewSelect>>", self.on_select)
    
    def on_select(self, event):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        print("Selected row:", values)
