from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginPage:
    def __init__(self, root, database, style_1, scaling):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._scaling = scaling
        self._login_page = None

        self.ticket_val = StringVar()
        self.password_val = StringVar()

        # Load original logo once; render scaled version when building UI
        self._logo_pil_original = Image.open("img/logo.png")
        self._logo_img = None  # PhotoImage created later

    def _render_logo(self, size_px: int):
        logo_pil = self._logo_pil_original.resize((size_px, size_px), Image.Resampling.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(logo_pil)
        return self._logo_img

    def get_page(self):
        if self._login_page:
            return self._login_page

        page = Frame(self._root)
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)

        # A single content frame centered in the page
        content = Frame(page)
        content.grid(row=0, column=0)

        pad = int(16 * self._scaling)
        gap = int(10 * self._scaling)

        # Logo block
        logo_size = max(120, int(260 * self._scaling))
        logo = self._render_logo(logo_size)
        logo_label = Label(content, image=logo)
        logo_label.grid(row=0, column=0, pady=(0, pad))

        # Form block
        form = Frame(content)
        form.grid(row=1, column=0, sticky="ew")

        # Make entry column stretch
        form.grid_columnconfigure(0, weight=0)
        form.grid_columnconfigure(1, weight=1)

        Label(form, text="Ticket:", font=self._style_1).grid(row=0, column=0, sticky="w", padx=(0, gap), pady=(0, gap))
        Label(form, text="Password:", font=self._style_1).grid(row=1, column=0, sticky="w", padx=(0, gap), pady=(0, gap))

        Entry(form, font=self._style_1, bg="#D4F1F4", textvariable=self.ticket_val).grid(row=0, column=1, sticky="ew", pady=(0, gap))
        Entry(form, font=self._style_1, bg="#D4F1F4", textvariable=self.password_val, show="*").grid(row=1, column=1, sticky="ew", pady=(0, gap))

        Button(
            form,
            text="Login",
            command=self._on_login,
            font=self._style_1,
            background="#75E6DA"
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(gap, 0))

        self._login_page = page
        return self._login_page

    def _on_login(self):
        ticket = self.ticket_val.get()
        password = self.password_val.get()

        check_login, stand = self._database.check_login(ticket, password)

        if check_login:
            self.ticket_val.set("")
            self.password_val.set("")
            if not stand:
                self._visitor_page_management.init_data_for_ticket(ticket)
                self._root.focus_set()
                self._visitor_page_management.get_page().tkraise()
            else:
                self._seller_page_management.fill_order_table_rows(stand)
                self._seller_page_management.fill_product_table_rows(stand)
                self._root.focus_set()
                self._seller_page_management.get_page().tkraise()
        else:
            messagebox.showerror("Fehler", "Ungültige Login-Daten!")

    def set_visitor_pageManagement(self, visitor_page_management):
        self._visitor_page_management = visitor_page_management

    def set_seller_page_management(self, seller_page_management):
        self._seller_page_management = seller_page_management
