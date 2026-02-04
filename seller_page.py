from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from elements import PlaceholderEntry
import datetime
import math


class SellerPage:
    def __init__(self, root, database, style_1, scaling):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._scaling = scaling

        self._seller_page = None
        self._stand = None

        self._stand_label = None
        self._logo_img = None

        self._table = None    # orders
        self._table_2 = None  # inventory

        self._product_combo = None
        self._quantity_val = StringVar()

        # style
        self._style = ttk.Style(self._root)
        self._style.theme_use("default")

    def get_page(self):
        if self._seller_page:
            return self._seller_page

        pad = int(18 * self._scaling)
        gap = int(10 * self._scaling)

        page = Frame(self._root)
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)

        content = Frame(page)
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        # Layout rows:
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=0)
        content.grid_rowconfigure(2, weight=0)
        content.grid_rowconfigure(3, weight=0)
        content.grid_rowconfigure(4, weight=0)
        content.grid_rowconfigure(5, weight=1)  # spacer/footer

        self._load_images()

        # top
        top = Frame(content)
        top.grid(row=0, column=0, sticky="ew", padx=pad, pady=(pad, gap))
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=0)

        self._stand_label = Label(top, text="Stand Nr.: -", font=self._style_1)
        self._stand_label.grid(row=0, column=0, sticky="w")

        # order table
        self._create_order_table(content, row=1, padx=pad, pady=(0, gap))

        # status button
        btn_row = Frame(content)
        btn_row.grid(row=2, column=0, sticky="ew", padx=pad, pady=(0, gap))
        btn_row.grid_columnconfigure(0, weight=1)

        Button(
            btn_row,
            text="Status weiterschalten",
            command=self._on_change_status,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=0, sticky="w")

        # inventory table
        self._create_product_table(content, row=3, padx=pad, pady=(0, gap))

        # add product row
        self._create_product_combo_box(content, row=4, padx=pad, pady=(0, gap))

        # logo
        footer = Frame(content)
        footer.grid(row=5, column=0, sticky="nsew", padx=pad, pady=(0, pad))
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_rowconfigure(0, weight=1)

        Label(footer, image=self._logo_img).grid(row=0, column=0, sticky="se")

        self._seller_page = page
        return self._seller_page

    def _load_images(self):
        logo_pil = Image.open("img/logo.png")
        s_size = max(30, round(50 * self._scaling))
        logo_pil = logo_pil.resize((s_size, s_size), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

    def _apply_treeview_style(self, prefix: str):
        """Unique style per table so they don't overwrite each other."""
        base = max(9, int(11 * self._scaling))
        rowh = max(18, int(28 * self._scaling))
        tv_style = f"{prefix}.Treeview"
        head_style = f"{prefix}.Treeview.Heading"

        self._style.configure(tv_style, font=("Arial", base), rowheight=rowh)
        self._style.configure(head_style, font=("Arial", base, "bold"), padding=(0, int(5 * self._scaling)), background="#05445E", foreground="white")
        return tv_style

    def _create_table_block(self, parent, title_text, columns, prefix, row, padx, pady, height=4, col_width=180):
        wrap = Frame(parent)
        wrap.grid(row=row, column=0, sticky="ew", padx=padx, pady=pady)
        wrap.grid_columnconfigure(0, weight=1)

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
        area.grid(row=1, column=0, sticky="ew", pady=(int(8 * self._scaling), 0))
        area.grid_columnconfigure(0, weight=1)
        area.grid_columnconfigure(1, weight=0)
        area.grid_rowconfigure(0, weight=0)

        tv_style = self._apply_treeview_style(prefix)

        tv = ttk.Treeview(
            area,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=height,
            style=tv_style
        )

        for c in columns:
            tv.heading(c, text=c, anchor="center")
            tv.column(
                c,
                anchor="center",
                width=int(col_width * self._scaling),
                stretch=True
            )

        tv.tag_configure("row", background="#D4F1F4")

        tv.grid(row=0, column=0, sticky="nsew",
                padx=(int(6 * self._scaling), int(6 * self._scaling)))

        vsb = ttk.Scrollbar(area, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        # horizontal scrollbar
        hsb = ttk.Scrollbar(area, orient="horizontal", command=tv.xview)
        tv.configure(xscrollcommand=hsb.set)
        hsb.grid(row=1, column=0, sticky="ew",
                 padx=(int(6 * self._scaling), int(6 * self._scaling)))

        return tv

    def _create_order_table(self, seller_page, row, padx, pady):
        columns = ("Bestellung Nr.", "Zeitstempel", "Zeit", "Status", "Priorisiert")
        self._table = self._create_table_block(
            parent=seller_page,
            title_text="Offene Bestellungen:",
            columns=columns,
            prefix="Orders",
            row=row,
            padx=padx,
            pady=pady,
            height=4,  
            col_width=170
        )
        self._table.bind("<Double-1>", self._open_popup)

    def _create_product_table(self, seller_page, row, padx, pady):
        columns = ("Name", "Menge", "Warnung")
        self._table_2 = self._create_table_block(
            parent=seller_page,
            title_text="Bestandsanzeige:",
            columns=columns,
            prefix="Stock",
            row=row,
            padx=padx,
            pady=pady,
            height=4, 
            col_width=170
        )
        self._table_2.bind("<<TreeviewSelect>>", self._disable_selection)

    def _create_product_combo_box(self, seller_page, row, padx, pady):
        wrap = Frame(seller_page)
        wrap.grid(row=row, column=0, sticky="ew", padx=padx, pady=pady)
        wrap.grid_columnconfigure(0, weight=1)
        wrap.grid_columnconfigure(1, weight=0)
        wrap.grid_columnconfigure(2, weight=0)
        wrap.grid_columnconfigure(3, weight=0)

        # products list
        products = self._database.get_products()
        options = {p["ID"]: p["name"] for p in products}
        display_values = [f"{v} ({k})" for k, v in options.items()]

        # combobox
        self._product_combo = ttk.Combobox(wrap, values=display_values, state="readonly", font=self._style_1)
        self._product_combo.grid(row=0, column=0, sticky="w")
        self._product_combo.set("Produkt wählen")

        # quantity input
        _validate_int = (seller_page.register(self._validate_int), "%P")
        self._quantity_val = StringVar()
        quantity_ipt = PlaceholderEntry(
            wrap, "Menge", "grey",
            font=self._style_1, bg="#D4F1F4",
            textvariable=self._quantity_val,
            validate="key", validatecommand=_validate_int
        )
        quantity_ipt.grid(row=0, column=1, sticky="w", padx=(int(10 * self._scaling), 0))

        # add button 
        Button(
            wrap, text="Bestand hinzufügen",
            command=self._on_add_product,
            font=self._style_1, background="#75E6DA"
        ).grid(row=0, column=3, sticky="e")

    def _validate_int(self, new_value):
        if new_value == "" or new_value == "Menge":
            return True
        return new_value.isdigit()

    def _disable_selection(self, event=None):
        event.widget.selection_remove(event.widget.selection())

    def fill_order_table_rows(self, stand):
        self._table.delete(*self._table.get_children())

        orders = self._database.get_orders_for_stand(stand)
        for order in orders:
            row = (
                order["ID"],
                order["timestamp"].strftime("%d.%m.%y %X"),
                order["time"],
                order["status_desc"],
                order["prioritized"]
            )
            self._table.insert("", END, values=row, tags=("row",))

        self._stand = stand
        self._stand_label.config(text=f"Stand Nr.: {stand}")

    def fill_product_table_rows(self, stand):
        self._table_2.delete(*self._table_2.get_children())

        products = self._database.get_products_for_stand(stand)
        for product in products:
            warning = "!!!" if int(product["quantity"]) < 10 else ""
            self._table_2.insert("", END, values=(product["name"], product["quantity"], warning), tags=("row",))

    def _on_add_product(self, event=None):
        display = self._product_combo.get()
        quantity = self._quantity_val.get()
        if not display or not quantity or quantity == "Menge":
            return

        key = display.split("(", 1)[1].strip(")")
        self._database.add_product_for_stand(self._stand, key, int(quantity))
        self.fill_product_table_rows(self._stand)

        self._product_combo.set("Produkt wählen")
        self._quantity_val.set("")

    def _open_popup(self, event=None):
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        popup = Toplevel(self._seller_page)
        popup.title("Bestellung: " + str(selected_order[0]))
        popup.geometry(f"{int(420 * self._scaling)}x{int(320 * self._scaling)}")

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(1, weight=1)

        title = Label(
            popup,
            text="Positionen:",
            font=("Arial", int(self._scaling * 14), "bold"),
            bg="#05445E",
            fg="white",
            anchor="w",
            padx=int(12 * self._scaling),
            pady=int(6 * self._scaling),
        )
        title.grid(row=0, column=0, sticky="ew")

        columns = ("Name", "Menge")

        tv_style = "Popup.Treeview"
        head_style = "Popup.Treeview.Heading"
        base = max(9, int(11 * self._scaling))
        self._style.configure(tv_style, font=("Arial", base), rowheight=max(18, int(28 * self._scaling)))
        self._style.configure(head_style, font=("Arial", base, "bold"), padding=(0, int(5 * self._scaling)), background="#05445E", foreground="white")

        table_area = Frame(popup)
        table_area.grid(row=1, column=0, sticky="nsew", padx=int(10 * self._scaling), pady=int(10 * self._scaling))
        table_area.grid_columnconfigure(0, weight=1)
        table_area.grid_rowconfigure(0, weight=1)

        table = ttk.Treeview(table_area, columns=columns, show="headings", height=6, style=tv_style)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=int(self._scaling * 160))

        table.tag_configure("row", background="#D4F1F4")
        table.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(table_area, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        # fill rows
        order_id = selected_order[0]
        positions = self._database.get_positions_for_order(order_id)
        special_requests = self._database.get_special_requests_for_order(order_id)

        for position in positions:
            table.insert("", END, values=(position["name"], position["quantity"]), tags=("row",))

        Label(popup, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0, sticky="w", padx=int(10 * self._scaling))
        Label(popup, text=special_requests, font=self._style_1, wraplength=int(380 * self._scaling))\
            .grid(row=3, column=0, sticky="w", padx=int(10 * self._scaling), pady=(0, int(10 * self._scaling)))

    def _on_change_status(self, event=None):
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")
        self._database.change_status_for_order(selected_order[0])
        self.fill_order_table_rows(self._stand)
