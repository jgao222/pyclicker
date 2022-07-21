import re
import tkinter as tk
from tkinter import ttk
from tkinter.constants import VERTICAL

import consts


class Slider(tk.Frame):
    """
    Wrapper class for a slider with a display of its current value
    @callback
    - calls its callback with an updated value of cps rounded to nearest tenth
    """
    def __init__(self, parent, start: float, end: float):
        super().__init__(parent)

        self._start = start
        self._end = end

        self._callback = None
        self._cps_val = consts.DEFAULT_CPS

        label = ttk.Label(self, text="CPS (Rate): ")
        label.grid(row=0, column=0, pady="0 10")

        self._VALUE_TEXT = tk.StringVar(master=parent, name="CPS_DISPLAY")
        self._VALUE_TEXT.set(str(consts.DEFAULT_CPS))
        # self._VALUE_TEXT.trace_add("write", self._handle_text_update)

        check_valid_wrapper = (self.register(self.check_valid), '%P', '%V')
        self._cps_entry = ttk.Entry(
            self, textvariable=self._VALUE_TEXT, width=5,
            validate="all",
            validatecommand=check_valid_wrapper)
        self._cps_entry.bind("<Return>",
                             lambda _:
                             self.check_valid(
                                self._VALUE_TEXT.get(), "focusout"
                             ))
        self._cps_entry.grid(row=0, column=1, pady="0 10")

        self._VALUE = tk.DoubleVar()
        self._VALUE.set(consts.DEFAULT_CPS)

        self._slider = ttk.Scale(
            self,
            orient=VERTICAL,
            length=500,
            # make sure to configure callback for this in outside code
            name="cps_adjust_slider",
            from_=end,
            to=start,
            variable=self._VALUE,
            command=self._update,
            # not supported on ttk.scale
            #  tickinterval=10.0
        )

        def override_leftclick(event):  # change left click to jump instantly
            self._slider.event_generate("<Button-3>", x=event.x, y=event.y)
            return "break"
        self._slider.bind("<Button-1>", override_leftclick)
        self._slider.grid(row=1, column=0, rowspan=5, columnspan=2)

    def _update(self, cps, update_text=True):
        consts.dprint("update called", 2)
        cps_val = round(float(cps), consts.ROUND_PRECISION)
        if update_text:
            self._VALUE_TEXT.set(str(cps_val))  # set the visible entry text
        self._cps_entry.state(["!invalid"])
        if self._callback:
            self._callback(cps_val)

    def _handle_text_update(self):
        tval = None
        try:
            tval = float(self._VALUE_TEXT.get())
            if tval > self._end or tval < self._start:  # clamp
                if tval > self._end:
                    tval = self._end
                elif tval < self._start:
                    tval = self._start
            self._update(tval, False)
        except ValueError:
            self._VALUE_TEXT(str(self._VALUE.get()))

    def set_callback(self, callback):
        """
        Set the callback to be called when the slider is changed
        @args
        - callback: a function which takes 1 argument, the value of the slider
        """
        self._callback = callback

    def check_valid(self, newval, op):
        consts.dprint(f"called check_valid: {newval}, {op}")
        valid = False
        if op == 'key' or op == 'focusin':
            valid = re.match('^[0-9]*.?[0-9]?$', newval) is not None \
                and len(newval) <= 5
        elif op == 'focusout':
            val = None
            try:
                val = float(newval)
            except ValueError:
                print("Non float entry")
            except TypeError:
                print("TypeError: This shouldn't happen!")
            valid = val is not None
            self._handle_text_update()
        self._cps_entry.state(["!invalid"] if valid else ["invalid"])
        return valid
