import tkinter as tk
from tkinter import ttk


class PointSelector(ttk.Frame):
    """
    Selector for specific point to click at
    @callback
    - calls its callback with selected point tuple (x, y), or (None, None)
    """
    def __init__(self, master):
        super().__init__(master)
        self._callback = None

        self._mode = tk.StringVar()
        # radio between clicking at cursor and at set point
        cursor_option = ttk.Radiobutton(self, text="At cursor",
                                        variable=self._mode, value="CURSOR")
        point_option = ttk.Radiobutton(self, text="At point",
                                       variable=self._mode, value="POINT")
        cursor_option.grid(row=0, column=1)
        point_option.grid(row=2, column=1)

        self._mode.trace_add("write", self.handle_mode_change)

        # an entry? label? displaying coordinates
        (self._x, self._y) = (0, 0)
        self._COORD_TEXT = tk.StringVar()
        self._COORD_TEXT.set(f"({self._x}, {self._y})")
        self._COORD_ENTRY = ttk.Entry(self, textvariable=self._COORD_TEXT)

    def handle_mode_change(self, *args):
        # surely this is only called after the value is updated right?
        match self._mode:
            case "CURSOR":  # should grey out the point selection stuff
                pass
            case "POINT":
                pass

    def set_callback(self, callback):
        self._callback = callback
