import json
import os
from sys import platform
import WalabotAPI as walabot

class WalabotAPI:
    def __init__(self):
        walabot.Init()  # load the WalabotSDK to the Python wrapper
        walabot.SetSettingsFolder()  # set the path to the essetial database files
        walabot.ConnectAny()  # establishes communication with the Walabot
        walabot.SetProfile(walabot.PROF_SENSOR)  # set scan profile out of the possibilities
        walabot.SetDynamicImageFilter(walabot.FILTER_TYPE_MTI)  # specify filter to use
        walabot.Start()  # starts Walabot in preparation for scanning

    def get_targets(self):
        """
        This is just a wrapper for a built-in function in order
        to get the data into a format which is actually usable.
        """
        walabot.Trigger()
        raw = walabot.GetSensorTargets()
        targets = []
        for i, t in enumerate(raw):
            targets.append({
                'x': t.xPosCm,
                'y': t.yPosCm,
                'z': t.zPosCm
            })
        return targets

class Target:
    def __init__(self, number=10):
        self.x_vals = []
        self.y_vals = []
        self.z_vals = []
        self.x_avg = 0.0
        self.y_avg = 0.0
        self.z_avg = 0.0
        self.num_to_avg = number

    def update(self, new_x, new_y, new_z):
        self._add_vals(new_x, new_y, new_z)
        self._calculate_average()

    def _add_vals(self, x, y, z):
        self.x_vals.append(x)
        self.y_vals.append(y)
        self.z_vals.append(z)
        if len(self.x_vals) > self.num_to_avg:
            del(self.x_vals[0])
        if len(self.y_vals) > self.num_to_avg:
            del(self.y_vals[0])
        if len(self.z_vals) > self.num_to_avg:
            del(self.z_vals[0])

    def _calculate_average(self):
        for val in self.x_vals:
            self.x_avg += val
        for val in self.y_vals:
            self.y_avg += val
        for val in self.z_vals:
            self.z_avg += val
        self.x_avg = self.x_avg / self.num_to_avg
        self.y_avg = self.y_avg / self.num_to_avg
        self.z_avg = self.z_avg / self.num_to_avg

if __name__ == '__main__':
    device = WalabotAPI()
    seen_targets = []
    while True:
        targets = device.get_targets()
        while len(targets) > len(seen_targets):
            seen_targets.append(Target())
        x = 0
        while x < len(targets):
            seen_targets[x].update(targets[x]['x'], targets[x]['y'], targets[x]['z'])
            x+=1
        os.system('cls')
        x = 0
        while x < len(seen_targets):
            print(str(x+1))
            print("\tX\t%.2f" % round(seen_targets[x].x_avg,2)) # Positive = towards the right when looking in direction of radio transmission
            print("\tY\t%.2f" % round(seen_targets[x].y_avg,2)) # Positive = towards the top (opposite side of USB plugs)
            print("\tZ\t%.2f" % round(seen_targets[x].z_avg,2)) # Postive = farther away from the walabot in the direction of radio transmission
            x+=1
