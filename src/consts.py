import pynput

DEFAULT_CPS = 10
ROUND_PRECISION = 1  # round to one decimal place
ACTIVE_STRING = "Currently Active"
NOT_ACTIVE_STRING = "Currently Not Active"

# pynput key constants
# see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
KEY_R = pynput.keyboard.KeyCode.from_char("r")
KEY_ESC = pynput.keyboard.Key.esc

# blacklisted windows by name
# the program won't display these as choices, if they exist
WINDOWS_TO_FILTER = set([
    "Microsoft Text Input Application",
    "Program Manager",
])

# mock hwnd to represent clicking anywhere
ANYWHERE_HWND = -1  # assuming no actual window takes on hwnd of -1

DEBUG_LEVEL = 0  # -1 for no debugging


def dprint(string: str, level: int = 0):
    if level < DEBUG_LEVEL:
        print(string)
