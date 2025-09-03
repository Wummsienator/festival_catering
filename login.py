from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from database import Database

root = Tk()

#styles
style1 = font.Font(size=20)

#variables
database = Database()

#logo
logo_pil = Image.open("logo.png")
logo_pil = logo_pil.resize((300, 300), Image.Resampling.LANCZOS)

logo_img = ImageTk.PhotoImage(logo_pil)

#define columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

#define rows
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

#frames
form_frame = Frame(root)
form_frame.grid(row=2, column=2, pady=20)

#logo
img_l = Label(root, image=logo_img, font=style1).grid(row=1, column=2)

#labels
l1 = Label(form_frame, text="Ticket:", font=style1).grid(row=0, column=0)
l2 = Label(form_frame, text="Password:", font=style1).grid(row=1, column=0)

#input fields
ticket_val= StringVar()
password_val= StringVar()
ip1 = Entry(form_frame, font=style1, bg="#D4F1F4", textvariable=ticket_val).grid(row=0, column=1)
ip2 = Entry(form_frame, font=style1, bg="#D4F1F4", textvariable=password_val, show="*").grid(row=1, column=1)

#button
logBtn = Button(form_frame, text="Login", command=lambda: onLogin(), font=style1, background="#75E6DA").grid(row=2, column=0, columnspan=2)

#functions
def onLogin():
    ticket = ticket_val.get()
    password = password_val.get()

    data = database.readData()
    found = False

    for t in data["Tickets"]:
        if t == ticket:
            found = True
            if data["Tickets"][t]["password"] == password:
                print("Correct Password!")
                ticket_val.set("")
                password_val.set("")
            else:
                print("Wrong Password!")

    if not found:
        print("Invalid Ticket!")

#settings
root.geometry("950x950")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()