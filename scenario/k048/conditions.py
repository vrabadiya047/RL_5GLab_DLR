#!/usr/bin/env python3

import scenario.k048.conditions_ext as ext
import scenario.k048.conditions_req as req
from scenario.k048.detector_processing import K048_SignalExtensions, K048_SignalRequests, K048_SignalButtons, K048_DetectorProcessing
from scenario.k048.enum import SGR_K048, DET_K048
from scenario.tls_control_basics.timer import Timer


class K048_Extensions:
    def __init__(self) -> None:
        self.maindirection = ext.Ext_MainDirection()
        self.fz21 = ext.Ext_FZ21()
        self.fz40 = ext.Ext_FZ40()

    def update(self, ext: K048_SignalExtensions) -> None:
        self.maindirection.update(ext.getValue(SGR_K048.FZ11), ext.getValue(SGR_K048.FZ31))
        self.fz21.update(ext.getValue(SGR_K048.FZ21))
        self.fz40.update(ext.getValue(SGR_K048.FZ41), ext.getValue(SGR_K048.FZ42))


class K048_Requests:
    def __init__(self) -> None:
        self.jam_d32 = req.TrafficJam_D32()
        self.fz21 = req.Req_FZ21()
        self.ph2_fz21 = req.Req_Ph2_FZ21()
        self.fz40 = req.Req_FZ40()
        self.fg300 = req.Req_FG300()
        self.ph2_f100 = req.Req_Ph2_F100()
        self.ph2_fz40 = req.Req_Ph2_FZ40()
        self.ph2_fg300 = req.Req_Ph2_FG300()
        self.f100 = req.Req_F100()
        self.maindirection = req.Req_MainDirection()
        self.dan = req.Req_DAN()

    def update(self, t: float, reqs: K048_SignalRequests, buttons: K048_SignalButtons,
               d32: int, vd11: float, vd11a: float, vd31: float, vd31a: float, vd31b: float, dan: bool) -> None:
        self.jam_d32.update(t, d32)
        self.fz21.update(reqs.getValue(SGR_K048.FZ21), reqs.getValue(SGR_K048.R41))
        self.ph2_fz21.update(reqs.getValue(SGR_K048.FZ21), buttons.getValue(SGR_K048.R41), self.jam_d32, t)
        self.fz40.update(reqs.getValue(SGR_K048.FZ41), reqs.getValue(SGR_K048.FZ42))
        self.fg300.update(buttons.getValue(SGR_K048.F301), buttons.getValue(SGR_K048.F302),
                          buttons.getValue(SGR_K048.F303), buttons.getValue(SGR_K048.F304),
                          buttons.getValue(SGR_K048.R41))
        self.ph2_f100.update(buttons.getValue(SGR_K048.F101), buttons.getValue(SGR_K048.F102),
                             buttons.getValue(SGR_K048.F103), buttons.getValue(SGR_K048.F104), self.jam_d32, t)
        self.ph2_fz40.update(reqs.getValue(SGR_K048.FZ41), reqs.getValue(SGR_K048.FZ42), buttons.getValue(SGR_K048.R41),
                             self.jam_d32, t)
        self.ph2_fg300.update(buttons.getValue(SGR_K048.F301), buttons.getValue(SGR_K048.F302),
                              buttons.getValue(SGR_K048.F303), buttons.getValue(SGR_K048.F304), self.jam_d32, t)
        self.f100.update(buttons.getValue(SGR_K048.F101), buttons.getValue(SGR_K048.F102),
                         buttons.getValue(SGR_K048.F103), buttons.getValue(SGR_K048.F104))
        self.maindirection.update(vd11, vd11a, vd31, vd31a, vd31b)
        self.dan.update(dan, t)


class K048_EmergencyRequests:
    def __init__(self) -> None:
        self.requestId = 0  # emergency request id, 0 is no request
        self.requestTimer = Timer()
        self.timeout = 300.0  # timeout for Emergency Request -> check original control

    def update(self, t: float):
        # check for timeout of running emergency request
        if self.requestId != 0:
            if self.requestTimer.getDurationSinceStart(t) > self.timeout:
                self.requestEmergencyPhase(t, 0)

    def requestEmergencyPhase(self, t: float, rId: int):
        """ Request an emergency phase, 0 is no request. Switching directly from one request to another is not allowed. """
        if rId == 0:
            if self.requestId != 0:
                self.requestId = rId
                self.requestTimer.stopTimer(t)
        else:
            if self.requestId == 0:
                self.requestId = rId
                self.requestTimer.startTimer(t)

    def getValue(self, rId):
        if rId == self.requestId:
            return True
        return False


class K048_Conditions:
    def __init__(self) -> None:
        self.ext = K048_Extensions()
        self.req = K048_Requests()
        self.emr = K048_EmergencyRequests()

    def update(self, t: float, processing: K048_DetectorProcessing, DAN: bool) -> None:
        self.ext.update(processing.getExt())
        self.req.update(t, processing.getReq(), processing.getButtons(),
                        processing.getDetValue(DET_K048.D32, 0),
                        processing.getDetValue(DET_K048.VD11, 1),
                        processing.getDetValue(DET_K048.VD11a, 1),
                        processing.getDetValue(DET_K048.VD31, 1),
                        processing.getDetValue(DET_K048.VD31a, 1),
                        processing.getDetValue(DET_K048.VD31b, 1),
                        DAN)
        self.emr.update(t)

    def getExt(self) -> K048_Extensions:
        return self.ext

    def getReq(self) -> K048_Requests:
        return self.req

    def getEmR(self) -> K048_EmergencyRequests:
        return self.emr
