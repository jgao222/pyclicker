"""
The main GUI and misc gui elements for the program
"""
import tkinter as tk
from tkinter import ttk

# local imports
import gui.activity_label as activity_label
import gui.slider as slider
import gui.window_selector as window_selector
import gui.point_selector as point_selector
import gui.button_selector as button_selector

import consts


class MainGui(tk.Frame):
    def __init__(self, parent):
        root = parent
        super().__init__(root)

        # listeners for internal events going outwards
        self._event_callbacks = dict([
            ("cps_change", list()),
            ("window_change", list()),
            ("click_pos_change", list()),
            ("click_type_change", list()),
            ("request_set_click_position", list())
        ])
        # listeners for external events coming in
        self._event_listeners = dict([
            ("active_change", list()),
            ("set_click_position", list()),
        ])
        # doing listeners like this is a bit wasteful for space, it might be
        # better to lazily instantiate them, default to empty dicts, and fill
        # them in when necessary

        # a label indicating if the clicker is active or not
        active_label = activity_label.ActivityLabel(
            self, text=" Clicker State ")
        self.add_event_handler("active_change", active_label.update)
        active_label.grid(row=0, column=0,
                          columnspan=2, pady="0 20", sticky="NSEW")
        # force an update in order to lock it at the first dims it gets
        self.update()
        active_label.configure(width=active_label.winfo_width(),
                               height=active_label.winfo_height() + 35)
        # yes that's a magic number, gah

        # a slider with a label showing its current value
        self._slider = slider.Slider(self, 0.1, 50)
        self._slider.set_callback(
            lambda new_cps: self.emit_event("cps_change", new_cps)
        )
        self._slider.grid(row=1, column=0, rowspan=5, columnspan=2)

        # a separator to divide the slider from window selector
        sep2 = ttk.Separator(self, orient="vertical")
        sep2.grid(column=2, row=0, rowspan=9, sticky="ns", padx="20 20")

        # labelframe containing options
        options_frame = ttk.LabelFrame(self, text="Options")

        # click type selector for LMB or RMB (left/right mouse buttons)
        self._btn_selection = button_selector.ButtonSelector(options_frame)
        self._btn_selection.set_callback(
            lambda new_btn: self.emit_event("click_type_change", new_btn)
        )
        self._btn_selection.grid(row=0, column=0, columnspan=2,
                                 padx="20 0")

        # separator for button and window selector
        sep3 = ttk.Separator(options_frame, orient="horizontal")
        sep3.grid(row=1, column=0, columnspan=2, padx="20 20", pady="20 20",
                  sticky="ew")

        # a dropdown (combobox) showcasing open windows
        window_selection = window_selector.WindowSelector(options_frame)
        window_selection.set_callback(
            lambda new_window: self.emit_event("window_change", new_window)
        )
        window_selection.grid(row=2, column=0, columnspan=2, padx="20 20")

        # separator to divide window and point selectors
        sep4 = ttk.Separator(options_frame, orient="horizontal")
        sep4.grid(row=3, column=0, columnspan=2, padx="20 20", pady="20 20",
                  sticky="ew")

        # point selector for where to click
        self._point_selection = point_selector.PointSelector(
            options_frame,)
        self._point_selection.set_callback(
            lambda new_point: self.emit_event("click_pos_change", new_point)
        )
        self._point_selection.set_btn_callback(
            lambda: self.emit_event("request_set_click_position", None))
        self.add_event_handler(
            "set_click_position",
            self._point_selection.handle_external_set_coords)
        self._point_selection.grid(row=4, column=0, padx="20 0",
                                   sticky="nw")

        options_frame.grid(row=0, column=3, rowspan=5, sticky="nsew")

        # grid self onto root
        self.grid(row=0, column=0, sticky="nsw", padx="15 15", pady="20 20")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def emit_event(self, event, value):
        if event in self._event_callbacks:
            for callback in self._event_callbacks[event]:
                callback(value)
        else:
            consts.dprint("Tried to emit event with no external" +
                          " listeners for it", 1)

    def add_event_callback(self, event, callback):
        if event in self._event_callbacks:
            self._event_callbacks[event].append(callback)
        else:
            consts.dprint("Tried to add callback to nonexistent UI event", 1)

    def add_event_handler(self, event, handler):
        if event in self._event_listeners:
            self._event_listeners[event].append(handler)
        else:
            consts.dprint("Tried to add handler for nonexistent outside event",
                          1)

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
