import tkinter as tk
from tkinter import ttk

import win32gui
import consts


class WindowSelector(tk.Frame):
    """
    A combobox (list) of open windows for the user to select
    @callback
    - calls its callback with the hwnd of the currently selected window
    """
    def __init__(self, parent):
        super().__init__(parent)

        self._title = ttk.Label(self, text="Click in:")
        self._title.grid(row=0, column=0, padx="20 10")

        self._selected_text = tk.StringVar()
        self._selected_text.set("Anywhere")
        self._window_to_hwnd = dict()

        self._selection_box = ttk.Combobox(
            self,
            textvariable=self._selected_text,
            width=40,
            values=["Anywhere"],
            state="readonly"
        )

        self.refresh_selection_list()

        self._selection_box.grid(row=0, column=1)
        self._selection_box.bind("<<ComboboxSelected>>", lambda _: self._update())

        # add a button to manually refresh the window list
        refresh_button = ttk.Button(self, text="Refresh", state="readonly", command=self.refresh_selection_list)
        refresh_button.grid(row=0, column=2)


    def _update(self):
        print("selector updated")
        self._selection_box.selection_clear()
        self.master.focus()
        if self._callback:
            self._callback(self._window_to_hwnd[self._selected_text.get()])


    def set_callback(self, callback):
        self._callback = callback


    def refresh_selection_list(self):
        old_selection = self._selected_text.get()
        old_hwnd = self._window_to_hwnd[old_selection]

        self._selection_box["values"] = ()
        self._window_to_hwnd.clear()

        self._window_to_hwnd[old_selection] = old_hwnd # put the previously selected window back in
        # this will make it so that if the user doesn't change the selection but the window text
        # changes, it will still recognize the right thing and have a valid hwnd

        def clear_and_get_window_list(hwnd, _ignore):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if window_text and window_text not in consts.WINDOWS_TO_FILTER:
                    self._window_to_hwnd[window_text] = hwnd

        win32gui.EnumWindows(clear_and_get_window_list, None)
        self._selection_box["values"] = sorted(list(self._window_to_hwnd.keys()))

        # manually put in the anywhere option as the first choice
        tmp_copy = list(self._selection_box["values"])
        tmp_copy.insert(0, "Anywhere")
        self._window_to_hwnd["Anywhere"] = consts.ANYWHERE_HWND

        self._selection_box["values"] = tmp_copy
        # self._selected_text.set("Anywhere") # set back to anywhere as default
