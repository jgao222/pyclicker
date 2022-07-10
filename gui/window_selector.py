import tkinter as tk
from tkinter import ttk


class WindowSelector(tk.Frame):
    """
    A combobox (list) of open windows for the user to select
    """
    def __init__(self, parent):
        super().__init__(parent)

        self._title = ttk.Label(self, text="Click in:")
        self._title.grid(row=0, column=0, padx="20 10")

        self._selected_text = tk.StringVar()
        self._selected_text.set("Anywhere")
        self._selection_box = ttk.Combobox(
            self,
            textvariable=self._selected_text,
            values=("Anywhere", "PLACEHOLDER1", "PLACEHOLDER2"),
            state="readonly"
            )
        self._selection_box.grid(row=0, column=1)
        self._selection_box.bind("<<ComboboxSelected>>", lambda _: self._update())


    def _update(self):
        print("selector updated")
        self._selection_box.selection_clear()
        self.master.focus()
        if self._callback:
            self._callback(self._selected_text.get())


    def set_callback(self, callback):
        self._callback = callback
