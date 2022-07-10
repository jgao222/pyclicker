"""
The main GUI and misc gui elements for the program
"""
import tkinter as tk
from tkinter import ttk
from tkinter.constants import VERTICAL

# local imports
import gui.activity_label as activity_label
import gui.slider as slider
import gui.window_selector as window_selector


class MainGui(tk.Frame):
    def __init__(self, parent):
        root = parent
        super().__init__(root)

        # listeners for internal events going outwards
        self._event_callbacks = dict([
            ("cps_change", list()),
            ("window_change", list())
        ])

        # listeners for external events coming in
        self._event_listeners = dict([
            ("active_change", list())
        ])

        # a label indicating if the clicker is active or not
        active_label = activity_label.ActivityLabel(self)
        self._event_listeners["active_change"].append(active_label.update)
        active_label.grid(row=0, column=0, columnspan=2, pady="0 20", sticky="")

        # a slider with a label showing its current value
        self._slider = slider.Slider(self, 0.1, 50)
        self._slider.set_callback(lambda new_cps:
            self.emit_event("cps_change", new_cps)
        )
        self._slider.grid(row=2, column=0, rowspan=5, columnspan=2)

        # a dropdown (combobox) showcasing open windows
        window_selection = window_selector.WindowSelector(self)
        window_selection.set_callback(lambda new_window:
            self.emit_event("window_change", new_window)
        ) # TODO propagate selection out to program
        window_selection.grid(row=0, column=3)

        # grid self onto root
        self.grid(row=0, column=0, sticky="nsw", padx="15 15", pady="20 20")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


    def get_vars(self):
        """
        Please don't modify the map returned by this function!
        """
        return self._externally_visible_variables


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
        Has the UI respond to an external event, which contains one value
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
