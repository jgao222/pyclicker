import pyautogui
import time
import win32.win32gui as win32gui

# local imports
import consts


class Clicker:
    def __init__(self):
        # initialize stuff
        self._active = False
        self._click_counter = 0
        self._seconds_counter = 0
        self._time_last = time.perf_counter()

        self._click_count = 0

        self._cps = consts.DEFAULT_CPS
        self._click_interval_seconds = 1 / self._cps
        self._cur_window = consts.ANYWHERE_HWND

        # for clicking at set point
        self._click_at_point = False
        self._point_to_click = (None, None)

        self._click_button = "left"

    def update_cps(self, click_speed=consts.DEFAULT_CPS):
        self._cps = click_speed

    def update(self):
        """Update function to be called once every loop of program"""
        self.do_clicking()

    def update_window(self, window=consts.ANYWHERE_HWND):
        """Change the window to be clicked inside of"""
        consts.dprint(f"Clicker got window: {window}", 1)
        self._cur_window = window
        consts.dprint("Clicker window is now " +
                      f"{win32gui.GetWindowText(self._cur_window)}", 1)

    def update_click_point(self, target_point=(None, None)):
        """
        Update the click point
        @args
        - to_click: whether to click at a set point
        - target_point: a tuple (x, y) screen coordinates point to click at
        """
        self._point_to_click = target_point
        self._click_at_point = target_point[0] and target_point[1]
        consts.dprint("Updated point to click at to be: " +
                      f"{self._point_to_click}", 2)

    def update_click_btn(self, btn="left"):
        """
        Update the click type
        @args
        - type: 'left' or 'right'
        """
        self._click_button = btn

    def adjust_speed(self):
        if self._click_counter and self._seconds_counter:
            if (self._click_counter / self._seconds_counter) < self._cps:
                self._click_interval_seconds /= 2
            else:
                self._click_interval_seconds = 1 / self._cps

        if self._click_counter > 63:
            self._click_counter = 0
            self._seconds_counter = 0

    def do_clicking(self):
        if self.should_click():
            pyautogui.click(x=self._point_to_click[0],
                            y=self._point_to_click[1],
                            button=self._click_button)

            self._click_counter += 1
            cur_time = time.perf_counter()
            if self._time_last:
                self._seconds_counter += cur_time - self._time_last
            self._time_last = cur_time
            self.adjust_speed()
            time.sleep(self._click_interval_seconds)
        else:
            # on last call of this function, reset time_last value
            self._time_last = 0

    def toggle_clicking(self):
        consts.dprint("clicking toggled to " + str(not self._active) +
                      f" at {self._cps} for {self._click_button} button", 2)
        self._active = not self._active

        self.change_in_active_state()

    def should_click(self):
        if self._active:
            # ideally we just use one expression and short circuit, but this is
            # clearer, so we can leave it in for now
            click_anywhere = self._cur_window == consts.ANYWHERE_HWND
            foreground_is_selected = (win32gui.GetForegroundWindow() ==
                                      self._cur_window)
            cursor_in_selected = None
            if self._cur_window != consts.ANYWHERE_HWND:
                if self._click_at_point:
                    cursor_in_selected = point_in_rect(
                        (self._point_to_click[0], self._point_to_click[1]),
                        win32gui.GetWindowRect(self._cur_window)
                    )
                else:
                    cursor_in_selected = point_in_rect(
                        win32gui.GetCursorPos(),
                        win32gui.GetWindowRect(self._cur_window)
                    )
            else:
                cursor_in_selected = True

            cursor_in_target = click_anywhere or (
                foreground_is_selected and cursor_in_selected
            )
            self_focused = win32gui.GetWindowText(
                win32gui.GetForegroundWindow()) == consts.WINDOW_NAME

            # cursor_in_target = self._cur_window == consts.ANYWHERE_HWND or \
            #     ((win32gui.GetForegroundWindow() == self._cur_window) and
            #      (point_in_rect(win32gui.GetCursorPos(),
            #                     win32gui.GetClientRect(self._cur_window))))
            # TODO: print statement
            consts.dprint(f"foreground: {foreground_is_selected} | " +
                          f"cursor_in: {cursor_in_selected}",
                          3)

            return cursor_in_target and not self_focused
        return False

    # these two methods send events outward
    def add_callback_to_active_change(self, callback):
        self._active_change_callback = callback

    def change_in_active_state(self):
        if self._active_change_callback:
            self._active_change_callback(self._active)


# helper methods
def point_in_rect(point, rect):
    """
    Checks if a point is inside a rectangle
    @args
    - point: a point as tuple (x, y)
    - rect: a rectange as tuple (left, top, right, bottom)
    """
    consts.dprint(f"p: {point}, r: {rect}")
    return (
        point[0] >= rect[0]
        and point[0] <= rect[2]
        and point[1] >= rect[1]
        and point[1] <= rect[3]
    )
