from tkinter import *
from PIL import Image, ImageTk

class LoginPage():
    def __init__(self, root, database, style1):
        self._root = root
        self._database = database
        self._style1 = style1
        self._loginPage = ""

        #logo
        logo_pil = Image.open("img/logo.png")
        logo_pil = logo_pil.resize((300, 300), Image.Resampling.LANCZOS)

        self._logo_img = ImageTk.PhotoImage(logo_pil)

    def getPage(self):
        if not self._loginPage:
            #page
            loginPage = Frame(self._root)

            #define columns
            loginPage.grid_columnconfigure(0, weight=1)
            loginPage.grid_columnconfigure(1, weight=1)
            loginPage.grid_columnconfigure(2, weight=1)
            loginPage.grid_columnconfigure(3, weight=1)
            loginPage.grid_columnconfigure(4, weight=1)

            #define rows
            loginPage.grid_rowconfigure(0, weight=1)
            loginPage.grid_rowconfigure(1, weight=1)
            loginPage.grid_rowconfigure(2, weight=1)
            loginPage.grid_rowconfigure(3, weight=1)
            loginPage.grid_rowconfigure(4, weight=1)

            #frames
            form_frame = Frame(loginPage)
            form_frame.grid(row=2, column=2, pady=20)

            #logo
            Label(loginPage, image=self._logo_img, font=self._style1).grid(row=1, column=2)

            #labels
            Label(form_frame, text="Ticket:", font=self._style1).grid(row=0, column=0)
            Label(form_frame, text="Password:", font=self._style1).grid(row=1, column=0)

            #input fields
            self.ticket_val= StringVar()
            self.password_val= StringVar()
            Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=self.ticket_val).grid(row=0, column=1)
            Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=self.password_val, show="*").grid(row=1, column=1)

            #button
            Button(form_frame, text="Login", command=lambda: self.onLogin(), font=self._style1, background="#75E6DA").grid(row=2, column=0, columnspan=2)

            self._loginPage = loginPage
        return self._loginPage

    def onLogin(self):
        ticket = self.ticket_val.get()
        password = self.password_val.get()

        if self._database.checkLogin(ticket, password):
            self.ticket_val.set("")
            self.password_val.set("")
            self._besucherPageManagement.fillOrderTableRows(ticket)
            self._besucherPageManagement.getPage().tkraise()

    def setBesucherPageManagement(self, besucherPageManagement):
        self._besucherPageManagement = besucherPageManagement