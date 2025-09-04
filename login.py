from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from database import Database

class LoginPage():
    def __init__(self, root, database, style1):
        self._root = root
        self._database = database
        self._style1 = style1
        self._loginPage = ""

        self._besucherPage = Frame(root)

    def getPage(self):
        if not self._loginPage:
            #page
            loginPage = Frame(self._root)

            #logo
            logo_pil = Image.open("logo.png")
            logo_pil = logo_pil.resize((300, 300), Image.Resampling.LANCZOS)

            logo_img = ImageTk.PhotoImage(logo_pil)

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
            img_l = Label(loginPage, image=logo_img, font=self._style1).grid(row=1, column=2)

            #labels
            l1 = Label(form_frame, text="Ticket:", font=self._style1).grid(row=0, column=0)
            l2 = Label(form_frame, text="Password:", font=self._style1).grid(row=1, column=0)

            #input fields
            self.ticket_val= StringVar()
            self.password_val= StringVar()
            ip1 = Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=self.ticket_val).grid(row=0, column=1)
            ip2 = Entry(form_frame, font=self._style1, bg="#D4F1F4", textvariable=self.password_val, show="*").grid(row=1, column=1)

            #button
            logBtn = Button(form_frame, text="Login", command=lambda: self.onLogin(), font=self._style1, background="#75E6DA").grid(row=2, column=0, columnspan=2)

            self._loginPage = loginPage
        return self._loginPage

    def onLogin(self):
        ticket = self.ticket_val.get()
        password = self.password_val.get()

        data = self._database.readData()
        found = False

        for t in data["Tickets"]:
            if t == ticket:
                found = True
                if data["Tickets"][t]["password"] == password:
                    print("Correct Password!")
                    self.ticket_val.set("")
                    self.password_val.set("")
                    self._besucherPage.tkraise()
                else:
                    print("Wrong Password!")

        if not found:
            print("Invalid Ticket!")

    def setBesucherPage(self, besucherPage):
        self._besucherPage = besucherPage