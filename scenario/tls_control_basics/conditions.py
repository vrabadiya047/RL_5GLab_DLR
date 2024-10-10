#!/usr/bin/env python3

from .signalgroup import SignalGroup
from .timer import Timer

class Condition:
    def __init__(self) -> None:
        self.value = False # type: bool
        
    def setValue(self, value : bool) -> None:
        self.value = value
            
    def getValue(self) -> bool:
        return self.value
    
    def update(self) -> None:
        pass

class SignalButton(Condition):
    """ Request based on buttons, e.g. pedestrian or bicycle, resets when signal shows GO """
    def update(self, button : bool, sgr : SignalGroup) -> None:
        if(button):
            self.setValue(True)
        if sgr.signalstateGO():
            self.setValue(False)

class SignalRequest(Condition):
    """ Request is issued when number of vehicles is above a certain threshold, resets when corresponding signal shows GO """
    def __init__(self) -> None:
        super().__init__()
        self.threshold = 0
        self.values = []
        self.stateGo = False
        
    def setThreshold(self, i : int) -> None:
        self.threshold = i
        
    def update(self, numVeh : int, sgr : SignalGroup, t : float) -> None:
        if sgr.signalstateGO(t):
            self.reset()
            return
        self.values.append(numVeh)
        self.stateGo = sgr.signalstateGO(t)
        
    def getValue(self) -> bool:
        if not self.stateGo:
            for value in self.values:
                if value > self.threshold:
                    return True
        return False
    
    def reset(self):
        self.stateGo = False
        self.values.clear()
        
class SignalExtension(Condition):
    """ Extension is issued when time gap between two vehicles at corresponding detector is below certain threshold """
    def __init__(self) -> None:
        super().__init__()
        self.timeGap = 3.0
        self.values = []
    
    def setTimeGap(self, t : float) -> None:
        self.timeGap = t
        
    def update(self, timegap : float) -> None:
        self.values.append(timegap)

    def getValue(self) -> bool:
        for value in self.values:
            if value < self.timeGap:
                return True
        return False
    
    def reset(self) -> None:
        self.values.clear()