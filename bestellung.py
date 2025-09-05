from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class BestellungPage():
    def __init__(self, root, database, style1):
        self._root = root
        self._database = database
        self._style1 = style1
        self._bestellungPage = ""
        self._ticket = "1234567"
        self._selectedStand = ""
        self._currentTime = 0
        self._currentPrice = 0
        self._priority = False

    def getPage(self):
        if not self._bestellungPage:
            #page
            bestellungPage = Frame(self._root)

            #frames
            form_frame = Frame(bestellungPage)
            form_frame.grid(row=1, column=0, columnspan=2)

            self.createColumns(bestellungPage)
            self.createRows(bestellungPage)
            self.loadImages()
            self.createPrioritySwitch(bestellungPage)
            self.createStandTable(bestellungPage)
            self.createBestellkarteTable(bestellungPage)
            self.createWarenkorbTable(bestellungPage)

            #labels
            self._ticketLabel = Label(bestellungPage, text="Ticket: 1234567", font=self._style1)
            self._ticketLabel.grid(row=0, column=1)
            self._creditLabel = Label(bestellungPage, text="Guthaben: 222€", font=self._style1)
            self._creditLabel.grid(row=0, column=6)

            self._timeLabel = Label(bestellungPage, text="Wartezeit: 0", font=self._style1)
            self._timeLabel.grid(row=5, column=1)
            self._priceLabel = Label(bestellungPage, text="Gesamtpreis: 0€", font=self._style1)
            self._priceLabel.grid(row=5, column=6)

            Label(bestellungPage, image=self._logo_img, font=self._style1).grid(row=8, column=7)
            Label(form_frame, text="⌕", font=self._style1).grid(row=0, column=1)

            #buttons
            Button(bestellungPage, text="€▷", command=lambda: print("test"), font=self._style1, background="#75E6DA").grid(row=0, column=7)
            Button(bestellungPage, text="Abbrechen", command=lambda: self.onCancel(), font=self._style1, background="#75E6DA").grid(row=7, column=2)
            Button(bestellungPage, text="Bestellen", command=lambda: self.onOrder(), font=self._style1, background="#75E6DA").grid(row=7, column=5)

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
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((50, 50), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        on_pil = Image.open("img/on.png")
        on_pil = on_pil.resize((50, 25), Image.Resampling.LANCZOS)
        self._on_img = ImageTk.PhotoImage(on_pil)

        off_pil = Image.open("img/off.png")
        off_pil = off_pil.resize((50, 25), Image.Resampling.LANCZOS)
        self._off_img = ImageTk.PhotoImage(off_pil)

    def createPrioritySwitch(self, bestellungPage):
        #create Frame 
        form_frame = Frame(bestellungPage)
        form_frame.grid(row=6, column=2, columnspan=2)
        
        Label(form_frame, text="Priorisieren:", font=self._style1).grid(row=0, column=0)
        self._prioritySwitch = Button(form_frame, image = self._off_img, bd = 0,command = self.switchPriority)
        self._prioritySwitch.grid(row=0, column=1)

    def switchPriority(self):
        if self._priority:
            self._prioritySwitch.config(image = self._off_img)
            self._priority = False
        else:
            self._prioritySwitch.config(image = self._on_img)
            self._priority = True

    def createStandTable(self, bestellungPage):
        #frames
        form_frame = Frame(bestellungPage)
        form_frame.grid(row=2, column=0, columnspan=3)

        # Title label
        title = Label(
            form_frame,
            text="Stand Auswahl:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=30
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

    def createWarenkorbTable(self, bestellungPage):
        #frames
        form_frame = Frame(bestellungPage)
        form_frame.grid(row=4, column=1, columnspan=7)

        # Title label
        title = Label(
            form_frame,
            text="Warenkorb:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        # Define table columns
        columns = ("Name", "Wartezeit", "Preis", "Menge")
        self.table3 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=4)

        # Define headings
        for col in columns:
            self.table3.heading(col, text=col)
            self.table3.column(col, anchor="center", width=180)

        # Style rows
        style = ttk.Style(bestellungPage)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table3.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table3.grid(row=1, column=0)

        self.table3.bind("<Double-1>", self.onRemoveOrderPosition)

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
        if not selected:
            return
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

        self._selectedStand = selectedStand
        self.clearWarenkorb()

    def clearWarenkorb(self):
        self._currentTime = 0
        self._currentPrice = 0

        #clear existing rows
        self.table3.delete(*self.table3.get_children())

    def onAddOrderPosition(self, event):
        selected = self.table2.focus()
        if not selected:
            return
        selectedProduct = self.table2.item(selected, "values")

        #check available quantity
        if selectedProduct[3] == "0":
            return
        
        #update available cquantity
        updatedRow = (selectedProduct[0], selectedProduct[1], selectedProduct[2], int(selectedProduct[3]) - 1)
        self.table2.item(selected, values=updatedRow)

        #update warenkorb
        found = False
        itemIDs = self.table3.get_children()
        for id in itemIDs:
            if id == selected:
                found = True
                item = self.table3.item(id, "values")
                currentQuantity = int(item[3])
                #update time
                currentTime = int(item[1])
                newTime = currentTime + ( currentTime // currentQuantity) 
                #update price
                currentPrice = int(item[2])
                newPrice = currentPrice + ( currentPrice // currentQuantity)
                #update quantity
                newQuantity = currentQuantity + 1

                #update table
                newItem = (item[0], newTime, newPrice, newQuantity)
                self.table3.item(selected, values=newItem)

                #update time/price
                self._currentTime += currentTime // currentQuantity
                self._currentPrice += currentPrice // currentQuantity

        
        if not found:
            products = self._database.getProductsForStand(self._selectedStand)
            for product in products:
                if selected == product["product"]:
                    newRow = (product["name"], product["time"], product["price"], 1)
                    self.table3.insert("", END, iid=selected, values=newRow, tags=("row",))

                    #update time/price
                    self._currentTime += product["time"]
                    self._currentPrice += product["price"]

        self.updateTimePriceLabels()

    def updateTimePriceLabels(self):
        timeTxt = "Wartezeit: " + str(self._currentTime)
        self._timeLabel.config(text=timeTxt)
        priceTxt = "Gesamtpreis: " + str(self._currentPrice) + "€"
        self._priceLabel.config(text=priceTxt) 

    def onRemoveOrderPosition(self, event):
        selected = self.table3.focus()
        if not selected:
            return
        selectedProduct = self.table3.item(selected, "values")

        #update warenkorb
        if selectedProduct[3] == "1":
            self.table3.delete(selected)

            #update time/price
            currentQuantity = int(selectedProduct[3])
            currentTime = int(selectedProduct[1])
            currentPrice = int(selectedProduct[2])
            
            self._currentTime -= currentTime // currentQuantity
            self._currentPrice -= currentPrice // currentQuantity
        else:
            currentQuantity = int(selectedProduct[3])
            #update time
            currentTime = int(selectedProduct[1])
            newTime = currentTime - ( currentTime // currentQuantity) 
            #update price
            currentPrice = int(selectedProduct[2])
            newPrice = currentPrice - ( currentPrice // currentQuantity)
            #update quantity
            newQuantity = currentQuantity - 1

            #update table
            newItem = (selectedProduct[0], newTime, newPrice, newQuantity)
            self.table3.item(selected, values=newItem)

            #update time/price
            self._currentTime -= currentTime // currentQuantity
            self._currentPrice -= currentPrice // currentQuantity

        #update available quantity
        bestellkarteItem = self.table2.item(selected, "values")
        updatedRow = (bestellkarteItem[0], bestellkarteItem[1], bestellkarteItem[2], int(bestellkarteItem[3]) + 1)
        self.table2.item(selected, values=updatedRow)

        self.updateTimePriceLabels()

    def onCancel(self):
        self.clearWarenkorb()

        #clear tables
        self.table.delete(*self.table.get_children())
        self.table2.delete(*self.table2.get_children())
        self.table3.delete(*self.table3.get_children())

        #reset time/price
        self._currentTime = 0
        self._currentPrice = 0
        self._priority = False

        self._besucherPageManagement.fillOrderTableRows(self._ticket)
        self._besucherPageManagement.getPage().tkraise()

    def onOrder(self):
        orderPositions = []
        warenkorbItems = self.table3.get_children()

        if warenkorbItems:
            for itemID in warenkorbItems:
                item = self.table3.item(itemID, "values")
                orderPositions.append({"product": itemID, "quantity": int(item[3])})

            self._database.placeOrder(self._selectedStand, self._ticket, orderPositions, self._currentPrice)
        self.onCancel()

    def setBesucherPageManagement(self, besucherPageManagement):
        self._besucherPageManagement = besucherPageManagement
