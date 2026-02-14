from tkinter import *
from tkinter import messagebox

class CreditDialog(Toplevel):
    """
    Popup: Kreditkarte + PIN + Betrag -> ruft on_success(amount) bei Erfolg auf
    """

    TEST_CARDS = {
        "4111111111111111": "1234",
        "5555555555554444": "4321",
    }

    def __init__(self, parent, style_font, on_success):
        super().__init__(parent)
        self._style_1 = style_font
        self._on_success = on_success

        self.title("Guthaben aufladen")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._btn_color = "#75E6DA"
        self._input_bg = "#D4F1F4"
        self._header_bg = "#05445E"
        self._header_fg = "white"

        self._card_val = StringVar()
        self._pin_val = StringVar()
        self._amount_val = StringVar()

        container = Frame(self, padx=20, pady=15)
        container.grid(row=0, column=0)

        header = Label(
            container,
            text="Guthaben aufladen",
            font=("Arial", 14, "bold"),
            bg=self._header_bg,
            fg=self._header_fg,
            width=35
        )
        header.grid(row=0, column=0, columnspan=2, pady=(0, 12))

        Label(container, text="Kreditkarte Nr.:", font=self._style_1).grid(row=1, column=0, sticky="w")
        Entry(container, textvariable=self._card_val, font=self._style_1, bg=self._input_bg, width=25)\
            .grid(row=2, column=0, sticky="w", pady=(2, 10))

        Label(container, text="PIN:", font=self._style_1).grid(row=1, column=1, sticky="w", padx=(10, 0))
        Entry(container, textvariable=self._pin_val, font=self._style_1, bg=self._input_bg, width=8, show="*")\
            .grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(2, 10))

        Label(container, text="Betrag (€):", font=self._style_1).grid(row=3, column=0, sticky="w")
        Entry(container, textvariable=self._amount_val, font=self._style_1, bg=self._input_bg, width=15)\
            .grid(row=4, column=0, sticky="w", pady=(2, 12))

        btn_frame = Frame(container)
        btn_frame.grid(row=5, column=0, columnspan=2, sticky="e")

        Button(btn_frame, text="Aufladen", command=self._submit, font=self._style_1, background=self._btn_color)\
            .grid(row=0, column=0)
        Button(btn_frame, text="Schließen", command=self.destroy, font=self._style_1, background=self._btn_color)\
            .grid(row=0, column=1, padx=(8, 0))

        self.bind("<Return>", lambda e: self._submit())

    def _submit(self):
        card = self._card_val.get().strip()
        pin = self._pin_val.get().strip()
        amount_str = self._amount_val.get().strip().replace(",", ".")

        if card not in self.TEST_CARDS:
            messagebox.showerror("Fehler", "Test-Kreditkarte unbekannt.")
            return
        if self.TEST_CARDS[card] != pin:
            messagebox.showerror("Fehler", "PIN ist falsch.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Fehler", "Bitte gültigen Betrag eingeben (z.B. 10 oder 10.50).")
            return
        if amount <= 0:
            messagebox.showerror("Fehler", "Betrag muss größer als 0 sein.")
            return

        try:
            self._on_success(amount)
        except Exception as ex:
            messagebox.showerror("Fehler", f"Aufladen fehlgeschlagen:\n{ex}")
            return

        self.destroy()