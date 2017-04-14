import json
from os import system
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

if __name__ == '__main__':
    device = WalabotAPI()
    while True:
        targets = device.get_targets()
        print(json.dumps(targets, indent=2))
        print('----')
