from sys import platform
import os
import time

## Import our stuff
from api.bokeh_api import BokehAPI
from api.walabot_api import WalabotAPI

class SleepTracker:
    def __init__(self):
        self.walabot = WalabotAPI()

    def _get_date_time(self):
        """
        Returns a timestamp string.

        Output (example):
        2017-03-29 19:37:01
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def track(self):
        while True:
            targets = self.walabot.get_targets()
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            x = 0
            while x < len(targets):
                print(str(x+1))
                print(round(targets[x]['x'],2)) # Positive = towards the right when looking in direction of radio transmission
                print(round(targets[x]['y'],2)) # Positive = towards the top (opposite side of USB plugs)
                print(round(targets[x]['z'],2))# Postive = farther away from the walabot in the direction of radio transmission
                x+=1


class Database:
    def __init__(self):
        pass

if __name__ == '__main__':
    print("Sleep tracker initializing...")
    tracker = SleepTracker()
    tracker.track()
