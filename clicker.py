import pyautogui
import time
import win32gui

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
        # CLICK_INTERVAL_MS = 1000 / self._cps
        self._cur_window = consts.ANYWHERE_HWND


    def update_cps(self, click_speed=consts.DEFAULT_CPS):
        # this version of update (overloaded) is to update on the cps_change event
        # rounding now handled in gui, value out of that is already rounded
        # click_speed = round(float(click_speed), consts.ROUND_PRECISION)
        self._cps = click_speed


    def update(self):
        """Update function to be called once every loop of program"""
        self.do_clicking()


    def update_window(self, window=consts.ANYWHERE_HWND):
        """Change the window to be clicked inside of"""
        print(f"Clicker got window: {window} to be set to")
        self._cur_window = window
        print(f"self._cur_window is now {win32gui.GetWindowText(self._cur_window)}")


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
            pyautogui.click()

            self._click_counter += 1
            cur_time = time.perf_counter()
            if self._time_last:
                self._seconds_counter += cur_time - self._time_last
            self._time_last = cur_time
            # print(f"clicked at {CLICK_COUNTER} / {self._seconds_counter} Clicks per sec")
            self.adjust_speed()
            time.sleep(self._click_interval_seconds)
        else:
            self._time_last = 0  # on last call of this function, reset time_last value


    def toggle_clicking(self):
        print("clicking toggled to " + str(not self._active))
        self._active = not self._active

        self.change_in_active_state()


    def should_click(self):
        if self._active:
            click_anywhere = self._cur_window == consts.ANYWHERE_HWND
            foreground_is_selected = win32gui.GetForegroundWindow() == self._cur_window
            cursor_in_selected = point_in_rect(win32gui.GetCursorPos(), win32gui.GetClientRect(self._cur_window))

            # print(f"anywhere: {click_anywhere} | selected window in foreground: {foreground_is_selected} | cursor in window: {cursor_in_selected}")

            cursor_in_target = click_anywhere or (foreground_is_selected and cursor_in_selected)

            # print(f"{cursor_in_target} that the cursor is " +
            #     f"in the target window, it is {cursor_in_target} that we will click")
            if cursor_in_target:
                return True
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
    print(f"point: {point} | rect: {rect}")
    return (
        point[0] >= rect[0] and
        point[0] <= rect[2] and
        point[1] >= rect[1] and
        point[1] <= rect[3]
    )