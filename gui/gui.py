"""
The main GUI and misc gui elements for the program
"""
import tkinter as tk
from tkinter import ttk
from tkinter.constants import VERTICAL

# local imports
import consts
import gui.activity_label as activity_label


class MainGui(tk.Frame):
    def __init__(self, parent):
        root = parent
        super().__init__(root)

        # listeners for internal events going outwards
        self._event_callbacks = dict([
            ("cps_change", list())
        ])

        # listeners for external events coming in
        self._event_listeners = dict([
            ("active_change", list())
        ])

        # main_frame = ttk.Frame(root, padding=(30, 12, 30, 12))
        active_label = activity_label.ActivityLabel(self)
        self._event_listeners["active_change"].append(active_label.update)
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


    def get_vars(self):
        """
        Please don't modify the map returned by this function!
        """
        return self._externally_visible_variables


    def update_cps(self, new_cps):
        cps_val = round(float(new_cps), consts.ROUND_PRECISION)
        self._CPS_TEXT.set("CPS (Rate): " + str(cps_val))
        # send external listeners message that the value was updated
        self.emit_event("cps_change", cps_val)


    def emit_event(self, event, value):
        if event in self._event_callbacks:
            for callback in self._event_callbacks[event]:
                callback(value)
        else:
            print("Tried to emit event with no external listeners for it")


    def add_event_callback(self, event, callback):
        if event in self._event_callbacks:
            self._event_callbacks[event].append(callback)
        else:
            print("Tried to add callback to nonexistent UI event")


    def respond_event(self, event, value):
        """
        Has the UI respond to an event, which contains one value
        Event types not enforced, limited flexibility here
        UI elements which need to respond to these events should be set up in
            the initialization of the UI
        @args
        - event: a string event name
        - value: a value associated with the event
        """
        if event in self._event_listeners:
            for callback in self._event_listeners[event]:
                callback(value)
        else:
            print("Tried to make UI respond to event it isn't listening for")


    def set_active_text(self, text):
        self._ACTIVE_TEXT.set(text)
