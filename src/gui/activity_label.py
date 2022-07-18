import tkinter as tk
from tkinter import ttk
import consts


class ActivityLabel(ttk.LabelFrame):
    """
    A label showing the activity/state of something
    """  # specific purpose object, could be generalized later

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._ACTIVE_TEXT = tk.StringVar(master=parent, name="ACTIVE_DISPLAY")
        self._ACTIVE_TEXT.set(consts.NOT_ACTIVE_STRING)

        self._label = ttk.Label(self, textvariable=self._ACTIVE_TEXT,
                                foreground=consts.NOT_ACTIVE_COLOR)
        # place instead of grid to center for some reason doesn't compute
        # the height correctly, and results in needing magic numbers to offset
        # self._label.place(relx=0.5, rely=0.5, anchor="center")
        self._label.grid(row=0, column=0, pady="0 10")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def update(self, state: bool):
        """
        Update what is shown in this label
        @args
        - state: boolean representing the activity of the thing this label
                 represents
        """
        if state:
            self._ACTIVE_TEXT.set(consts.ACTIVE_STRING)
            self._label.configure(foreground=consts.ACTIVE_COLOR)
        else:
            self._ACTIVE_TEXT.set(consts.NOT_ACTIVE_STRING)
            self._label.configure(foreground=consts.NOT_ACTIVE_COLOR)
