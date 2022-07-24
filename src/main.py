"""
This approach uses a constant main loop and sleeping, no threads. It is simpler
and works better than the other version. Disabling the pyautogui pause time was
the biggest factor in making it work.
"""
# import sys
import time

import pyautogui
import pynput
import tkinter as tk
import sv_ttk  # theme

# local imports
import gui.gui as gui
import consts
import clicker


pyautogui.PAUSE = 0  # we want to go fast


# global variables

PROGRAM_RUNNING = True

LAST_KEY = None
LAST_KEY_HANDLED = (
    True  # indicates whether or not the latest key input has been handled
)

BINDINGS = {}


def init_bindings(root, clicker):
    """
    Initializes some bindings for the main program
    @args
    - root: the root tkinter widget
    - clicker: the clicker object
    """
    global BINDINGS
    # we need to use pynput listener b/c tkinter only listens for inputs when
    # focused on its window
    root.protocol(
        "WM_DELETE_WINDOW", handle_quit
    )  # end custom mainloop when press close btn

    BINDINGS = {
        consts.KEY_R: clicker.toggle_clicking,
        consts.KEY_ESC: handle_quit,
    }


def init_kb_listener():
    kb_listener = pynput.keyboard.Listener(on_press=lambda k: set_last_key(k))
    kb_listener.start()


def set_last_key(key):
    global LAST_KEY, LAST_KEY_HANDLED
    LAST_KEY = key
    LAST_KEY_HANDLED = False


def handle_key(key, bindings):
    consts.dprint(f"key was pressed: {key}", 2)
    # use custom bindings method instead of tkinter's since it works better
    # to capture input, as pynput listener operates in own thread
    if key in bindings:
        bindings[key]()  # this is a function call


def handle_quit():
    global PROGRAM_RUNNING
    PROGRAM_RUNNING = False


def update_texts(ui: gui.MainGui, active):
    ui.respond_event("active_change", active)


def main():
    global LAST_KEY_HANDLED

    root = tk.Tk()
    sv_ttk.set_theme("light")

    # root.resizable(False, False)
    root.title(consts.WINDOW_NAME)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ui = gui.MainGui(root)

    # this is a hack to make entries play nicer/more as expected
    # so that focusout events will happen when user clicks out of an entry
    def try_focus(e):
        try:
            e.widget.focus()
        except Exception:
            pass
    root.bind_all("<Button-1>", try_focus)
    root.update()  # prod it once to fit geometry

    # lock min w/h to initial
    root.minsize(root.winfo_width(), root.winfo_height())

    clickerObject = clicker.Clicker()
    clickerObject.add_callback_to_active_change(
        lambda state: ui.respond_event("active_change", state)
    )

    # set up events going between
    # change in ui click speed setting changes the cps in clickerObject
    ui.add_event_callback("cps_change", clickerObject.update_cps)
    # change in ui window selection changes the allowed window
    ui.add_event_callback("window_change", clickerObject.update_window)
    # add position change
    ui.add_event_callback("click_pos_change", clickerObject.update_click_point)
    # lmb or rmb click type change
    ui.add_event_callback("click_type_change", clickerObject.update_click_btn)

    init_bindings(root, clickerObject)
    init_kb_listener()

    while PROGRAM_RUNNING:
        # tkinter doesn't play nice when not called from main, so can't make a
        # callback from pynput keyboard handler call tkinter object methods
        # need to do it manually back here in the main loop
        if not LAST_KEY_HANDLED:
            handle_key(LAST_KEY, BINDINGS)
            LAST_KEY_HANDLED = True

        # split tkinter main loop b/c need to loop the clicker in as well
        root.update_idletasks()
        root.update()
        clickerObject.update()
        time.sleep(0.01)  # sleep for a bit to be lighter on resources
        # note this technically limits the click rate to 100


if __name__ == "__main__":
    main()
