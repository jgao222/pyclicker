"""
This approach uses threading and appears to be limited to a max of 8 CPS,
despite the threading.Timer intervals being set to ridiculously short intervals.
"""
# import sys
import time
import pyautogui
import pynput
from threading import Timer

CPS = 10
CLICK_INTERVAL_SECONDS = 1 / CPS

# CLICK_INTERVAL_MS = 1000 / CPS
RUNNING = True
MOUSE_CONTROLLER = pynput.mouse.Controller()
ACTIVE = False

KEY_R = pynput.keyboard.KeyCode.from_char("r")
TIME_LAST = time.time()

CLICK_COUNTER = 0
SECONDS_COUNTER = 0

pyautogui.PAUSE = 0 # it seems any amount of pause time messes up the rates

def on_press(key):
  # print(key == KEY_R)
  print("key was pressed")
  if key == pynput.keyboard.Key.esc:
    # print("exiting")
    # quit()
    return False
  elif key == KEY_R:
    # print("nop")
    toggle_clicking()
  return True

def on_click(x, y, button, pressed):
  # print(x, y, button, pressed)
  # toggle_clicking()
  print("nop")


def toggle_clicking():
  # print("clicking toggled")
  global TIME_LAST
  global TIMER_GLOBAL
  global ACTIVE
  if ACTIVE:
    ACTIVE = False
  else:
    ACTIVE = True
    TIME_LAST = time.time()
    do_click()
    # print("should have started clicking")


def do_click():
  global TIME_LAST
  global CLICK_COUNTER, SECONDS_COUNTER
  global CLICK_INTERVAL_SECONDS
  # print(ACTIVE)
  if ACTIVE:
    pyautogui.click()
    CLICK_COUNTER += 1
    cur_time = time.time()
    delta = cur_time - TIME_LAST
    SECONDS_COUNTER += delta
    true_cps = CLICK_COUNTER / SECONDS_COUNTER
    # print(delta - CLICK_INTERVAL_SECONDS)
    print(f"{true_cps} < {CPS}")
    if true_cps < CPS: # automatic speed up if we are behind on speed
      CLICK_INTERVAL_SECONDS /= 2
    else:
      CLICK_INTERVAL_SECONDS = 1 / CPS
    print(f"CLICK INTERVAL: {CLICK_INTERVAL_SECONDS}")
    t = Timer(CLICK_INTERVAL_SECONDS, do_click)
    t.daemon = True
    t.start()
    TIME_LAST = time.time()
  # print("done click")


def print_debug():
  print("debug")


def main():
  global CLICK_COUNTER, SECONDS_COUNTER
  kb_listener = pynput.keyboard.Listener(on_press=on_press)
  # ms_listener = pynput.mouse.Listener(on_click=on_click)e
  kb_listener.start()
  # ms_listener.start()

  while kb_listener.running:
    # may limit the clicking speed
    if CLICK_COUNTER >= 64:
      CLICK_COUNTER %= 64
      SECONDS_COUNTER = 0
    time.sleep(1) # keep the program alive b/c i don't know otherwise how
    # print("heartbeat")
  kb_listener.stop()


if __name__ == "__main__":
  main()
