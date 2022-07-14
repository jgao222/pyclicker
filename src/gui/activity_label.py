import tkinter as tk
from tkinter import ttk
import consts

class ActivityLabel(tk.Frame):
    """
    A label showing the activity/state of something
    """ # specific purpose object, could be generalized later
    def __init__(self, parent):
        super().__init__(parent)
        self._ACTIVE_TEXT = tk.StringVar(master=parent, name="ACTIVE_DISPLAY")
        self._ACTIVE_TEXT.set(consts.NOT_ACTIVE_STRING)

        self._label = ttk.Label(self, textvariable=self._ACTIVE_TEXT)
        self._label.grid(row=0, column=0, sticky="nsew")


    def update(self, state: bool):
        """
        Update what is shown in this label
        @args
        - state: boolean representing the activity of the thing this label represents
        """
        if state:
            self._ACTIVE_TEXT.set(consts.ACTIVE_STRING)
        else:
            self._ACTIVE_TEXT.set(consts.NOT_ACTIVE_STRING)
