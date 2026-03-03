from tkinter import *

class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="Enter text...", color="grey", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]        #foreground clolor

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        if self["fg"] == self.placeholder_color and self.get() == self.placeholder:
            self.delete(0, END)
            self["fg"] = self.default_fg_color

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color

    def restore_placeholder(self):
        text = self.get()
        if text == "" or (self["fg"] == self.placeholder_color and text != self.placeholder):
            self.delete(0, END)
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color
