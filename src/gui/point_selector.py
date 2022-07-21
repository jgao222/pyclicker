import tkinter as tk
from tkinter import ttk
import re
from ast import literal_eval

import consts


class PointSelector(ttk.LabelFrame):
    """
    Selector for specific point to click at
    @callback
    - calls its callback with selected point tuple (x, y), or (None, None)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._callback = None

        self._mode = tk.StringVar()
        self._mode.set("CURSOR")
        # radio between clicking at cursor and at set point
        cursor_option = ttk.Radiobutton(self, text="At cursor",
                                        variable=self._mode, value="CURSOR")
        point_option = ttk.Radiobutton(self, text="At point",
                                       variable=self._mode, value="POINT")
        cursor_option.grid(row=0, column=0, sticky="w",
                           padx="40 0", pady="5 0")
        point_option.grid(row=1, column=0, sticky="w", padx="40 0")

        self._mode.trace_add("write", self.handle_mode_change)

        # an entry? label? displaying coordinates
        (self._x, self._y) = (0, 0)
        self._COORD_TEXT = tk.StringVar()
        self._COORD_TEXT.set(f"({self._x}, {self._y})")
        self._COORD_TEXT.trace_add("write", self.handle_text_update)

        check_valid_wrapper = (self.register(self.check_valid_coords), "%P")
        self._COORD_ENTRY = ttk.Entry(self, textvariable=self._COORD_TEXT,
                                      validate="all",
                                      validatecommand=check_valid_wrapper,
                                      state="disabled")
        self._COORD_ENTRY.grid(row=2, column=0, pady="0 10", padx="50 5")

    def handle_mode_change(self, *args):
        # surely this is only called after the value is updated right?
        consts.dprint("called handle_mode_change", 2)
        match self._mode.get():
            case "CURSOR":  # should grey out the point selection stuff
                self._COORD_ENTRY.configure(state="disabled")
                self._callback((None, None))
            case "POINT":
                self._COORD_ENTRY.configure(state="normal")
                self._callback((self._x, self._y))

    def handle_text_update(self, *args):
        new_text = self._COORD_TEXT.get()
        if re.match('^\\([0-9]+,\\s?[0-9]+\\)$', new_text) is not None:
            (self._x, self._y) = literal_eval(new_text)
            self._callback((self._x, self._y))

    def set_callback(self, callback):
        self._callback = callback

    def check_valid_coords(self, newval):
        consts.dprint(f"called check_valid_coords: {newval}")
        valid = re.match('^\\([0-9]*,\\s?[0-9]*\\)$', newval) is not None
        return valid
