"""
This approach uses a constant main loop and sleeping, no threads. It is simpler
and works better than the other version. Disabling the pyautogui pause time was
the biggest factor in making it work.
"""
# import sys
import time
from tkinter.constants import HORIZONTAL
import pyautogui
import pynput
import tkinter as tk
from tkinter import ttk


DEFAULT_CPS = 10

MOUSE_CONTROLLER = pynput.mouse.Controller()

# also see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
KEY_R = pynput.keyboard.KeyCode.from_char("r")

pyautogui.PAUSE = 0

root = tk.Tk()
root.title("pyclick")

CLICK_COUNTER = 0
SECONDS_COUNTER = 0
TIME_LAST = time.perf_counter()

CLICK_COUNT = 0

CPS = DEFAULT_CPS
CPS_text = tk.StringVar()
CPS_text.set(DEFAULT_CPS)
CLICK_INTERVAL_SECONDS = 1 / CPS
# CLICK_INTERVAL_MS = 1000 / CPS


RUNNING = True
ACTIVE = False

ACTIVE_STRING = "Active"
NOT_ACTIVE_STRING = "Currently Not Active"
ACTIVE_TEXT = tk.StringVar()
ACTIVE_TEXT.set(NOT_ACTIVE_STRING)

PRECISION = 1

UPDATE_TEXT_FLAG = False # because we want to update text on callback, but tkinter doesn't like that
                         # since pynput listeners and callbacks run in their own thread

def init_gui():
  main_frame = ttk.Frame(root)
  active_label = ttk.Label(main_frame, textvariable=ACTIVE_TEXT)
  active_label.pack()

  label = ttk.Label(main_frame, text="CPS (Rate)")
  label.pack()

  slider = ttk.Scale(main_frame, orient=HORIZONTAL, length=500, command=update_cps, from_=0.1, to=50.0)
  slider.set(DEFAULT_CPS)
  slider.pack()

  clicks_label = ttk.Label(main_frame, textvariable=CPS_text)
  clicks_label.pack()

  main_frame.pack()


def init_bindings():
  # we need to use pynput listener b/c tkinter only listens for inputs when focused on root
  kb_listener = pynput.keyboard.Listener(on_press=handle_key)
  kb_listener.start()
  # root.bind("<KeyPress>", handle_key)
  # root.bind("<Escape>", handle_quit)
  root.protocol("WM_DELETE_WINDOW", handle_quit) # end tcustom mainloop when press close btn



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


def update_cps(click_speed=DEFAULT_CPS):
  global CPS
  # print(type(click_speed))
  click_speed = round(float(click_speed), PRECISION)
  CPS_text.set(str(click_speed))
  CPS = click_speed
  # CLICK_COUNT += 1
  # COUNT_VAR.set(CLICK_COUNT)


def on_click(x, y, button, pressed):
  # print(x, y, button, pressed)
  # toggle_clicking()
  print("nop")


def toggle_clicking():
  print("clicking toggled")
  global ACTIVE, UPDATE_TEXT_FLAG
  ACTIVE = not ACTIVE

  UPDATE_TEXT_FLAG = True


def update_texts():
  if ACTIVE:
    ACTIVE_TEXT.set(ACTIVE_STRING)
  else:
    ACTIVE_TEXT.set(NOT_ACTIVE_STRING)


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
    TIME_LAST = 0 # on last call of this function, reset time_last value


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


# COUNT_VAR = tk.StringVar()

init_gui()
init_bindings()

# root.mainloop()
while RUNNING:
  if UPDATE_TEXT_FLAG:
    update_texts()
    UPDATE_TEXT_FLAG = False
  root.update_idletasks()
  root.update()
  do_clicking()


