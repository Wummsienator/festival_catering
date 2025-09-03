from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

root = Tk()

#styles
style1 = font.Font(size=20)

#logo
logo_pil = Image.open("logo.png")
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

#frames
form_frame = Frame(root)
form_frame.grid(row=1, column=2, pady=20)

#logo
img_l = Label(form_frame, image=logo_img).grid(row=0, column=0)

#labels
l1 = Label(form_frame, text="Ticket:", font=style1).grid(row=1, column=0)
l2 = Label(form_frame, text="Password:", font=style1).grid(row=2, column=0)

#input fields
ip1 = Entry(form_frame, font=style1, bg="#D4F1F4").grid(row=1, column=1)
ip2 = Entry(form_frame, font=style1, bg="#D4F1F4").grid(row=2, column=1)


#settings
root.geometry("1450x650")
root.title("Festival Catering")
root.resizable(False, False)
root.mainloop()