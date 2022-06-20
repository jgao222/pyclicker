import tkinter as tk
from tkinter import ttk
from tkinter.constants import HORIZONTAL, VERTICAL

# local imports
import consts


def init_gui(root):
    """
    initialize tkinter GUI
    args
      root: a root (`tk.Tk()`) to put the elements into
    returns
      the frame that got initialized
    """
    main_frame = ttk.Frame(root, padding=(30, 12, 30, 12))

    ACTIVE_TEXT = tk.StringVar(master=root, name="ACTIVE_DISPLAY")
    ACTIVE_TEXT.set(consts.NOT_ACTIVE_STRING)

    active_label = ttk.Label(main_frame, textvariable=ACTIVE_TEXT)
    active_label.grid(row=0, column=0, columnspan=2)

    CPS_text = tk.StringVar(master=root, name="CPS_DISPLAY")
    CPS_text.set("CPS (Rate): " + str(consts.DEFAULT_CPS))

    clicks_label = ttk.Label(main_frame, textvariable=CPS_text)
    clicks_label.grid(row=1, column=0, columnspan=2)
    slider = ttk.Scale(
        main_frame,
        orient=VERTICAL,
        length=500,
        # command=update_cps,
        name="cps_adjust_slider",
        from_=0.1,
        to=50.0,
        #  tickinterval=10.0
    )
    slider.set(consts.DEFAULT_CPS)
    slider.grid(row=2, column=0, rowspan=5)
    main_frame.grid(row=0, column=0)

    return (main_frame, {"cps_text": CPS_text, "active_text": ACTIVE_TEXT})
