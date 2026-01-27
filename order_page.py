from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from elements import PlaceholderEntry
from decimal import *

class OrderPage():
    def __init__(self, root, database, style_1, scaling):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._scaling = scaling
        self._order_page = None
        self._ticket = None
        self._selected_stand = None
        self._current_time = 0
        self._current_price = Decimal(0.00)
        self._priority = False

    def get_page(self):
        if not self._order_page:
            #page
            order_page = Frame(self._root)

            #frames
            form_frame = Frame(order_page)
            form_frame.grid(row=1, column=0, columnspan=2)

            self._create_columns(order_page)
            self._create_rows(order_page)
            self._load_images()
            self._create_priority_switch(order_page)
            self._create_stand_table(order_page)
            self._create_bestellkarte_table(order_page)
            self._create_warenkorb_table(order_page)

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
            Button(order_page, text="€▷", command=lambda: self._add_credit(), font=self._style_1, background="#75E6DA").grid(row=0, column=7)
            Button(order_page, text="Abbrechen", command=lambda: self._on_cancel(), font=self._style_1, background="#75E6DA").grid(row=8, column=2)
            Button(order_page, text="Bestellen", command=lambda: self._on_order(), font=self._style_1, background="#75E6DA").grid(row=8, column=5)

            #input fields
            self._stand_val = StringVar()
            self._stand_ipt = PlaceholderEntry(form_frame, "Suche Stand", "grey", font=self._style_1, bg="#D4F1F4", textvariable=self._stand_val)
            self._stand_ipt.grid(row=0, column=0)
            self._stand_ipt.bind("<Return>", self._on_search_stand)

            self._special_requests_val = StringVar()
            self._special_requests_ipt = PlaceholderEntry(order_page, "Sonderwünsche", "grey", font=self._style_1, bg="#D4F1F4", textvariable=self._special_requests_val, width=50)
            self._special_requests_ipt.grid(row=6, column=1, columnspan=7)

            self._order_page = order_page
        return self._order_page
    
    def _create_columns(self, order_page):
        order_page.grid_columnconfigure(0, weight=1)
        order_page.grid_columnconfigure(1, weight=1)
        order_page.grid_columnconfigure(2, weight=1)
        order_page.grid_columnconfigure(3, weight=1)
        order_page.grid_columnconfigure(4, weight=1)
        order_page.grid_columnconfigure(5, weight=1)
        order_page.grid_columnconfigure(6, weight=1)
        order_page.grid_columnconfigure(7, weight=1)
        order_page.grid_columnconfigure(8, weight=1)

    def _create_rows(self, order_page):
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

    def _load_images(self):
        logo_pil = Image.open("img/logo.png")
        s_size = round(50 * self._scaling)
        s_size_2 = round(25 * self._scaling)
        logo_pil = logo_pil.resize((s_size, s_size), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        on_pil = Image.open("img/on.png")
        on_pil = on_pil.resize((s_size, s_size_2), Image.Resampling.LANCZOS)
        self._on_img = ImageTk.PhotoImage(on_pil)

        off_pil = Image.open("img/off.png")
        off_pil = off_pil.resize((s_size, s_size_2), Image.Resampling.LANCZOS)
        self._off_img = ImageTk.PhotoImage(off_pil)

    def _create_priority_switch(self, order_page):
        #create Frame 
        form_frame = Frame(order_page)
        form_frame.grid(row=7, column=2, columnspan=2)
        
        Label(form_frame, text="Priorisieren:", font=self._style_1).grid(row=0, column=0)
        self._priority_switch = Button(form_frame, image = self._off_img, bd = 0,command = self._switch_priority)
        self._priority_switch.grid(row=0, column=1)

    def _switch_priority(self):
        if self._priority:
            self._priority_switch.config(image = self._off_img)
            self._priority = False
        else:
            self._priority_switch.config(image = self._on_img)
            self._priority = True

    def _create_stand_table(self, order_page):
        #frames
        form_frame = Frame(order_page)
        form_frame.grid(row=2, column=0, columnspan=3)

        #title label
        title = Label(
            form_frame,
            text="Stand Auswahl:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=30
        )
        title.grid(row=0, column=0)

        #define table columns
        columns = ("Nummer", "Name")
        self._table = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=3)

        #define headings
        for col in columns:
            self._table.heading(col, text=col)
            self._table.column(col, anchor="center", width=180)

        #style rows
        style = ttk.Style(order_page)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table.grid(row=1, column=0)

        #vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self._table.bind("<<TreeviewSelect>>", self._on_select_stand)

    def _create_bestellkarte_table(self, order_page):
        #frames
        form_frame = Frame(order_page)
        form_frame.grid(row=3, column=1, columnspan=7)

        #title label
        title = Label(
            form_frame,
            text="Bestellkarte:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        #define table columns
        columns = ("Name", "Wartezeit", "Preis", "Lagerbestand")
        self._table_2 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=4)

        #define headings
        for col in columns:
            self._table_2.heading(col, text=col)
            self._table_2.column(col, anchor="center", width=180)

        #style rows
        style = ttk.Style(order_page)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table_2.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table_2.grid(row=1, column=0)

        #vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table_2.yview)
        self._table_2.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self._table_2.bind("<Double-1>", self._on_add_order_position)

    def _create_warenkorb_table(self, order_page):
        #frames
        form_frame = Frame(order_page)
        form_frame.grid(row=4, column=1, columnspan=7)

        #title label
        title = Label(
            form_frame,
            text="Warenkorb:",
            font=("Arial", 14, "bold"),
            bg="#05445E",
            fg="white",
            width=60
        )
        title.grid(row=0, column=0)

        #define table columns
        columns = ("Name", "Wartezeit", "Preis", "Menge")
        self._table_3 = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="browse", height=4)

        #define headings
        for col in columns:
            self._table_3.heading(col, text=col)
            self._table_3.column(col, anchor="center", width=180)

        #style rows
        style = ttk.Style(order_page)
        style.theme_use("default")

        #header style
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#05445E", foreground="white")

        #row styles
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self._table_3.tag_configure("row", background="#D4F1F4")   # baby blue

        self._table_3.grid(row=1, column=0)

        #vertical scrollbar
        vsb = ttk.Scrollbar(form_frame, orient="vertical", command=self._table_3.yview)
        self._table_3.configure(yscrollcommand=vsb.set)
        vsb.grid(row=1, column=1, sticky="ns")

        self._table_3.bind("<Double-1>", self._on_remove_order_position)

    def set_ticket(self, ticket):
        #check vip
        isVip = self._database.check_vip(ticket)

        ticketTxt = "Ticket: " + ticket
        if isVip:
            ticketTxt = ticketTxt + " ☆"
            self._priority_switch.config(state="active") 
        else:
            self._priority_switch.config(state="disabled") 
        self._ticket_label.config(text=ticketTxt) 
        credit_txt = "Guthaben: " + str(self._database.get_credit_for_ticket(ticket)) + "€"
        self._credit_label.config(text=credit_txt) 
        self._ticket = ticket

    def _on_search_stand(self, event=None):
        stand_str = self._stand_val.get()

        #clear existing rows
        self._table.delete(*self._table.get_children())
        #insert sample data
        data = []
        stands = self._database.search_stand(stand_str)

        for stand in stands:
            data.append( (stand["ID"], stand["name"]) )

        for i, row in enumerate(data):
            self._table.insert("", END, values=row, tags=("row",))

    def _on_select_stand(self, event=None):
        selected = self._table.focus()
        if not selected:
            return
        selected_stand = self._table.item(selected, "values")[0]

        #clear existing rows
        self._table_2.delete(*self._table_2.get_children())
        #insert sample data
        data = []
        ids = []
        products = self._database.get_products_for_stand(selected_stand)

        for product in products:
            data.append( (product["name"], product["time"], product["price"], product["quantity"]) )
            ids.append(product["ID"])

        for i, row in enumerate(data):
            self._table_2.insert("", END, iid=ids[i], values=row, tags=("row",))

        self._selected_stand = selected_stand
        self._clear_warenkorb()

    def _clear_warenkorb(self):
        self._current_time = 0
        self._current_price = Decimal(0.00)

        #clear existing rows
        self._table_3.delete(*self._table_3.get_children())

    def _on_add_order_position(self, event=None):
        selected = self._table_2.focus()
        if not selected:
            return
        selected_product = self._table_2.item(selected, "values")

        #check available quantity
        if selected_product[3] == "0":
            return
        
        #update available cquantity
        updated_row = (selected_product[0], selected_product[1], selected_product[2], int(selected_product[3]) - 1)
        self._table_2.item(selected, values=updated_row)

        #update warenkorb
        found = False
        item_ids = self._table_3.get_children()
        for id in item_ids:
            if id == selected:
                found = True
                item = self._table_3.item(id, "values")
                current_quantity = int(item[3])
                #update time
                current_time = int(item[1])
                new_time = current_time + ( current_time // current_quantity) 
                #update price
                current_price = Decimal(item[2])
                new_price = current_price + ( current_price // current_quantity)
                #update quantity
                new_quantity = current_quantity + 1

                #update table
                new_item = (item[0], new_time, new_price, new_quantity)
                self._table_3.item(selected, values=new_item)

                #update time/price
                self._current_time += current_time // current_quantity
                self._current_price += current_price // current_quantity

        
        if not found:
            products = self._database.get_products_for_stand(self._selected_stand)
            for product in products:
                if int(selected) == product["ID"]:
                    newRow = (product["name"], product["time"], product["price"], 1)
                    self._table_3.insert("", END, iid=selected, values=newRow, tags=("row",))

                    #update time/price
                    self._current_time += product["time"]
                    self._current_price += product["price"]

        self._update_time_price_labels()

    def _update_time_price_labels(self):
        time_txt = "Wartezeit: " + str(self._current_time)
        self._time_label.config(text=time_txt)
        price_txt = "Gesamtpreis: " + str(self._current_price) + "€"
        self._price_label.config(text=price_txt) 

    def _on_remove_order_position(self, event=None):
        selected = self._table_3.focus()
        if not selected:
            return
        selected_product = self._table_3.item(selected, "values")

        #update warenkorb
        if selected_product[3] == "1":
            self._table_3.delete(selected)

            #update time/price
            current_quantity = int(selected_product[3])
            current_time = int(selected_product[1])
            current_price = Decimal(selected_product[2])
            
            self._current_time -= current_time // current_quantity
            self._current_price -= current_price // current_quantity
        else:
            current_quantity = int(selected_product[3])
            #update time
            current_time = int(selected_product[1])
            new_time = current_time - ( current_time // current_quantity) 
            #update price
            current_price = Decimal(selected_product[2])
            new_price = current_price - ( current_price // current_quantity)
            #update quantity
            new_quantity = current_quantity - 1

            #update table
            new_item = (selected_product[0], new_time, new_price, new_quantity)
            self._table_3.item(selected, values=new_item)

            #update time/price
            self._current_time -= current_time // current_quantity
            self._current_price -= current_price // current_quantity

        #update available quantity
        bestellkarte_item = self._table_2.item(selected, "values")
        updated_row = (bestellkarte_item[0], bestellkarte_item[1], bestellkarte_item[2], int(bestellkarte_item[3]) + 1)
        self._table_2.item(selected, values=updated_row)

        self._update_time_price_labels()

    def _on_cancel(self):
        self._clear_warenkorb()

        #clear tables
        self._table.delete(*self._table.get_children())
        self._table_2.delete(*self._table_2.get_children())
        self._table_3.delete(*self._table_3.get_children())

        #clear input fields
        self._stand_val.set("")
        self._special_requests_val.set("")

        #reset time/price
        self._current_time = 0
        self._current_price = Decimal(0.00)
        self._priority = False

        self._visitor_page_management.fill_order_table_rows(self._ticket)
        self._visitor_page_management.get_page().tkraise()

    def _on_order(self):
        #not enough credit
        if self._current_price > self._database.get_credit_for_ticket(self._ticket):
            messagebox.showerror("Fehler", "Zu wenig Guthaben!") 
            return

        order_positions = []
        warenkorb_items = self._table_3.get_children()

        #special requests
        special_requests = ""
        if self._special_requests_val.get() != "Sonderwünsche":
            special_requests = self._special_requests_val.get()

        if warenkorb_items:
            for item_id in warenkorb_items:
                item = self._table_3.item(item_id, "values")
                order_positions.append({"productID": int(item_id), "quantity": int(item[3])})

            if self._database.place_order(self._selected_stand, self._ticket, order_positions, self._current_price, special_requests, self._priority):
                #if successfull
                self._database.create_message_for_ticket(self._ticket, f"Bestellung an Stand {self._selected_stand} erfolgreich aufgegeben.")
                self._on_cancel()
        else:
            messagebox.showerror("Fehler", "Leerer Warenkorb!") 

    def set_visitor_pageManagement(self, visitor_page_management):
        self._visitor_page_management = visitor_page_management

    def _add_credit(self):
        self._database.add_credit_for_ticket(self._ticket, 10)

        credit_txt = "Guthaben: " + str(self._database.get_credit_for_ticket(self._ticket)) + "€"
        self._credit_label.config(text=credit_txt) 

