from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class SellerPage():
    def __init__(self, root, database, style_1):
        self._root = root
        self._database = database
        self._style_1 = style_1
        self._seller_page = None
        self._stand = "1"

    def getPage(self):
        if not self._seller_page:
            seller_page = Frame(self._root)


            self._seller_page = seller_page
        return self._seller_page