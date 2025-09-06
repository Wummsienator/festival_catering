from tkinter import *
from PIL import Image, ImageTk

class LoginPage():
    def __init__(self, root, database, style_1):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._login_page = None

        #logo
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((300, 300), Image.Resampling.LANCZOS)

        self._logo_img = ImageTk.PhotoImage(logo_pil)

    def getPage(self):
        if not self._login_page:
            #page
            login_page = Frame(self._root)

            #define columns
            login_page.grid_columnconfigure(0, weight=1)
            login_page.grid_columnconfigure(1, weight=1)
            login_page.grid_columnconfigure(2, weight=1)
            login_page.grid_columnconfigure(3, weight=1)
            login_page.grid_columnconfigure(4, weight=1)

            #define rows
            login_page.grid_rowconfigure(0, weight=1)
            login_page.grid_rowconfigure(1, weight=1)
            login_page.grid_rowconfigure(2, weight=1)
            login_page.grid_rowconfigure(3, weight=1)
            login_page.grid_rowconfigure(4, weight=1)

            #frames
            form_frame = Frame(login_page)
            form_frame.grid(row=2, column=2, pady=20)

            #logo
            Label(login_page, image=self._logo_img, font=self._style_1).grid(row=1, column=2)

            #labels
            Label(form_frame, text="Ticket:", font=self._style_1).grid(row=0, column=0)
            Label(form_frame, text="Password:", font=self._style_1).grid(row=1, column=0)

            #input fields
            self.ticket_val= StringVar()
            self.password_val= StringVar()
            Entry(form_frame, font=self._style_1, bg="#D4F1F4", textvariable=self.ticket_val).grid(row=0, column=1)
            Entry(form_frame, font=self._style_1, bg="#D4F1F4", textvariable=self.password_val, show="*").grid(row=1, column=1)

            #button
            Button(form_frame, text="Login", command=lambda: self.onLogin(), font=self._style_1, background="#75E6DA").grid(row=2, column=0, columnspan=2)

            self._login_page = login_page
        return self._login_page

    def onLogin(self):
        ticket = self.ticket_val.get()
        password = self.password_val.get()

        #check login validity and dependently get corresponding stand
        check_login, stand = self._database.checkLogin(ticket, password)

        if check_login == "Visitor":
            self.ticket_val.set("")
            self.password_val.set("")
            self._visitor_page_management.fillOrderTableRows(ticket)
            self._visitor_page_management.getPage().tkraise()
        elif check_login == "Seller":
            self.ticket_val.set("")
            self.password_val.set("")
            self._seller_page_management.fillOrderTableRows(stand)
            self._seller_page_management.fillProductTableRows(stand)
            self._seller_page_management.getPage().tkraise()


    def setVisitorPageManagement(self, visitor_page_management):
        self._visitor_page_management = visitor_page_management

    def setSellerPageManagement(self, seller_page_management):
        self._seller_page_management = seller_page_management