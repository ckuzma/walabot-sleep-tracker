import json
import os
from sys import platform

from imp import load_source
walabot = None
if os.name == 'nt': # Windows
    walabot = load_source('WalabotAPI', 'C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI.py')
else: # Unix
    walabot = load_source('WalabotAPI', '/usr/share/walabot/python/WalabotAPI.py')

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

if __name__ == '__main__':
    device = WalabotAPI()
    while True:
        targets = device.get_targets()
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
