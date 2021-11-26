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


CPS = 10
CLICK_INTERVAL_SECONDS = 1 / CPS

# CLICK_INTERVAL_MS = 1000 / CPS
RUNNING = True
MOUSE_CONTROLLER = pynput.mouse.Controller()
ACTIVE = False

# also see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
KEY_R = pynput.keyboard.KeyCode.from_char("r")

CLICK_COUNTER = 0
SECONDS_COUNTER = 0
TIME_LAST = time.perf_counter()

CLICK_COUNT = 0


pyautogui.PAUSE = 0

def init_gui():
  main_frame = ttk.Frame(root)
  label = tk.Label(main_frame, text="text")
  label.pack()

  button = tk.Button(main_frame, text="click me!", command=update_score)
  button.pack()

  clicks_label = tk.Label(main_frame, textvariable=COUNT_VAR)
  clicks_label.pack()

  main_frame.pack()


def init_bindings():
  # we need to use pynput listener b/c tkinter only listens for inputs when focused on root
  kb_listener = pynput.keyboard.Listener(on_press=handle_key)
  kb_listener.start()
  # root.bind("<KeyPress>", handle_key)
  # root.bind("<Escape>", handle_quit)


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


def update_score():
  global CLICK_COUNT
  CLICK_COUNT += 1
  COUNT_VAR.set(CLICK_COUNT)


def on_click(x, y, button, pressed):
  # print(x, y, button, pressed)
  # toggle_clicking()
  print("nop")


def toggle_clicking():
  print("clicking toggled")
  global ACTIVE
  ACTIVE = not ACTIVE


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


root = tk.Tk()
root.title("pyclick")

COUNT_VAR = tk.StringVar()

init_gui()
init_bindings()

# root.mainloop()
while RUNNING:
  root.update_idletasks() # this is why we can't just * import
  root.update()
  do_clicking()


