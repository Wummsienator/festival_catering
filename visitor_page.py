from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
import qrcode

class VisitorPage:
    def __init__(self, root, database, style_1, scaling):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._scaling = scaling

        self._visitor_page = None
        self._ticket = None

        self._order_page_management = None

        # vars
        self._friend_ticket_val = StringVar()

        # images
        self._logo_img = None
        self._qr_img = None
        self._logo_pil_original = Image.open("img/logo.png")
        self._qr_pil_original = Image.open("img/QR_Code.png")

        # ttk styles
        self._style = ttk.Style(self._root)
        self._style.theme_use("default")

        # tables
        self._table = None
        self._table2 = None

        # labels
        self._ticket_label = None
        self._credit_label = None

        # periodic update
        self._notify_job = None

    def get_page(self):
        if self._visitor_page:
            return self._visitor_page

        page = Frame(self._root)
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)

        pad = int(18 * self._scaling)      # page padding
        gap = int(10 * self._scaling)      # internal gaps

        # main content
        content = Frame(page)
        content.grid(row=0, column=0, sticky="nsew")

        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=0)
        content.grid_rowconfigure(2, weight=0)
        content.grid_rowconfigure(3, weight=0)
        content.grid_rowconfigure(4, weight=1)  # notifications can take leftover space
        content.grid_rowconfigure(5, weight=0)

        # render images once
        self._load_images()

        # Top bar
        top = Frame(content)
        top.grid(row=0, column=0, sticky="ew", padx=pad, pady=(pad, gap))
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=0)
        top.grid_columnconfigure(2, weight=0)

        self._ticket_label = Label(top, text="Ticket: -", font=self._style_1)
        self._ticket_label.grid(row=0, column=0, sticky="w")

        self._credit_label = Label(top, text="Guthaben: -", font=self._style_1)
        self._credit_label.grid(row=0, column=1, sticky="e", padx=(gap, gap))

        Button(
            top,
            text="€▷",
            command=self._add_credit,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=2, sticky="e")

        # Orders
        orders = Frame(content)
        orders.grid(row=1, column=0, sticky="ew", padx=pad)
        orders.grid_columnconfigure(0, weight=1)
        self._create_order_table(orders, scaling=self._scaling, gap=gap, rows_visible=4)

        # Actions
        actions = Frame(content)
        actions.grid(row=2, column=0, sticky="ew", padx=pad, pady=(gap, gap))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=0)

        Button(
            actions,
            text="Bestellung aufnehmen",
            command=self._on_go_to_order_page,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=0, sticky="w")

        unlock = Frame(actions)
        unlock.grid(row=0, column=1, sticky="e")
        unlock.grid_columnconfigure(0, weight=0)
        unlock.grid_columnconfigure(1, weight=1)

        Label(unlock, text="Ticket Freund:", font=self._style_1).grid(row=0, column=0, sticky="e", padx=(0, gap))
        Entry(unlock, font=self._style_1, bg="#D4F1F4", textvariable=self._friend_ticket_val, width=14)\
            .grid(row=0, column=1, sticky="ew", padx=(0, gap))

        Button(
            unlock,
            text="Bestellung freischalten",
            command=self._unlock_ticket_for_friend,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=0, column=2, sticky="e")

        qr_row = Frame(content)
        qr_row.grid(row=3, column=0, sticky="ew", padx=pad, pady=(0, gap))
        qr_row.grid_columnconfigure(0, weight=1)

        self._qr_label = Label(qr_row, image=self._qr_img)
        self._qr_label.grid(row=0, column=0)                    # centered by default

        # Notifications
        notif = Frame(content)
        notif.grid(row=4, column=0, sticky="nsew", padx=pad, pady=(0, gap))
        notif.grid_columnconfigure(0, weight=1)
        notif.grid_rowconfigure(0, weight=1)
        self._create_notification_table(notif, scaling=self._scaling)

        # Logo
        bottom = Frame(content)
        bottom.grid(row=5, column=0, sticky="ew", padx=pad, pady=(0, pad))
        bottom.grid_columnconfigure(0, weight=1)
        Label(bottom, image=self._logo_img).grid(row=0, column=0, sticky="e")

        self._visitor_page = page

        # start periodic update (UI-safe)
        self._schedule_notification_update()

        return self._visitor_page
    
    def init_data_for_ticket(self, ticket):
        self._ticket = ticket

        self._fill_order_table_rows()
        self._load_and_set_qr_code()
        self.update_notification_table()

    def _fill_order_table_rows(self):
        self._table.delete(*self._table.get_children())

        orders = self._database.get_orders_for_ticket(self._ticket)
        for order in orders:
            row = (order["stand"], order["time"], order["status_desc"], order["ID"])
            self._table.insert("", END, values=row, tags=("row",))

        is_vip = self._database.check_vip(self._ticket)
        ticket_txt = f"Ticket: {self._ticket}" + (" ☆" if is_vip else "")
        self._ticket_label.config(text=ticket_txt)

        credit_txt = f"Guthaben: {self._database.get_credit_for_ticket(self._ticket)}€"
        self._credit_label.config(text=credit_txt)

    def _load_and_set_qr_code(self):
        qr_payload = self._database.get_qr_code_payload(self._ticket)
        png_bytes = bytes(self._make_qr_png_bytes(qr_payload))
        img = Image.open(io.BytesIO(png_bytes))
 
        #scaling
        size = max(100, int(160 * self._scaling))
        img = img.resize((size, size), Image.Resampling.LANCZOS)

        self._qr_img = ImageTk.PhotoImage(img)
        self._qr_label.config(image=self._qr_img)
        self._qr_label.image = self._qr_img  

    def _make_qr_png_bytes(self, payload: str, box_size=10, border=2):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border,
        )
        qr.add_data(payload)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    def set_order_page_management(self, order_page_management):
        self._order_page_management = order_page_management

    def _load_images(self):
        #logo
        logo_size = max(40, int(60 * self._scaling))
        logo_pil = self._logo_pil_original.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)

        #demo qr code
        qr_size = max(100, int(160 * self._scaling))
        qr_pil = self._qr_pil_original.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        self._qr_img = ImageTk.PhotoImage(qr_pil)

    def _create_order_table(self, parent, scaling: float, gap: int, rows_visible: int = 4):
        box = Frame(parent)
        box.grid(row=0, column=0, sticky="ew")
        box.grid_columnconfigure(0, weight=1)

        # Title
        title = Label(
            box,
            text="Offene Bestellungen:",
            font=("Arial", int(14 * scaling), "bold"),
            bg="#05445E",
            fg="white",
            anchor="w",
            padx=int(12 * scaling),
            pady=int(6 * scaling),
        )
        title.grid(row=0, column=0, sticky="ew")

        # Table container
        table_area = Frame(box)
        table_area.grid(row=1, column=0, sticky="ew", pady=(gap, 0))
        table_area.grid_columnconfigure(0, weight=1)

        columns = ("Stand", "Wartezeit", "Status", "Bestellungsnummer")

        tv_style = "Orders.Treeview"
        head_style = "Orders.Treeview.Heading"

        base = max(9, int(11 * scaling))
        self._style.configure(tv_style, font=("Arial", base), rowheight=max(18, int(28 * scaling)))
        self._style.configure(head_style, font=("Arial", base, "bold"))
        self._style.configure(head_style, padding=(0, int(5 * scaling)))
        self._style.configure(head_style, background="#05445E", foreground="white")

        # Treeview
        self._table = ttk.Treeview(
            table_area,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=rows_visible,
            style=tv_style,
        )

        col_width = int(180 * scaling)
        for col in columns:
            self._table.heading(col, text=col)
            self._table.column(col, anchor="center", width=col_width, stretch=False)

        self._table.tag_configure("row", background="#D4F1F4")

        table_area.grid_rowconfigure(0, weight=0)
        table_area.grid_columnconfigure(0, weight=1)

        self._table.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(int(6 * scaling), int(6 * scaling))
        )

        # Vertical scrollbar
        vsb = ttk.Scrollbar(table_area, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        # Horizontal scrollbar
        hsb = ttk.Scrollbar(table_area, orient="horizontal", command=self._table.xview)
        self._table.configure(xscrollcommand=hsb.set)
        hsb.grid(row=1, column=0, sticky="ew", padx=(int(6 * scaling), int(6 * scaling)))

        self._table.bind("<Double-1>", self._open_popup)


    def _create_notification_table(self, parent, scaling: float):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        tv_style = "Notifications.Treeview"
        head_style = "Notifications.Treeview.Heading"

        base = max(9, int(11 * scaling))
        self._style.configure(tv_style, font=("Arial", base), rowheight=max(18, int(28 * scaling)))
        self._style.configure(head_style, font=("Arial", base, "bold"))
        self._style.configure(head_style, padding=(0, int(5 * scaling)))
        self._style.configure(head_style, background="#05445E", foreground="white")

        table_area = Frame(parent)
        table_area.grid(row=0, column=0, sticky="nsew")
        table_area.grid_columnconfigure(0, weight=1)
        table_area.grid_rowconfigure(0, weight=1)

        col = "Benachrichtigungen:"

        self._table2 = ttk.Treeview(
            table_area,
            columns=(col,),
            show="headings",
            selectmode="browse",
            height=4,
            style=tv_style,
        )

        self._table2.heading(col, text=col, anchor="center")
        self._table2.column(col, anchor="w", width=1, stretch=True)
        self._table2.tag_configure("row", background="#D4F1F4")
        self._table2.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar
        vsb = ttk.Scrollbar(table_area, orient="vertical", command=self._table2.yview)
        self._table2.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        self._table2.bind("<<TreeviewSelect>>", self._disable_selection)

    def _schedule_notification_update(self):
        if self._notify_job is not None:
            self._root.after_cancel(self._notify_job)
        self._notify_job = self._root.after(2500, self._poll_notifications)

    def _poll_notifications(self):
        self.update_notification_table()
        self._schedule_notification_update()

    def update_notification_table(self):
        if not self._ticket or not self._table2:
            return
        data = self._database.get_messages_for_ticket(self._ticket)
        self._table2.delete(*self._table2.get_children())
        for msg in reversed(data):
            self._table2.insert("", END, values=(msg,), tags=("row",))

    def _on_go_to_order_page(self):
        if not self._order_page_management:
            return
        self._order_page_management.set_ticket(self._ticket)
        self._root.focus_set()
        self._order_page_management.restore_place_holder()               #because somehow placeholders are cleared on opening page for second time
        self._order_page_management.get_page().tkraise()

    def _disable_selection(self, event=None):
        if event is not None:
            event.widget.selection_remove(event.widget.selection())

    def _add_credit(self):
        if not self._ticket:
            return
        self._database.add_credit_for_ticket(self._ticket, 10)
        credit_txt = f"Guthaben: {self._database.get_credit_for_ticket(self._ticket)}€"
        self._credit_label.config(text=credit_txt)

    def _unlock_ticket_for_friend(self):
        selected = self._table.focus()
        friend_ticket = self._friend_ticket_val.get().strip()

        if not selected or not friend_ticket:
            return

        if not self._database.check_ticket_exists(friend_ticket):
            messagebox.showerror("Fehler", "Ungültige Ticketnummer!")
            return

        values = self._table.item(selected, "values")
        order_id = values[3]

        if self._database.connect_order_to_ticket(order_id, friend_ticket):
            self._database.create_message_for_ticket(
                friend_ticket,
                f"Für sie wurde eine Bestellung an Stand {values[0]} freigeschaltet."
            )
            messagebox.showinfo("Erfolg", "Bestellung erfolgreich freigeschaltet.")
        else:
            messagebox.showinfo("Hinweis", f"Bestellung ist bereits für Ticket {friend_ticket} freigeschaltet.")

    def _open_popup(self, event=None):
        selected = self._table.focus()
        if not selected:
            return
        selected_order = self._table.item(selected, "values")

        popup = Toplevel(self._visitor_page)
        popup.title("Bestellung: " + str(selected_order[3]))
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
        order_id = selected_order[3]
        positions = self._database.get_positions_for_order(order_id)
        special_requests = self._database.get_special_requests_for_order(order_id)

        for position in positions:
            table.insert("", END, values=(position["name"], position["quantity"]), tags=("row",))

        Label(popup, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0, sticky="w", padx=int(10 * self._scaling))
        Label(popup, text=special_requests, font=self._style_1, wraplength=int(380 * self._scaling))\
            .grid(row=3, column=0, sticky="w", padx=int(10 * self._scaling), pady=(0, int(10 * self._scaling)))
