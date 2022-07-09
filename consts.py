import pynput

DEFAULT_CPS = 10
ROUND_PRECISION = 1 # round to one decimal place
ACTIVE_STRING = "Currently Active"
NOT_ACTIVE_STRING = "Currently Not Active"

# pynput key constants
# also see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
KEY_R = pynput.keyboard.KeyCode.from_char("r")
KEY_ESC = pynput.keyboard.Key.esc