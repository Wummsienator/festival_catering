from tkinter import *
from tkinter import ttk

class OrderDetailsDialog(Toplevel):
    def __init__(self, parent, style, style_1, scaling, database, order):
        super().__init__(parent)

        self._style = style
        self._style_1 = style_1
        self._scaling = scaling
        self._database = database

        self.title("Bestellung: " + str(order))
        self.geometry(f"{int(420 * self._scaling)}x{int(320 * self._scaling)}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = Label(
            self,
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

        tv_style = "self.Treeview"
        head_style = "self.Treeview.Heading"
        base = max(9, int(11 * self._scaling))
        self._style.configure(tv_style, font=("Arial", base), rowheight=max(18, int(28 * self._scaling)))
        self._style.configure(head_style, font=("Arial", base, "bold"), padding=(0, int(5 * self._scaling)), background="#05445E", foreground="white")

        table_area = Frame(self)
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
        order_id = order
        positions = self._database.get_positions_for_order(order_id)
        special_requests = self._database.get_special_requests_for_order(order_id)

        for position in positions:
            table.insert("", END, values=(position["name"], position["quantity"]), tags=("row",))

        Label(self, text="Sonderwünsche:", font=self._style_1).grid(row=2, column=0, sticky="w", padx=int(10 * self._scaling))
        Label(self, text=special_requests, font=self._style_1, wraplength=int(380 * self._scaling))\
            .grid(row=3, column=0, sticky="w", padx=int(10 * self._scaling), pady=(0, int(10 * self._scaling)))