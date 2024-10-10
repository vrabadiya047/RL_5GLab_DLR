#!/usr/bin/env python3

from scenario.tls_control_basics.conditions import Condition, SignalButton, SignalRequest
from scenario.tls_control_basics.timer import Timer

class TrafficJam_D32(Condition):
    def __init__(self) -> None:
        super().__init__()
        self.jamtimer = Timer()
    
    def update(self, t : float, d32 : int, decimals : int = 0):
        if d32 > 0:
            if not self.jamtimer.isRunning():
               self.jamtimer.startTimer(t)
            if self.getDuration(t, decimals) >= 10:
                self.setValue(True)
        else:
            self.jamtimer.stopTimer(t)
            self.setValue(False)
    
    def getDuration(self, t : float, decimals : int = 0) -> float:
        return round(self.jamtimer.getDurationSinceStart(t), decimals)

class Req_FZ21(Condition):
    def update(self, req_fz21 : SignalRequest, req_r41 : SignalButton) -> None:
        self.setValue(req_fz21.getValue() or req_r41.getValue())
        
class Req_Ph2_FZ21(Condition):
    def update(self, req_fz21 : SignalRequest, req_r41 : SignalButton, tjam_d32 : TrafficJam_D32, t : float, decimals : int = 0) -> None:
        self.setValue((req_fz21.getValue() or req_r41.getValue()) and tjam_d32.getDuration(t, decimals) > 0)
            
class Req_DAN(Condition):
    def __init__(self) -> None:
        super().__init__()
        self.setValue(False)
        self.timer = Timer()
    def update(self, DAN : bool, t : float) -> None:
        if self.getValue() and not DAN:
            self.timer.stopTimer(t)
        elif not self.getValue() and DAN:
            self.timer.startTimer(t)
        self.setValue(DAN)
    def getDuration(self, t : float) -> float:
        if self.timer.isRunning():
            return self.timer.getDurationSinceStart(t)
        else:
            return -1
    
class Req_FZ40(Condition):
    def update(self, req_fz41 : SignalRequest, req_fz42 : SignalRequest) -> None:
        self.setValue(req_fz41.getValue() or req_fz42.getValue())
        
class Req_FG300(Condition):
    def update(self, b_f301 : SignalButton, b_f302 : SignalButton, b_f303 : SignalButton, b_f304 : SignalButton, b_r41 : SignalButton) -> None:
        self.setValue(b_f301.getValue() or b_f302.getValue() or b_f303.getValue() or b_f304.getValue() or b_r41.getValue())
        
class Req_Ph2_F100(Condition):
    def update(self, b_f101 : SignalButton, b_f102 : SignalButton, b_f103 : SignalButton, b_f104 : SignalButton, tjam_d32 : TrafficJam_D32, t : float, decimals : int = 0) -> None:
        self.setValue((b_f101.getValue() or b_f102.getValue() or b_f103.getValue() or b_f104.getValue()) and tjam_d32.getDuration(t, decimals) > 0)
        
class Req_Ph2_FZ40(Condition):
    def update(self, req_fz41 : SignalRequest, req_fz42 : SignalRequest, b_r41 : SignalButton, tjam_d32 : TrafficJam_D32, t : float, decimals : int = 0) -> None:
        self.setValue((req_fz41.getValue() or req_fz42.getValue() or b_r41.getValue()) and tjam_d32.getDuration(t, decimals) > 0)
        
class Req_Ph2_FG300(Condition):
    def update(self, b_f301 : SignalButton, b_f302 : SignalButton, b_f303 : SignalButton, b_f304 : SignalButton, tjam_d32 : TrafficJam_D32, t : float, decimals : int = 0) -> None:
        self.setValue((b_f301.getValue() or b_f302.getValue() or b_f303.getValue() or b_f304.getValue()) and tjam_d32.getDuration(t, decimals) > 0)
        
class Req_F100(Condition):
    def update(self, b_f101 : SignalButton, b_f102 : SignalButton, b_f103 : SignalButton, b_f104 : SignalButton) -> None:
        self.setValue(b_f101.getValue() or b_f102.getValue() or b_f103.getValue() or b_f104.getValue())
        
class Req_MainDirection(Condition):
    def update(self, vd11 : float, vd11a : float, vd31 : float, vd31a : float, vd31b : float) -> None:
        self.setValue(vd11 < 1 or vd11a < 1 or vd31 < 1 or vd31a < 1 or vd31b < 1)