from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from elements import PlaceholderEntry

class OrderPage():
    def __init__(self, root, database, style_1):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._order_page = ""
        self._ticket = "1234567"
        self._selected_stand = ""
        self._current_time = 0
        self._current_price = 0
        self._priority = False

    def getPage(self):
        if not self._order_page:
            #page
            order_page = Frame(self._root)

            #frames
            form_frame = Frame(order_page)
            form_frame.grid(row=1, column=0, columnspan=2)

            self.createColumns(order_page)
            self.createRows(order_page)
            self.loadImages()
            self.createPrioritySwitch(order_page)
            self.createStandTable(order_page)
            self.createBestellkarteTable(order_page)
            self.createWarenkorbTable(order_page)

            #labels
            self._ticket_label = Label(order_page, text="Ticket: 1234567", font=self._style_1)
            self._ticket_label.grid(row=0, column=1)
            self._credit_label = Label(order_page, text="Guthaben: 222€", font=self._style_1)
            self._credit_label.grid(row=0, column=6)

            self._time_label = Label(order_page, text="Wartezeit: 0", font=self._style_1)
            self._time_label.grid(row=5, column=1)
            self._price_label = Label(order_page, text="Gesamtpreis: 0€", font=self._style_1)
            self._price_label.grid(row=5, column=6)

            Label(order_page, image=self._logo_img, font=self._style_1).grid(row=9, column=7)
            Label(form_frame, text="⌕", font=self._style_1).grid(row=0, column=1)

            #buttons
            Button(order_page, text="€▷", command=lambda: self.addCredit(), font=self._style_1, background="#75E6DA").grid(row=0, column=7)
            Button(order_page, text="Abbrechen", command=lambda: self.onCancel(), font=self._style_1, background="#75E6DA").grid(row=8, column=2)
            Button(order_page, text="Bestellen", command=lambda: self.onOrder(), font=self._style_1, background="#75E6DA").grid(row=8, column=5)

            #input fields
            self._stand_val = StringVar()
            self._standIpt = PlaceholderEntry(form_frame, "Suche Stand", "grey", font=self._style_1, bg="#D4F1F4", textvariable=self._stand_val)
            self._standIpt.grid(row=0, column=0)
            self._standIpt.bind("<Return>", self.onSearchStand)

            self._special_requests_val = StringVar()
            self._special_requests_ipt = PlaceholderEntry(order_page, "Sonderwünsche", "grey", font=self._style_1, bg="#D4F1F4", textvariable=self._special_requests_val, width=50)
            self._special_requests_ipt.grid(row=6, column=1, columnspan=7)

            self._order_page = order_page
        return self._order_page
    
    def createColumns(self, order_page):
        order_page.grid_columnconfigure(0, weight=1)
        order_page.grid_columnconfigure(1, weight=1)
        order_page.grid_columnconfigure(2, weight=1)
        order_page.grid_columnconfigure(3, weight=1)
        order_page.grid_columnconfigure(4, weight=1)
        order_page.grid_columnconfigure(5, weight=1)
        order_page.grid_columnconfigure(6, weight=1)
        order_page.grid_columnconfigure(7, weight=1)
        order_page.grid_columnconfigure(8, weight=1)

    def createRows(self, order_page):
        order_page.grid_rowconfigure(0, weight=1)
        order_page.grid_rowconfigure(1, weight=1)
        order_page.grid_rowconfigure(2, weight=1)
        order_page.grid_rowconfigure(3, weight=1)
        order_page.grid_rowconfigure(4, weight=1)
        order_page.grid_rowconfigure(5, weight=1)
        order_page.grid_rowconfigure(6, weight=1)
        order_page.grid_rowconfigure(7, weight=1)
        order_page.grid_rowconfigure(8, weight=1)
        order_page.grid_rowconfigure(9, weight=1)

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

    def createPrioritySwitch(self, order_page):
        #create Frame 
        form_frame = Frame(order_page)
        form_frame.grid(row=7, column=2, columnspan=2)
        
        Label(form_frame, text="Priorisieren:", font=self._style_1).grid(row=0, column=0)
        self._prioritySwitch = Button(form_frame, image = self._off_img, bd = 0,command = self.switchPriority)
        self._prioritySwitch.grid(row=0, column=1)

    def switchPriority(self):
        if self._priority:
            self._prioritySwitch.config(image = self._off_img)
            self._priority = False
        else:
            self._prioritySwitch.config(image = self._on_img)
            self._priority = True

    def createStandTable(self, order_page):
        #frames
        form_frame = Frame(order_page)
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
        style = ttk.Style(order_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table.grid(row=1, column=0)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self.table.bind("<<TreeviewSelect>>", self.onSelectStand)

    def createBestellkarteTable(self, order_page):
        #frames
        form_frame = Frame(order_page)
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
        style = ttk.Style(order_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table2.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table2.grid(row=1, column=0)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self.table2.yview)
        self.table2.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self.table2.bind("<Double-1>", self.onAddOrderPosition)

    def createWarenkorbTable(self, order_page):
        #frames
        form_frame = Frame(order_page)
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
        style = ttk.Style(order_page)
        style.theme_use("default")

        # Header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        # Row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.table3.tag_configure("row", background="#D4F1F4")   # baby blue

        self.table3.grid(row=1, column=0)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self.table3.yview)
        self.table3.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self.table3.bind("<Double-1>", self.onRemoveOrderPosition)

    def setTicket(self, ticket):
        #check vip
        isVip = self._database.readData()["Tickets"][ticket]["vip"]

        ticketTxt = "Ticket: " + ticket
        if isVip:
            ticketTxt = ticketTxt + " ☆"
            self._prioritySwitch.config(state="active") 
        else:
            self._prioritySwitch.config(state="disabled") 
        self._ticket_label.config(text=ticketTxt) 
        creditTxt = "Guthaben: " + str(self._database.getCreditForTicket(ticket)) + "€"
        self._credit_label.config(text=creditTxt) 
        self._ticket = ticket

    def onSearchStand(self, event=None):
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

    def onSelectStand(self, event=None):
        selected = self.table.focus()
        if not selected:
            return
        selected_stand = self.table.item(selected, "values")[0]

        #clear existing rows
        self.table2.delete(*self.table2.get_children())
        # Insert sample data
        data = []
        ids = []
        products = self._database.getProductsForStand(selected_stand)

        for product in products:
            data.append( (product["name"], product["time"], product["price"], product["quantity"]) )
            ids.append(product["product"])

        for i, row in enumerate(data):
            self.table2.insert("", END, iid=ids[i], values=row, tags=("row",))

        self._selected_stand = selected_stand
        self.clearWarenkorb()

    def clearWarenkorb(self):
        self._current_time = 0
        self._current_price = 0

        #clear existing rows
        self.table3.delete(*self.table3.get_children())

    def onAddOrderPosition(self, event=None):
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
                current_time = int(item[1])
                newTime = current_time + ( current_time // currentQuantity) 
                #update price
                current_price = int(item[2])
                newPrice = current_price + ( current_price // currentQuantity)
                #update quantity
                newQuantity = currentQuantity + 1

                #update table
                newItem = (item[0], newTime, newPrice, newQuantity)
                self.table3.item(selected, values=newItem)

                #update time/price
                self._current_time += current_time // currentQuantity
                self._current_price += current_price // currentQuantity

        
        if not found:
            products = self._database.getProductsForStand(self._selected_stand)
            for product in products:
                if selected == product["product"]:
                    newRow = (product["name"], product["time"], product["price"], 1)
                    self.table3.insert("", END, iid=selected, values=newRow, tags=("row",))

                    #update time/price
                    self._current_time += product["time"]
                    self._current_price += product["price"]

        self.updateTimePriceLabels()

    def updateTimePriceLabels(self):
        timeTxt = "Wartezeit: " + str(self._current_time)
        self._time_label.config(text=timeTxt)
        priceTxt = "Gesamtpreis: " + str(self._current_price) + "€"
        self._price_label.config(text=priceTxt) 

    def onRemoveOrderPosition(self, event=None):
        selected = self.table3.focus()
        if not selected:
            return
        selectedProduct = self.table3.item(selected, "values")

        #update warenkorb
        if selectedProduct[3] == "1":
            self.table3.delete(selected)

            #update time/price
            currentQuantity = int(selectedProduct[3])
            current_time = int(selectedProduct[1])
            current_price = int(selectedProduct[2])
            
            self._current_time -= current_time // currentQuantity
            self._current_price -= current_price // currentQuantity
        else:
            currentQuantity = int(selectedProduct[3])
            #update time
            current_time = int(selectedProduct[1])
            newTime = current_time - ( current_time // currentQuantity) 
            #update price
            current_price = int(selectedProduct[2])
            newPrice = current_price - ( current_price // currentQuantity)
            #update quantity
            newQuantity = currentQuantity - 1

            #update table
            newItem = (selectedProduct[0], newTime, newPrice, newQuantity)
            self.table3.item(selected, values=newItem)

            #update time/price
            self._current_time -= current_time // currentQuantity
            self._current_price -= current_price // currentQuantity

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

        #clear input fields
        self._stand_val.set("")
        self._special_requests_val.set("")

        #reset time/price
        self._current_time = 0
        self._current_price = 0
        self._priority = False

        self._visitor_page_management.fillOrderTableRows(self._ticket)
        self._visitor_page_management.getPage().tkraise()

    def onOrder(self):
        #not enough credit
        if self._current_price > self._database.getCreditForTicket(self._ticket):
            return

        orderPositions = []
        warenkorbItems = self.table3.get_children()

        #special requests
        special_requests = ""
        if self._special_requests_val.get() != "Sonderwünsche":
            special_requests = self._special_requests_val.get()

        if warenkorbItems:
            for itemID in warenkorbItems:
                item = self.table3.item(itemID, "values")
                orderPositions.append({"product": itemID, "quantity": int(item[3])})

            self._database.placeOrder(self._selected_stand, self._ticket, orderPositions, self._current_price, special_requests)
        self.onCancel()

    def setVisitorPageManagement(self, visitor_page_management):
        self._visitor_page_management = visitor_page_management

    def addCredit(self):
        self._database.addCreditForTicket(self._ticket, 10)

        creditTxt = "Guthaben: " + str(self._database.getCreditForTicket(self._ticket)) + "€"
        self._credit_label.config(text=creditTxt) 

