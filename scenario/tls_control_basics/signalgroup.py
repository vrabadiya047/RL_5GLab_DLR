#!/usr/bin/env python3

from typing import Mapping, Sequence
from .enum_base import SGR_Base, SignalState, SignalPattern
from .timer import Timer
    
class SignalGroup:
    def __init__(self, id : SGR_Base) -> None:
        self.id = id
        self.stateAssignment = {} # type: Mapping[SignalState, SignalPattern]
        self.stateAssignment[SignalState.GO] = SignalPattern.GREEN
        self.stateAssignment[SignalState.STOP] = SignalPattern.RED
        self.stateAssignment[SignalState.OFF] = SignalPattern.DARK
        self.state = SignalState.OFF
        self.lastState = self.state
        self.timer = {} # type: Mapping[SignalState, Timer]
        self.minDurations = {} # type: Mapping[SignalState, float]
        self.preparationPhase = {} # type: Mapping[SignalState, Sequence[SignalState]]
        for state in SignalState:
            self.timer[state] = Timer()
            self.preparationPhase[state] = []
            self.minDurations[state] = 0.0
        self.minDurations[SignalState.GO] = 5.0
        self.minDurations[SignalState.STOP] = 1.0
        
    def getID(self) -> SGR_Base:
        return self.id
        
    def setStateMinDuration(self, state : SignalState, dur : float) -> None:
        self.minDurations[state] = dur
        
    def isStateMinDurationReached(self, t : float) -> bool:
        minDur = self.minDurations[self.state]
        if self.lastState != SignalState.OFF:
            for state in self.preparationPhase[self.state]:
                minDur += self.minDurations[state]
        return self.timer[self.state].getDurationSinceStart(t) >= minDur
    
    def requestSignalState(self, t : float, state : SignalState) -> None:
        """ Requestable states: GO, STOP, OFF """
        if not state in [SignalState.GO, SignalState.STOP, SignalState.OFF]:
            raise RuntimeError("A different phase SignalState than STOP or GO was requested.")
        if state != self.state:
            if self.state != SignalState.OFF and not self.isStateMinDurationReached(t):
                #     print(self.state, self.timer[self.state].getDurationSinceStart(t), self.minDurations[self.state], self.timer[self.state].getDurationSinceStart(t) < self.minDurations[self.state])
                raise RuntimeError("Mininum duration (%.1fs) for signal state %s at signal %s was not respected (%.1fs) (time=%.1f)." % (
                    self.minDurations[self.state],self.state, self.id, self.timer[self.state].getDurationSinceStart(t),t))
            self.timer[self.state].stopTimer(t)
            self.lastState = self.state
            self.state = state
            self.timer[self.state].startTimer(t)        
    
    def getSignalState(self, t : float) -> SignalState:
        if not self.lastState == SignalState.OFF:
            requestStartTime = self.timer[self.state].startTime
            for state in self.preparationPhase[self.state]:
                requestStartTime += self.minDurations[state]
                if t < requestStartTime:
                    return state
        return self.state
    
    def signalstateGO(self, t : float) -> bool:
        return self.getSignalState(t) == SignalState.GO
    
    def getSignalPattern(self, t : float) -> SignalPattern:
        return self.stateAssignment[self.getSignalState(t)]
    
    def updateStateAssignment(self, state : SignalState, pattern : SignalPattern) -> None:
        self.stateAssignment[state] = pattern
        
        
class SignalGroup3Field(SignalGroup):
    def __init__(self, id : SGR_Base) -> None:
        super().__init__(id)
        self.stateAssignment[SignalState.T_GO_STOP] = SignalPattern.YELLOW
        self.stateAssignment[SignalState.T_STOP_GO] = SignalPattern.REDYELLOW
        self.preparationPhase[SignalState.GO] = [SignalState.T_STOP_GO]
        self.preparationPhase[SignalState.STOP] = [SignalState.T_GO_STOP]
        
class SignalGroup3FieldCar(SignalGroup3Field):
    def __init__(self, id : SGR_Base) -> None:
        super().__init__(id)
        self.minDurations[SignalState.T_GO_STOP] = 3.0
        self.minDurations[SignalState.T_STOP_GO] = 1.0
        
class SignalGroup3FieldBike(SignalGroup3Field):
    def __init__(self, id : SGR_Base) -> None:
        super().__init__(id)
        self.minDurations[SignalState.T_GO_STOP] = 2.0
        self.minDurations[SignalState.T_STOP_GO] = 1.0