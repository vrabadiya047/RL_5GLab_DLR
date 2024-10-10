#!/usr/bin/env python3

# from __future__ import annotations
from typing import AbstractSet, Sequence, Mapping, Tuple
from .enum_base import SGR_Base, SignalState
from .signalgroup import SignalGroup
from .timer import Timer


class Phase:
    """
    Class for managing signal groupes and their state
    """

    def __init__(self) -> None:
        self.statemap = {}  # type: Mapping[SGR_Base, SignalState]
        self.timer = Timer()

    def getStates(self) -> Mapping[SGR_Base, SignalState]:
        return self.statemap

    def getControlledSignalGroupIDs(self) -> AbstractSet[SGR_Base]:
        return self.statemap.keys()

    def setPhaseState(self, state: SignalState, sgr_list: Sequence[SGR_Base]) -> None:
        """ Assign all signal groups in sgr_list the SignalState state """
        for sgr in sgr_list:
            self.statemap[sgr] = state

    def run(self, t: float, sgr_list: Sequence[SignalGroup]) -> None:
        """ Apply the states in the phase to signal groups in sgr_list """
        if not self.timer.isRunning():
            self.timer.startTimer(t)
        for k in self.statemap:
            sgr_list[k].requestSignalState(t, self.statemap[k])

    def end(self, t: float) -> None:
        self.timer.stopTimer(t)

    def getDuration(self, t: float, decimals: int = 0) -> float:
        if not self.timer.isRunning():
            return -1
        return round(self.timer.getDurationSinceStart(t), decimals)

    def isActive(self) -> bool:
        return self.timer.isRunning()

    def initFromString(self, full_sgr_list: Sequence[SGR_Base], statestr: str) -> None:
        """ Initilize phase with list of signal group ids and corresponding chr as representative for signal state """
        for sgr in full_sgr_list:
            state = statestr[0].lower()
            if state == "g":
                self.statemap[sgr] = SignalState.GO
            elif state == "r":
                self.statemap[sgr] = SignalState.STOP
            elif state == "u":
                self.statemap[sgr] = SignalState.GO
            elif state == "o":
                self.statemap[sgr] = SignalState.OFF
            elif state == "y":
                self.statemap[sgr] = SignalState.STOP
            statestr = statestr[1:]

    @classmethod
    def getObjectFromString(cls, full_sgr_list: Sequence[SGR_Base], statestr: str):
        """ Get object that is initialized with 'initFromString' method """
        obj = cls()
        obj.initFromString(full_sgr_list, statestr)
        return obj


class PhaseTransition:
    """
    Class for managing a static sequence of phases with certain durations
    """

    def __init__(self) -> None:
        self.durationAndSubphase = []  # type: Sequence[tuple[float,Phase]]
        self.timer = Timer()

    def init(self, phasedur: Sequence[Tuple[float, Phase]]) -> None:
        """ Inilitialize phase transition, order in sequence is important! """
        self.durationAndSubphase = phasedur

    def run(self, t: float, sgr_list: Sequence[SignalGroup]) -> bool:
        """ Execute phase transition, returns true while active. Once inactive, immediately activate next phase in the same time step """
        if not self.timer.isRunning():
            self.timer.startTimer(t)
        d = 0.0
        for p in self.durationAndSubphase:
            d += p[0]
            if t < self.timer.startTime + d:
                p[1].run(t, sgr_list)
                return True
        self.timer.stopTimer(t)
        return False

    def getDuration(self, t: float, decimals: int = 0) -> float:
        """ Returns duration if phase is active, -1 otherwise """
        if not self.timer.isRunning():
            return -1
        return round(self.timer.getDurationSinceStart(t), decimals)

    def isActive(self) -> bool:
        """ Returns whether phase transition is acitve """
        return self.timer.isRunning()

    @classmethod
    def getObject(cls, phasedur: Sequence[Tuple[float, Phase]]):
        obj = cls()
        obj.init(phasedur)
        return obj
