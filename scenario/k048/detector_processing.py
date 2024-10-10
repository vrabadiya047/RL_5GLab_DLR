#!/usr/bin/env python3

from typing import Mapping, Tuple, Sequence
from .enum import SGR_K048, DET_K048
from scenario.tls_control_basics.conditions import SignalExtension, SignalButton, SignalRequest
from scenario.tls_control_basics.signalgroup import SignalGroup

class K048_SignalExtensions:
    def __init__(self) -> None:
        self._conditions = {} # type: Mapping[SGR_K048, SignalExtension]
        for sgr in SGR_K048:
            self._conditions[sgr] = SignalExtension()
    def setValue(self, timegap : float, sgr : SignalGroup):
        self._conditions[sgr.getID()].update(timegap)
    def getValue(self, sgr : SGR_K048):
        return self._conditions[sgr]
    def reset(self):
        for sgr in self._conditions:
            self._conditions[sgr].reset()

class K048_SignalRequests:
    def __init__(self) -> None:
        self._conditions = {} # type: Mapping[SGR_K048, SignalRequest]
        for sgr in SGR_K048:
            self._conditions[sgr] = SignalRequest()    
    def setValue(self, numVeh : int, signalgroup : SignalGroup, t : float) -> None:
        self._conditions[signalgroup.getID()].update(numVeh, signalgroup, t)
    def getValue(self, sgr : SGR_K048):
        return self._conditions[sgr]
    def reset(self):
        for sgr in self._conditions:
            self._conditions[sgr].reset()
        

class K048_SignalButtons:
    def __init__(self) -> None:
        self._conditions = {} # type: Mapping[SGR_K048, SignalButton]
        for sgr in SGR_K048:
            self._conditions[sgr] = SignalButton()
    def setValue(self, b : bool, signalgroup : SignalGroup):
        self._conditions[signalgroup.getID()].update(b, signalgroup)
    def getValue(self, sgr : SGR_K048):
        return self._conditions[sgr]
    
class K048_DetectorProcessing:
    def __init__(self) -> None:
        self._det_values = {} # type: Mapping[DET_K048,Tuple[int, float, bool, int]]
        self._ext = K048_SignalExtensions()
        self._req = K048_SignalRequests()
        self._buttons = K048_SignalButtons()
        self._mapReq = {
            DET_K048.D21 : [SGR_K048.FZ21],
            DET_K048.D41 : [SGR_K048.FZ41],
            DET_K048.D42 : [SGR_K048.FZ42],
            DET_K048.VD41 : [SGR_K048.FZ41],
            DET_K048.VD42 : [SGR_K048.FZ42],
            DET_K048.VD11 : [SGR_K048.FZ11],
            DET_K048.VD11a : [SGR_K048.FZ11],
            DET_K048.VD31 : [SGR_K048.FZ31],
            DET_K048.VD31a : [SGR_K048.FZ31],
            DET_K048.VD31b : [SGR_K048.FZ31],
            } # type: Mapping[DET_K048, Sequence[SGR_K048]]
        self._mapExt = {
            DET_K048.VD11 : [SGR_K048.FZ11],
            DET_K048.VD11a : [SGR_K048.FZ11],
            DET_K048.D21 : [SGR_K048.FZ21],
            DET_K048.VD31 : [SGR_K048.FZ31],
            DET_K048.VD31a : [SGR_K048.FZ31],
            DET_K048.VD31b : [SGR_K048.FZ31],
            DET_K048.VD41 : [SGR_K048.FZ41],
            DET_K048.VD42 : [SGR_K048.FZ42],
            } # type: Mapping[DET_K048, Sequence[SGR_K048]]
        self._mapButtons = {
            DET_K048.T_R21 : [SGR_K048.R21],
            DET_K048.T_R41 : [SGR_K048.R41],
            DET_K048.T_F101 : [SGR_K048.F101],
            DET_K048.T_F102 : [SGR_K048.F102],
            DET_K048.T_F103 : [SGR_K048.F103],
            DET_K048.T_F104 : [SGR_K048.F104],
            DET_K048.T_F301 : [SGR_K048.F301],
            DET_K048.T_F302 : [SGR_K048.F302],
            DET_K048.T_F303 : [SGR_K048.F303],
            DET_K048.T_F304 : [SGR_K048.F304],
            } # type: Mapping[DET_K048, Sequence[SGR_K048]]
    
    def process(self, signalgroups : Mapping[SGR_K048, SignalGroup], t : float) -> None:
        for det in self._det_values:
            if det in self._mapButtons:
                for sgr in self._mapButtons[det]:
                    self._buttons.setValue(self._det_values[det][2], signalgroups[sgr])
            if det in self._mapExt:
                for sgr in self._mapExt[det]:
                    self._ext.setValue(self._det_values[det][1], signalgroups[sgr])
            if det in self._mapReq:
                for sgr in self._mapReq[det]:
                    self._req.setValue(self._det_values[det][0], signalgroups[sgr], t)
    
    def getExt(self) -> K048_SignalExtensions:
        return self._ext
    
    def getReq(self) -> K048_SignalRequests:
        return self._req
    
    def getButtons(self) -> K048_SignalButtons:
        return self._buttons
    
    def reset(self) -> None:
        self._ext.reset()
        self._req.reset()
        
    def updateDetValues(self, det_values : Mapping[DET_K048,Tuple[int, float, bool, int]]):
        self._det_values = det_values
        
    def getDetValue(self, det : DET_K048, idx : int):
        """idx = 0 : number of vehicles on detector
        idx = 1 : time gap
        idx = 2 : request by button"""
        return self._det_values[det][idx]
    
    def getDetValues(self):
        return self._det_values