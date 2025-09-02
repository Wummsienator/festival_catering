from tkinter import *

root = Tk()
root.title("")

#Label Widgets
myLabel1 = Label(root, text="Test!")
myLabel2 = Label(root, text="Hello!")


myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=5)

root.mainloop()