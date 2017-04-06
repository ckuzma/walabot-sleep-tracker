from sys import platform
from os import system

import random # <-- Only used for dev architecture purposes
import time # <-- Only used for dev architecture purposes
import WalabotAPI

class SleepTracker:
    def __init__(self):
        self.walabot = WalabotAPI
        self.walabot.Init()
        self.walabot.SetSettingsFolder()

    def _detect_murphy(self):
        """
        This function is designed to figure out if the
        folding murphy bed is in the upright/stored
        configuration or horizontal/out.

        Output:
        True: bed is out
        False: bed is folded up
        """
        return True

    def _detect_sleep_state(self):
        """
        Reads in ~1 second worth of target tracking
        data and puts it through a filter to determine
        the sleep state of the target based on the
        amount of movement.

        Output:
        []: Zero people detected
        [0]: One person detected, not asleep
        [1]: One person detected, light sleep
        [2]: One person detected, deep sleep
        """
        # --- Begin debug dummy code ---
        if random.randint(0,1) is 0:
            return []
        else:
            time.sleep(1)
            sleep_state = random.randint(0,2)
            return [sleep_state]
        # --- End debug dummy code ---

    def _get_date_time(self):
        """
        Returns a timestamp string.

        Output (example):
        2017-03-29 19:37:01
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def track(self):
        """
        The only public function of this class, which
        runs the show.
        """
        while True:
            if self._detect_murphy():
                print(self._get_date_time())
                print('Murphy bed: Down')
                print('Sleep state: ' + str(self._detect_sleep_state()) + '\n')
            else:
                print('Murphy bed: Up')

class Database:
    def __init__(self):
        pass
        
# if __name__ == '__main__':
#     print("Sleep tracker initializing...")
#     tracker = SleepTracker()
#     tracker.track()
