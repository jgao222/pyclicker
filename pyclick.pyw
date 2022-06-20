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
from tkinter import ttk

# local imports
import gui.gui as gui
import consts

# global variables
MOUSE_CONTROLLER = pynput.mouse.Controller()

# also see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
KEY_R = pynput.keyboard.KeyCode.from_char("r")

pyautogui.PAUSE = 0

CLICK_COUNTER = 0
SECONDS_COUNTER = 0
TIME_LAST = time.perf_counter()

CLICK_COUNT = 0

CPS = consts.DEFAULT_CPS
CLICK_INTERVAL_SECONDS = 1 / CPS
# CLICK_INTERVAL_MS = 1000 / CPS

RUNNING = True
ACTIVE = False


def init_bindings(root):
    # we need to use pynput listener b/c tkinter only listens for inputs when focused on root
    kb_listener = pynput.keyboard.Listener(on_press=handle_key)
    kb_listener.start()
    # root.bind("<KeyPress>", handle_key)
    # root.bind("<Escape>", handle_quit)
    root.protocol(
        "WM_DELETE_WINDOW", handle_quit
    )  # end tcustom mainloop when press close btn


def handle_key(key):
    global RUNNING

    print("key was pressed")
    # print(event.keysym)
    # key = event.keysym
    if key == KEY_R:
        toggle_clicking()
    elif key == pynput.keyboard.Key.esc:
        handle_quit()


def handle_quit():
    # root.destroy()
    global RUNNING
    RUNNING = False


def update_cps(display_var, click_speed=consts.DEFAULT_CPS):
    global CPS
    # print(type(click_speed))
    click_speed = round(float(click_speed), consts.ROUND_PRECISION)
    display_var.set(str(click_speed))
    CPS = click_speed
    # CLICK_COUNT += 1
    # COUNT_VAR.set(CLICK_COUNT)


def on_click(x, y, button, pressed):
    # print(x, y, button, pressed)
    # toggle_clicking()
    print("nop")


def toggle_clicking():
    global ACTIVE, UPDATE_TEXT_FLAG
    print("clicking toggled to " + str(not ACTIVE))
    ACTIVE = not ACTIVE

    UPDATE_TEXT_FLAG = True


def update_texts(active_text):
    if ACTIVE:
        active_text.set(consts.ACTIVE_STRING)
    else:
        active_text.set(consts.NOT_ACTIVE_STRING)


def do_clicking():
    global CLICK_COUNTER, TIME_LAST, SECONDS_COUNTER
    if ACTIVE:
        pyautogui.click()

        CLICK_COUNTER += 1
        cur_time = time.perf_counter()
        if TIME_LAST:
            SECONDS_COUNTER += cur_time - TIME_LAST
        TIME_LAST = cur_time
        # print(f"clicked at {CLICK_COUNTER} / {SECONDS_COUNTER} Clicks per sec")
        adjust_speed()
        time.sleep(CLICK_INTERVAL_SECONDS)
    else:
        TIME_LAST = 0  # on last call of this function, reset time_last value


def adjust_speed():
    global CLICK_COUNTER, SECONDS_COUNTER
    global CLICK_INTERVAL_SECONDS

    if CLICK_COUNTER and SECONDS_COUNTER:
        if (CLICK_COUNTER / SECONDS_COUNTER) < CPS:
            CLICK_INTERVAL_SECONDS /= 2
        else:
            CLICK_INTERVAL_SECONDS = 1 / CPS

    if CLICK_COUNTER > 63:
        CLICK_COUNTER = 0
        SECONDS_COUNTER = 0


def print_debug():
    print("debug")


def main():
    # root.mainloop()
    root = tk.Tk()
    root.title("pyclick")
    ui, tk_vars = gui.init_gui(root)
    # need to configure the scale to call the handler for it
    display_var = tk_vars["cps_text"]
    cps_slider = ui.children["cps_adjust_slider"]
    cps_slider.configure(command=lambda _: update_cps(display_var, cps_slider.get()))

    active_text_var = tk_vars["active_text"]

    init_bindings(root)

    # because we want to update text on callback, but tkinter doesn't like that
    # since pynput listeners and callbacks run in their own thread
    UPDATE_TEXT_FLAG = False
    while RUNNING:
        if UPDATE_TEXT_FLAG:
            update_texts(active_text_var)
            UPDATE_TEXT_FLAG = False
        root.update_idletasks()
        root.update()
        do_clicking()


if __name__ == "__main__":
    main()
