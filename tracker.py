import json
import math
import os
import sys
import time

## Import our stuff
from api.walabot_api import WalabotAPI

# Variables
CSV_FILE_LOCATION = None # This is set at runtime
SAMPLE_DELAY = 1 # Seconds
DEEP_THRESHOLD = 2.0 # A non-moving target tends to not be picked up after a while, so really low here works great
LIGHT_THRESHOLD = 5.0 # Calibrated to my situation

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

    def _print_targets(self, targets):
        """
        Debug function to print out all of the target coordinates.
        """
        x = 0
        while x < len(targets):
            print('Target ' + str(x+1))
            print(json.dumps(targets[x], indent=2))
            print('')
            x+=1

    def _pythagorean(self, target_1, target_2):
        """
        Calculates the distance that a target has moved.
        """
        x_square = abs(target_1['x'] - target_2['x'])**2
        y_square = abs(target_1['y'] - target_2['y'])**2
        z_square = abs(target_1['z'] - target_2['z'])**2
        return math.sqrt(x_square + y_square + z_square)

    def _sleep_state(self, distance):
        """
        Takes in a distance reading and returns an integer corresponding to
        the current state of a user's sleep:
        2 = deep sleep
        1 = light sleep
        0 = awake
        """
        if distance < DEEP_THRESHOLD:
            return 2
        if distance < LIGHT_THRESHOLD:
            return 1
        else:
            return 0

    def track(self):
        # Open the CSV file
        file_io = open(CSV_FILE_LOCATION, 'a')

        x_points = []
        y_points = []
        time_point = int(time.time())
        prev_targets = []
        while True:
            ## Get targets
            targets = self.walabot.get_targets()

            ## Clear the screen
            if os.name == 'nt':
                os.system('cls') # Windows
            else:
                os.system('clear') # Unix

            ## Print number of points seen
            print('# of saved data points: ' + str(len(x_points)))

            ## Print the targets
            self._print_targets(targets)

            ## Figure out the distances
            distances = []
            x = 0
            while x < len(targets):
                if x < len(prev_targets):
                    distances.append(self._pythagorean(prev_targets[x], targets[x]))
                else:
                    distances.append(0.0)
                x+=1

            ## If 1 seconds have passes, save to file
            if int(time.time()) - time_point > SAMPLE_DELAY:
                x_points.append(len(x_points))
                try:
                    y_points.append(distances[0])
                except:
                    y_points.append(0)
                time_point = int(time.time())
                try:
                    csv_line = self._get_date_time() + ',' + str(distances[0]) + ',' + str(self._sleep_state(distances[0])) + '\n'
                except:
                    csv_line = self._get_date_time() + ',' + str(0) + ',' + str(self._sleep_state(0)) + '\n'
                file_io.write(csv_line)

            ## Assign previous targets their current values
            ## to compare with the next reading
            prev_targets = targets

if __name__ == '__main__':
    ## Look to make sure we have parameters needed to run
    if len(sys.argv) != 2:
        print('\n\tUSAGE:\n\tpython ' + sys.argv[0] + ' <OUTPUT_CSV_LOCATION>\n\n')
        exit()

    ## Read in CSV output location
    CSV_FILE_LOCATION = sys.argv[1]
    print("Sleep tracker initializing...")
    tracker = SleepTracker()
    tracker.track()
