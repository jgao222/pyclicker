import tkinter as tk
from tkinter import ttk
import re
from ast import literal_eval

import consts


class PointSelector(ttk.Frame):
    """
    Selector for specific point to click at
    @callback
    - calls its callback with selected point tuple (x, y), or (None, None)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._callback = None

        # a label to indicate the option
        click_label = ttk.Label(self, text="Click at: ")
        click_label.grid(row=0, column=0, sticky="w", padx="0 0")

        self._mode = tk.StringVar()
        self._mode.set("CURSOR")
        # radio between clicking at cursor and at set point
        cursor_option = ttk.Radiobutton(self, text="Cursor",
                                        variable=self._mode, value="CURSOR")
        point_option = ttk.Radiobutton(self, text="Position",
                                       variable=self._mode, value="POINT")
        cursor_option.grid(row=1, column=0, sticky="w",
                           padx="40 0", pady="5 0")
        point_option.grid(row=2, column=0, sticky="w", padx="40 0")

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
                                      state="disabled",
                                      width=12)
        self._COORD_ENTRY.grid(row=3, column=0, pady="0 10", padx="50 5")

        self._point_set_btn = ttk.Button(self, text="Set Point",
                                         command=self.handle_set_btn_pressed,
                                         state="disabled")
        self._point_set_btn.grid(row=3, column=1, padx="10 0",
                                 pady="0 10", sticky="sw")

        self._set_pt_info_label = ttk.Label(
            self, text="Click again to set click position",
            foreground="grey60")
        self._set_pt_info_label.grid(row=2, column=1, sticky="sw", pady="0 5")
        self._set_pt_info_label.grid_remove()

    def handle_mode_change(self, *args):
        # surely this is only called after the value is updated right?
        consts.dprint("called handle_mode_change", 2)
        match self._mode.get():
            case "CURSOR":  # should grey out the point selection stuff
                self._COORD_ENTRY.configure(state="disabled")
                self._point_set_btn.configure(state="disabled")
                self._callback((None, None))
            case "POINT":
                self._COORD_ENTRY.configure(state="normal")
                self._point_set_btn.configure(state="normal")
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

    def set_btn_callback(self, btn_callback):
        self._point_set_btn_callback = btn_callback

    def handle_set_btn_pressed(self):
        self._set_pt_info_label.grid()
        if self._point_set_btn_callback:
            self._point_set_btn_callback()

    def handle_external_set_coords(self, point):
        # hopefully this calls the callbacks that normally setting it would
        self._COORD_TEXT.set(f"({point[0]}, {point[1]})")
        self._set_pt_info_label.grid_remove()
