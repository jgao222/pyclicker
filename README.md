## Python Clicking Script

This is a simple script for an autoclicker, made in Python.

It uses `pynput` for detecting keyboard input and `pyautogui` for sending clicks.

Also uses `tkinter` to make a simple gui.

Currently sets `R` key to toggle clicking, `ESC` as a general failsafe to exit the program.


### GUI

The clicking speed (clicks per second) can be set from 0.1 to 50 via the slider, in steps of 0.1

The GUI also supports selecting a specific window that the clicker should be active in.

If an option other than `"Anywhere"` is selected, the clicker will only click in the specified window when that window is focused/in foreground.