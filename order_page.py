from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from elements import PlaceholderEntry
from decimal import Decimal
import math


class OrderPage:
    def __init__(self, root, database, style_1, scaling):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._scaling = scaling

        self._order_page = None
        self._ticket = None
        self._selected_stand = None

        self._current_time = 0
        self._current_price = Decimal("0.00")
        self._priority = False

        # widgets
        self._ticket_label = None
        self._credit_label = None
        self._time_label = None
        self._price_label = None

        self._stand_val = StringVar()
        self._special_requests_val = StringVar()

        self._stand_ipt = None
        self._special_requests_ipt = None

        self._priority_switch = None

        # tables
        self._table = None      # stands
        self._table_2 = None    # bestellkarte
        self._table_3 = None    # warenkorb

        # styles
        self._style = ttk.Style(self._root)
        self._style.theme_use("default")

        # images
        self._logo_img = None
        self._on_img = None
        self._off_img = None

        self._visitor_page_management = None

    # ---------------- public ----------------

    def get_page(self):
        if self._order_page:
            return self._order_page

        pad = int(18 * self._scaling)
        gap = int(10 * self._scaling)

        page = Frame(self._root)
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)

        content = Frame(page)
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        # rows: top bar, tables stack, bottom
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=1)
        content.grid_rowconfigure(2, weight=0)

        self._load_images()

        # ---------- TOP BAR ----------
        top = Frame(content)
        top.grid(row=0, column=0, sticky="ew", padx=pad, pady=(pad, gap))
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=0)
        top.grid_columnconfigure(2, weight=0)

        self._ticket_label = Label(top, text="Ticket: -", font=self._style_1)
        self._ticket_label.grid(row=0, column=0, sticky="w")

        right_top = Frame(top)
        right_top.grid(row=0, column=1, sticky="e")
        self._credit_label = Label(right_top, text="Guthaben: -", font=self._style_1)
        self._credit_label.grid(row=0, column=0, sticky="e", padx=(0, gap))

        Button(
            right_top, text="€▷",
            command=self._add_credit,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=1, sticky="e")

        # ---------- TABLES AREA (vertical stack) ----------
        tables = Frame(content)
        tables.grid(row=1, column=0, sticky="nsew", padx=pad)
        tables.grid_columnconfigure(0, weight=1)

        # FIXED-height table blocks: do NOT give them weight=1
        tables.grid_rowconfigure(0, weight=1)  # search input
        tables.grid_rowconfigure(1, weight=1)  # Stand Auswahl
        tables.grid_rowconfigure(2, weight=1)  # Bestellkarte
        tables.grid_rowconfigure(3, weight=1)  # Warenkorb
        tables.grid_rowconfigure(4, weight=1)  # spacer

        # --- Stand search input (ABOVE stand table) ---
        search = Frame(tables)
        search.grid(row=0, column=0, sticky="ew", pady=(0, gap))
        search.grid_columnconfigure(0, weight=1)

        self._stand_val = StringVar()
        self._stand_ipt = PlaceholderEntry(
            search, "Suche Stand", "grey",
            font=self._style_1, bg="#D4F1F4",
            textvariable=self._stand_val
        )
        self._stand_ipt.grid(row=0, column=0, sticky="ew")
        self._stand_ipt.bind("<Return>", self._on_search_stand)

        Label(search, text="⌕", font=self._style_1).grid(row=0, column=1, padx=(gap, 0))

        # --- tables in the required order ---
        self._create_stand_table(tables, gap=gap)            # row=1
        self._create_bestellkarte_table(tables, gap=gap)     # row=2
        self._create_warenkorb_table(tables, gap=0)          # row=3

        # spacer to absorb extra height (so tables remain compact)
        spacer = Frame(tables)
        spacer.grid(row=4, column=0, sticky="nsew")

        # ---------- BOTTOM ----------
        bottom = Frame(content)
        bottom.grid(row=2, column=0, sticky="ew", padx=pad, pady=(gap, pad))
        bottom.grid_columnconfigure(0, weight=1)

        # row 0: Sonderwünsche
        # row 1: Priorisieren
        # row 2: controls (labels left, buttons+logo right)
        bottom.grid_rowconfigure(0, weight=0)
        bottom.grid_rowconfigure(1, weight=0)
        bottom.grid_rowconfigure(2, weight=0)

        self._special_requests_val = StringVar()
        self._special_requests_ipt = PlaceholderEntry(
            bottom, "Sonderwünsche", "grey",
            font=self._style_1, bg="#D4F1F4",
            textvariable=self._special_requests_val
        )
        self._special_requests_ipt.grid(row=0, column=0, sticky="ew", pady=(0, gap))

        # priority row (own row)
        priority_row = Frame(bottom)
        priority_row.grid(row=1, column=0, sticky="ew", pady=(0, gap))
        priority_row.grid_columnconfigure(0, weight=1)
        self._create_priority_switch(priority_row)  # your version that grids inside parent

        # controls row
        controls = Frame(bottom)
        controls.grid(row=2, column=0, sticky="ew")
        controls.grid_columnconfigure(0, weight=1)  # left block
        controls.grid_columnconfigure(1, weight=0)  # right block

        # LEFT: both labels grouped
        left_block = Frame(controls)
        left_block.grid(row=0, column=0, sticky="w")

        self._time_label = Label(left_block, text="Wartezeit: 0", font=self._style_1)
        self._time_label.grid(row=0, column=0, sticky="w", padx=(0, int(18 * self._scaling)))

        self._price_label = Label(left_block, text="Gesamtpreis: 0€", font=self._style_1)
        self._price_label.grid(row=0, column=1, sticky="w")

        # RIGHT: buttons + logo bottom-right
        right_block = Frame(controls)
        right_block.grid(row=0, column=1, sticky="e")

        Button(
            right_block, text="Abbrechen",
            command=self._on_cancel,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=0, sticky="e", padx=(0, gap))

        Button(
            right_block, text="Bestellen",
            command=self._on_order,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=1, sticky="e", padx=(0, gap))

        # logo at bottom-right
        Label(right_block, image=self._logo_img).grid(row=0, column=2, sticky="e")

        self._order_page = page
        return self._order_page

    # ---------------- layout helpers ----------------

    def _load_images(self):
        logo_pil = Image.open("img/logo.png")
        s1 = max(30, round(50 * self._scaling))
        logo_pil = logo_pil.resize((s1, s1), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        on_pil = Image.open("img/on.png")
        off_pil = Image.open("img/off.png")
        s2 = max(15, round(25 * self._scaling))
        on_pil = on_pil.resize((s1, s2), Image.Resampling.LANCZOS)
        off_pil = off_pil.resize((s1, s2), Image.Resampling.LANCZOS)
        self._on_img = ImageTk.PhotoImage(on_pil)
        self._off_img = ImageTk.PhotoImage(off_pil)

    def _create_priority_switch(self, parent):
        wrap = Frame(parent)
        wrap.grid(row=0, column=0, sticky="w")

        Label(wrap, text="Priorisieren:", font=self._style_1).grid(
            row=0, column=0, sticky="w", padx=(0, int(6 * self._scaling))
        )

        self._priority_switch = Button(wrap, image=self._off_img, bd=0, command=self._switch_priority)
        self._priority_switch.grid(row=0, column=1, sticky="w")

    def _table_style(self, prefix: str):
        """Create a consistent unique style name per table."""
        base = max(9, int(11 * self._scaling))
        rowh = max(18, int(28 * self._scaling))
        tv_style = f"{prefix}.Treeview"
        head_style = f"{prefix}.Treeview.Heading"
        self._style.configure(tv_style, font=("Arial", base), rowheight=rowh)
        self._style.configure(head_style, font=("Arial", base, "bold"), padding=(0, int(5 * self._scaling)))
        return tv_style

    def _create_treeview_block(
        self, parent, title_text, columns, prefix, col_width, gap, row,
        height=3, stretch_cols=False
    ):
        wrap = Frame(parent)
        wrap.grid(row=row, column=0, sticky="ew", pady=(0, gap) if gap else 0)
        wrap.grid_columnconfigure(0, weight=1)
        wrap.grid_rowconfigure(1, weight=0)  # fixed height block

        title = Label(
            wrap,
            text=title_text,
            font=("Arial", int(self._scaling * 14), "bold"),
            bg="#05445E",
            fg="white",
            anchor="w",
            padx=int(12 * self._scaling),
            pady=int(6 * self._scaling),
        )
        title.grid(row=0, column=0, sticky="ew")

        area = Frame(wrap)
        area.grid(row=1, column=0, sticky="ew", pady=(gap, 0))

        # ✅ Make the table column expand, scrollbar column stay fixed
        area.grid_columnconfigure(0, weight=1)
        area.grid_columnconfigure(1, weight=0)
        # ✅ Keep fixed height (but allow nsew without vertical growth)
        area.grid_rowconfigure(0, weight=0)

        base = max(9, int(11 * self._scaling))
        rowh = max(18, int(28 * self._scaling))
        tv_style = f"{prefix}.Treeview"
        head_style = f"{prefix}.Treeview.Heading"
        self._style.configure(tv_style, font=("Arial", base), rowheight=rowh)
        self._style.configure(head_style, font=("Arial", base, "bold"), padding=(0, int(5 * self._scaling)))

        tv = ttk.Treeview(
            area,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=height,
            style=tv_style,
        )

        for i, col in enumerate(columns):
            tv.heading(col, text=col, anchor="center")
            is_last = (i == len(columns) - 1)

            tv.column(
                col,
                anchor="center",
                width=col_width,
                stretch=(stretch_cols and is_last)
            )

        tv.tag_configure("row", background="#D4F1F4")

        # ✅ Fill available width AND keep fixed height (row weight is 0)
        tv.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(int(6 * self._scaling), int(6 * self._scaling))
        )

        vsb = ttk.Scrollbar(area, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        hsb = ttk.Scrollbar(area, orient="horizontal", command=tv.xview)
        tv.configure(xscrollcommand=hsb.set)
        hsb.grid(
            row=1, column=0,
            sticky="ew",
            padx=(int(6 * self._scaling), int(6 * self._scaling))
        )

        return tv

    def _create_stand_table(self, parent, gap: int):
        self._table = self._create_treeview_block(
            parent=parent,
            title_text="Stand Auswahl:",
            columns=("Nummer", "Name"),
            prefix="Stand",
            col_width=int(160 * self._scaling),
            gap=gap,
            row=1,
            height=3,
            stretch_cols=True   # Name column fills width
        )
        self._table.bind("<<TreeviewSelect>>", self._on_select_stand)

    def _create_bestellkarte_table(self, parent, gap: int):
        self._table_2 = self._create_treeview_block(
            parent=parent,
            title_text="Bestellkarte:",
            columns=("Name", "Wartezeit", "Preis", "Lagerbestand"),
            prefix="Card",
            col_width=int(170 * self._scaling),
            gap=gap,
            row=2,
            height=3
        )
        self._table_2.bind("<Double-1>", self._on_add_order_position)

    def _create_warenkorb_table(self, parent, gap: int):
        self._table_3 = self._create_treeview_block(
            parent=parent,
            title_text="Warenkorb:",
            columns=("Name", "Wartezeit", "Preis", "Menge"),
            prefix="Cart",
            col_width=int(170 * self._scaling),
            gap=gap,
            row=3,
            height=3
        )
        self._table_3.bind("<Double-1>", self._on_remove_order_position)

    # ---------------- existing logic (mostly unchanged) ----------------

    def _switch_priority(self):
        if self._priority:
            self._priority_switch.config(image=self._off_img)
            self._priority = False
        else:
            self._priority_switch.config(image=self._on_img)
            self._priority = True

    def set_ticket(self, ticket):
        isVip = self._database.check_vip(ticket)

        ticketTxt = "Ticket: " + ticket + (" ☆" if isVip else "")
        self._ticket_label.config(text=ticketTxt)

        if isVip:
            self._priority_switch.config(state="active")
        else:
            self._priority_switch.config(state="disabled")
            self._priority = False
            self._priority_switch.config(image=self._off_img)

        credit_txt = "Guthaben: " + str(self._database.get_credit_for_ticket(ticket)) + "€"
        self._credit_label.config(text=credit_txt)

        self._ticket = ticket

    def _on_search_stand(self, event=None):
        stand_str = self._stand_val.get()

        self._table.delete(*self._table.get_children())
        stands = self._database.search_stand(stand_str)

        for stand in stands:
            self._table.insert("", END, values=(stand["ID"], stand["name"]), tags=("row",))

    def _on_select_stand(self, event=None):
        selected = self._table.focus()
        if not selected:
            return
        selected_stand = self._table.item(selected, "values")[0]

        self._table_2.delete(*self._table_2.get_children())
        data = []
        ids = []
        products = self._database.get_products_for_stand(selected_stand)

        for product in products:
            data.append((product["name"], product["time"], product["price"], product["quantity"]))
            ids.append(product["ID"])

        for i, row in enumerate(data):
            self._table_2.insert("", END, iid=ids[i], values=row, tags=("row",))

        self._selected_stand = selected_stand
        self._clear_warenkorb()

    def _clear_warenkorb(self):
        self._current_time = 0
        self._current_price = Decimal("0.00")
        self._table_3.delete(*self._table_3.get_children())
        self._update_time_price_labels()

    def _on_add_order_position(self, event=None):
        selected = self._table_2.focus()
        if not selected:
            return
        selected_product = self._table_2.item(selected, "values")

        if selected_product[3] == "0":
            return

        updated_row = (selected_product[0], selected_product[1], selected_product[2], int(selected_product[3]) - 1)
        self._table_2.item(selected, values=updated_row)

        found = False
        for iid in self._table_3.get_children():
            if iid == selected:
                found = True
                item = self._table_3.item(iid, "values")
                current_quantity = int(item[3])

                current_time = int(item[1])
                new_time = current_time + (current_time // current_quantity)

                current_price = Decimal(str(item[2]))
                new_price = current_price + (current_price // current_quantity)

                new_quantity = current_quantity + 1

                self._table_3.item(iid, values=(item[0], new_time, new_price, new_quantity))

                self._current_time += current_time // current_quantity
                self._current_price += current_price // current_quantity
                break

        if not found:
            products = self._database.get_products_for_stand(self._selected_stand)
            for product in products:
                if int(selected) == product["ID"]:
                    self._table_3.insert("", END, iid=selected,
                                         values=(product["name"], product["time"], product["price"], 1),
                                         tags=("row",))
                    self._current_time += product["time"]
                    self._current_price += product["price"]
                    break

        self._update_time_price_labels()

    def _on_remove_order_position(self, event=None):
        selected = self._table_3.focus()
        if not selected:
            return
        selected_product = self._table_3.item(selected, "values")

        if selected_product[3] == "1":
            self._table_3.delete(selected)

            current_quantity = int(selected_product[3])
            current_time = int(selected_product[1])
            current_price = Decimal(str(selected_product[2]))

            self._current_time -= current_time // current_quantity
            self._current_price -= current_price // current_quantity
        else:
            current_quantity = int(selected_product[3])

            current_time = int(selected_product[1])
            new_time = current_time - (current_time // current_quantity)

            current_price = Decimal(str(selected_product[2]))
            new_price = current_price - (current_price // current_quantity)

            new_quantity = current_quantity - 1

            self._table_3.item(selected, values=(selected_product[0], new_time, new_price, new_quantity))

            self._current_time -= current_time // current_quantity
            self._current_price -= current_price // current_quantity

        bestellkarte_item = self._table_2.item(selected, "values")
        updated_row = (bestellkarte_item[0], bestellkarte_item[1], bestellkarte_item[2], int(bestellkarte_item[3]) + 1)
        self._table_2.item(selected, values=updated_row)

        self._update_time_price_labels()

    def _update_time_price_labels(self):
        self._time_label.config(text="Wartezeit: " + str(self._current_time))
        self._price_label.config(text="Gesamtpreis: " + str(self._current_price) + "€")

    def _on_cancel(self):
        self._clear_warenkorb()

        self._table.delete(*self._table.get_children())
        self._table_2.delete(*self._table_2.get_children())
        self._table_3.delete(*self._table_3.get_children())

        self._stand_val.set("")
        self._special_requests_val.set("")

        self._current_time = 0
        self._current_price = Decimal("0.00")
        self._priority = False
        if self._priority_switch:
            self._priority_switch.config(image=self._off_img)

        self._visitor_page_management.fill_order_table_rows(self._ticket)
        self._visitor_page_management.get_page().tkraise()

    def _on_order(self):
        if self._current_price > self._database.get_credit_for_ticket(self._ticket):
            messagebox.showerror("Fehler", "Zu wenig Guthaben!")
            return

        order_positions = []
        warenkorb_items = self._table_3.get_children()

        special_requests = ""
        if self._special_requests_val.get() != "Sonderwünsche":
            special_requests = self._special_requests_val.get()

        if warenkorb_items:
            for item_id in warenkorb_items:
                item = self._table_3.item(item_id, "values")
                order_positions.append({"productID": int(item_id), "quantity": int(item[3])})

            if self._database.place_order(self._selected_stand, self._ticket, order_positions,
                                         self._current_price, special_requests, self._priority):
                self._database.create_message_for_ticket(
                    self._ticket,
                    f"Bestellung an Stand {self._selected_stand} erfolgreich aufgegeben."
                )
                self._on_cancel()
        else:
            messagebox.showerror("Fehler", "Leerer Warenkorb!")

    def set_visitor_pageManagement(self, visitor_page_management):
        self._visitor_page_management = visitor_page_management

    def _add_credit(self):
        self._database.add_credit_for_ticket(self._ticket, 10)
        credit_txt = "Guthaben: " + str(self._database.get_credit_for_ticket(self._ticket)) + "€"
        self._credit_label.config(text=credit_txt)
