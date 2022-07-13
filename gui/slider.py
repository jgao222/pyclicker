import tkinter as tk
from tkinter import ttk
from tkinter.constants import VERTICAL

import consts

class Slider(tk.Frame):
    """
    Wrapper class for a slider with a display of its current value
    """
    def __init__(self, parent, start: float, end: float):
        super().__init__(parent)

        self._callback = None
        self._cps_val = consts.DEFAULT_CPS

        self._CPS_TEXT = tk.StringVar(master=parent, name="CPS_DISPLAY")
        self._CPS_TEXT.set("CPS (Rate): " + str(consts.DEFAULT_CPS))

        clicks_label = ttk.Label(self, textvariable=self._CPS_TEXT)
        clicks_label.grid(row=0, column=0, columnspan=2)

        self._CPS_SCALE_VALUE = tk.DoubleVar()
        self._CPS_SCALE_VALUE.set(consts.DEFAULT_CPS)

        self._slider = ttk.Scale(
            self,
            orient=VERTICAL,
            length=500,
            # make sure to configure callback for this in outside code
            name="cps_adjust_slider",
            from_=end,
            to=start,
            variable=self._CPS_SCALE_VALUE,
            command=self._update,
            # not supported on ttk.scale
            #  tickinterval=10.0
        )
        self._slider.grid(row=1, column=0, rowspan=5, columnspan=2)


    def _update(self, cps):
        cps_val = round(float(cps), consts.ROUND_PRECISION)
        self._CPS_TEXT.set("CPS (Rate): " + str(cps_val))
        if self._callback:
            self._callback(cps_val)


    def set_callback(self, callback):
        """
        Set the callback to be called when the slider is changed
        @args
        - callback: a function which takes 1 argument, the value of the slider
        """
        self._callback = callback

