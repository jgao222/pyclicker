import pyautogui
import time

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


    def update_cps(self, click_speed=consts.DEFAULT_CPS):
        # rounding now handled in gui, value out of that is already rounded
        # click_speed = round(float(click_speed), consts.ROUND_PRECISION)
        self._cps = click_speed


    def update(self):
        """Update function to be called once every loop of program"""
        self.do_clicking()


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
        if self._active:
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


    def add_callback_to_active_change(self, callback):
        self._active_change_callback = callback


    def change_in_active_state(self):
        self._active_change_callback(self._active)
