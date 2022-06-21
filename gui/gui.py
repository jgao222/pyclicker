import tkinter as tk
from tkinter import ttk
from tkinter.constants import VERTICAL

# local imports
import consts


class MainGui(tk.Frame):
    def __init__(self, parent):
        root = parent
        super().__init__(root)
        # main_frame = ttk.Frame(root, padding=(30, 12, 30, 12))

        self._ACTIVE_TEXT = tk.StringVar(master=root, name="ACTIVE_DISPLAY")
        self._ACTIVE_TEXT.set(consts.NOT_ACTIVE_STRING)

        active_label = ttk.Label(self, textvariable=self._ACTIVE_TEXT)
        active_label.grid(row=0, column=0, columnspan=2, pady="0 20", sticky="nw")

        self._CPS_TEXT = tk.StringVar(master=root, name="CPS_DISPLAY")
        self._CPS_TEXT.set("CPS (Rate): " + str(consts.DEFAULT_CPS))

        clicks_label = ttk.Label(self, textvariable=self._CPS_TEXT)
        clicks_label.grid(row=1, column=0, columnspan=2)

        self._CPS_SCALE_VALUE = tk.DoubleVar()
        self._CPS_SCALE_VALUE.set(consts.DEFAULT_CPS)
        slider = ttk.Scale(
            self,
            orient=VERTICAL,
            length=500,
            # make sure to configure callback for this in outside code
            name="cps_adjust_slider",
            from_=50.0,
            to=1.0,
            variable=self._CPS_SCALE_VALUE,
            command=self.update_cps
            # not supported on ttk.scale
            #  tickinterval=10.0
        )
        slider.grid(row=2, column=0, rowspan=5, columnspan=2)

        self.grid(row=0, column=0, sticky="nsw", padx="15 15", pady="20 20")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # put externally visible variables into a map
        self._externally_visible_variables = {
            "cps_text": self._CPS_TEXT,
            "active_text": self._ACTIVE_TEXT,
            "cps_scale_value": self._CPS_SCALE_VALUE
        }

        # listeners for updates to the cps value
        self._cps_listeners = list()


    def get_vars(self):
        """
        Please don't modify the map returned by this function!
        """
        return self._externally_visible_variables


    def update_cps(self):
        cps_val = self._CPS_SCALE_VALUE.get()
        self._CPS_TEXT.set("CPS (Rate): " + str(cps_val))
        for listener in self._cps_listeners:
            listener.update_cps(cps_val)


    def subscribe_cps_listener(self, listener):
        """
        A listener to the cps value from the scale on this object
        should have an update_cps method accepting one value
        which is the new cps to update to
        """
        self._cps_listeners.append(listener)


    def set_active_text(self, text):
        self._ACTIVE_TEXT.set(text)