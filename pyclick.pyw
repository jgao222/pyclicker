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


def init_bindings(root):
    """
    Initializes some bindings for the main program
    """
    # we need to use pynput listener b/c tkinter only listens for inputs when focused on root
    root.protocol(
        "WM_DELETE_WINDOW", handle_quit
    )  # end custom mainloop when press close btn


def init_kb_listener():
    kb_listener = pynput.keyboard.Listener(on_press=lambda k: set_last_key(k))
    kb_listener.start()


def set_last_key(key):
    global LAST_KEY, LAST_KEY_HANDLED
    LAST_KEY = key
    LAST_KEY_HANDLED = False


def handle_key(key, bindings):
    print(f"key was pressed: {key}")
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
    # root.resizable(False, False)
    root.title("pyclick")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ui = gui.MainGui(root)

    root.update() # prod it once to fit geometry
    root.minsize(root.winfo_width(), root.winfo_height()) # set min w/h to initial

    clickerObject = clicker.Clicker()
    clickerObject.add_callback_to_active_change(lambda state: update_texts(ui, state))

    # set up events going between
    # change in ui click speed setting to change the value in the object doing clicking
    ui.add_event_callback("cps_change", clickerObject.update_cps)
    # change in ui window selection to change the selected window in clicker object
    ui.add_event_callback("window_change", clickerObject.update_window)

    bindings = {consts.KEY_R: clickerObject.toggle_clicking, consts.KEY_ESC: handle_quit}

    init_bindings(root)
    init_kb_listener()

    while PROGRAM_RUNNING:
        # tkinter doesn't play nice when not called from main, so can't make a
        # callback from pynput keyboard handler call tkinter object methods
        # need to do it manually back here in the main loop
        if not LAST_KEY_HANDLED:
            handle_key(LAST_KEY, bindings)
            LAST_KEY_HANDLED = True

        # need to split tkinter main loop b/c need to loop the clicker in as well
        root.update_idletasks()
        root.update()
        clickerObject.update()
        time.sleep(0.01) # sleep for a bit to be lighter on resources


if __name__ == "__main__":
    main()
