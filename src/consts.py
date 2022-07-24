import pynput

WINDOW_NAME = "pyclick"

DEFAULT_CPS = 10.0
ROUND_PRECISION = 1  # round to one decimal place
ACTIVE_STRING = "Active"
ACTIVE_COLOR = "green"
NOT_ACTIVE_STRING = "Not Active"
NOT_ACTIVE_COLOR = "red"

# pynput key constants
KEY_R = pynput.keyboard.KeyCode.from_char("r")
KEY_ESC = pynput.keyboard.Key.esc
# see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
# for tkinter keys

# blacklisted windows by name
# the program won't display these as choices, if they exist
WINDOWS_TO_FILTER = set([
    "Microsoft Text Input Application",
    "Program Manager",
    "pyclick",  # don't click in self
])

# mock hwnd to represent clicking anywhere
ANYWHERE_HWND = -1  # assuming no actual window takes on hwnd of -1

DEBUG_LEVEL = 2  # -1 for no debugging


def dprint(string: str, level: int = 0):
    if level <= DEBUG_LEVEL:
        print(string)
