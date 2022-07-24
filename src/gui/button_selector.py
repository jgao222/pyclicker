import tkinter as tk
from tkinter import ttk


class ButtonSelector(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._callback = None

        # a label to indicate the option
        click_label = ttk.Label(self, text="Click Type: ")
        click_label.grid(row=0, column=0, sticky="w", padx="0 0")

        self._mode = tk.StringVar()
        self._mode.set("left")
        # radio between clicking at cursor and at set point
        left = ttk.Radiobutton(self, text="Left Click",
                               variable=self._mode, value="left")
        right = ttk.Radiobutton(self, text="Right Click",
                                variable=self._mode, value="right")
        left.grid(row=0, column=1, padx="10 0", pady="5 0")
        right.grid(row=0, column=2, padx="10 0", pady="5 0")

        self._mode.trace_add("write", self.handle_mode_change)

    def handle_mode_change(self, *args):
        self._callback(self._mode.get())

    def set_callback(self, callback):
        self._callback = callback
