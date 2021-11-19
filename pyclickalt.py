"""
This approach uses a constant main loop and sleeping, no threads. It is simpler
and works better than the other version. Disabling the pyautogui pause time was
the biggest factor in making it work.
"""
# import sys
import time
import pyautogui
import pynput

from pyclick import TIME_LAST
# from threading import Timer, active_count

CPS = 10
CLICK_INTERVAL_SECONDS = 1 / CPS

# CLICK_INTERVAL_MS = 1000 / CPS
RUNNING = True
MOUSE_CONTROLLER = pynput.mouse.Controller()
ACTIVE = False

KEY_R = pynput.keyboard.KeyCode.from_char("r")

CLICK_COUNTER = 0
SECONDS_COUNTER = 0
TIME_LAST = time.perf_counter()

pyautogui.PAUSE = 0

def on_press(key):
  global RUNNING
  # print(key == KEY_R)
  print("key was pressed")
  if key == pynput.keyboard.Key.esc:
    # print("exiting")
    # quit()
    RUNNING = False
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
  global ACTIVE
  ACTIVE = not ACTIVE


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
  global CLICK_COUNTER, SECONDS_COUNTER
  global TIME_LAST
  kb_listener = pynput.keyboard.Listener(on_press=on_press)
  kb_listener.start()

  while RUNNING:
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
      TIME_LAST = 0

  kb_listener.stop()


if __name__ == "__main__":
  main()
