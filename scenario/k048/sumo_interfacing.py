#!/usr/bin/env python3

import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# import libsumo
import traci
from enum import Enum, unique
from typing import Mapping, Sequence, Tuple, List

from .enum import SGR_K048, SGR_Base, DET_K048, DET_Base
from scenario.tls_control_basics.signalgroup import SignalGroup, SignalGroup3FieldBike, SignalGroup3FieldCar, \
    SignalPattern, SignalState

SUMO_CONTROLID2SGR = [
    None,  # 0
    SGR_K048.FZ21,  # 1
    SGR_K048.FZ21,
    SGR_K048.FZ21,
    SGR_K048.FZ31,
    SGR_K048.FZ31,  # 5
    SGR_K048.FZ31,
    SGR_K048.FZ31,
    SGR_K048.FZ12,
    SGR_K048.FZ12,
    SGR_K048.FZ11,  # 10
    SGR_K048.FZ11,
    SGR_K048.FZ11,
    SGR_K048.FZ33,
    SGR_K048.FZ33,
    SGR_K048.FZ32,  # 15 - GREEN/OFF signal
    SGR_K048.FZ41,
    SGR_K048.FZ42,
    SGR_K048.F201_202,  # 19 - start pedestrian
    SGR_K048.F301,
    SGR_K048.F101,  # 20
    SGR_K048.F401  # 21
]  # type: Sequence[SGR_K048]


class SUMOSignalGroup(SignalGroup):
    """
    Signal group with conversion from signal pattern to corresponding sumo chr
    """

    def __init__(self, id: SGR_Base) -> None:
        super().__init__(id)
        self.pattern2sumo = {}  # type: Mapping[SignalPattern, chr]
        self.pattern2sumo[SignalPattern.GREEN] = 'G'
        self.pattern2sumo[SignalPattern.RED] = 'r'
        self.pattern2sumo[SignalPattern.DARK] = 'o'

    def updateSUMOPattern(self, pattern: SignalPattern, c: chr) -> None:
        """ Update the pattern to sumo chr assignment """
        self.pattern2sumo[pattern] = c

    def getSUMOControlChar(self, t: float) -> chr:
        return self.pattern2sumo[self.stateAssignment[self.getSignalState(t)]]


class SUMOSignalGroup3FieldCar(SignalGroup3FieldCar, SUMOSignalGroup):
    """
    Signal group with yellow light with conversion from signal pattern to corresponding sumo chr
    """

    def __init__(self, id: SGR_Base) -> None:
        super().__init__(id)
        self.pattern2sumo[SignalPattern.YELLOW] = 'y'
        self.pattern2sumo[SignalPattern.REDYELLOW] = 'u'


class SUMOSignalGroup3FieldBike(SignalGroup3FieldBike, SUMOSignalGroup):
    """
    Signal group with yellow light with conversion from signal pattern to corresponding sumo chr
    """

    def __init__(self, id: SGR_Base) -> None:
        super().__init__(id)
        self.pattern2sumo[SignalPattern.YELLOW] = 'y'
        self.pattern2sumo[SignalPattern.REDYELLOW] = 'u'


class K048_SUMO_Signals:
    def __init__(self):
        self.signals = {}  # type: Mapping[SGR_Base, SUMOSignalGroup]
        for sgr in SGR_K048:
            i = sgr.value
            if i in range(1, 9) and not i == 5:
                self.signals[sgr] = SUMOSignalGroup3FieldCar(sgr)
            elif i in range(9, 13):
                self.signals[sgr] = SUMOSignalGroup3FieldBike(sgr)
            elif i in range(13, 25) or i == 5:
                self.signals[sgr] = SUMOSignalGroup(sgr)

        self.last_states = {}  # type: Mapping[SGR_Base, SignalState]
        for sgr in SGR_K048:
            self.last_states[sgr] = SignalState.OFF

        self.signals[SGR_K048.FZ32].updateStateAssignment(SignalState.STOP, SignalPattern.DARK)
        self.signals[SGR_K048.FZ32].updateSUMOPattern(SignalPattern.DARK, 'g')

    def getSignals(self) -> Mapping[SGR_Base, SUMOSignalGroup]:
        return self.signals

    def getLastStates(self) -> Mapping[SGR_Base, SignalState]:
        return self.last_states

    def setLastStates(self, states: Mapping[SGR_Base, SignalState]) -> None:
        self.last_states = states


def buildSUMOControlString(t: float, sumo_sig_grp: K048_SUMO_Signals) -> str:
    """ Builds a sumo control string from SUMO_CONTROLID2SGR and SUMO_SIG_GRP """
    signalstr = ""
    for sgr in SUMO_CONTROLID2SGR:
        if sgr != None:
            signalstr = signalstr + sumo_sig_grp.getSignals()[sgr].getSUMOControlChar(t)
        else:
            signalstr = signalstr + "g"
    return signalstr


@unique
class SUMO_DETECTOR_TYPE(Enum):
    INDUCTION_LOOP = 0
    AREA_DETECTOR = 1


SUMO_DET2ID_TYPE = {
    DET_K048.VD11: ("VD11", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.VD11a: ("VD11a", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.D21: ("D21", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.VD31: ("VD31", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.VD31a: ("VD31a", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.VD31b: ("VD31b", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.D32: ("D32_long", SUMO_DETECTOR_TYPE.AREA_DETECTOR),
    DET_K048.D41: ("D41", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.VD41: ("VD41", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.D42: ("D42", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.VD42: ("VD42", SUMO_DETECTOR_TYPE.INDUCTION_LOOP),
    DET_K048.T_R21: None,
    DET_K048.T_R41: None,
    DET_K048.T_F101: None,
    DET_K048.T_F102: None,
    DET_K048.T_F103: None,
    DET_K048.T_F104: None,
    DET_K048.T_F301: None,
    DET_K048.T_F302: None,
    DET_K048.T_F303: None,
    DET_K048.T_F304: None,
}  # type: # Mapping[DET_Base, tuple[str,SUMO_DETECTOR_TYPE]]


class SumoInterfaceFunctions:

    def __init__(self, use_gui: bool = False) -> None:
        if use_gui:
            self._lib = traci
        else:
            self._lib = traci
        self._INDUCTION_LOOP_EXIT_TIMES_CACHE = {}  # type: Mapping[str,Tuple[str,float]] # det_id : (veh_id, exitTime)
        self._AREA_DETECTOR_TIME_GAP_CACHE = {}  # type: Mapping[DET_Base,float]
        self._AREA_DETECTOR_VEH_ID_LIST_CACHE = {}  # type: Mapping[DET_Base,List[str]]

    # return netto time-gap - see ticket #1464 (reset state for each simulation run)    
    def _inductionloop_timegap(self, id: str) -> float:
        """returns the largest netto-time gap between sucessive vehicles"""
        vehicleData = self._lib.inductionloop.getVehicleData(id)
        if len(vehicleData) == 0:
            return self._lib.inductionloop.getTimeSinceDetection(id)
        gaps = []
        for veh_id, veh_length, entry_time, exit_time, vType in vehicleData:
            last_veh, last_exit = self._INDUCTION_LOOP_EXIT_TIMES_CACHE.get(id, (None, None))
            if last_veh != veh_id:
                gaps.append((last_exit, entry_time))
                if last_exit is not None and entry_time - last_exit <= 0:
                    print("negative time gap det=%s lastVeh=%s (exit=%s) veh_id=%s (entry=%s)" % (
                        id, last_veh, last_exit, veh_id, entry_time))
            self._INDUCTION_LOOP_EXIT_TIMES_CACHE[id] = veh_id, exit_time
        # if id == 'RD1': print vehicleData, gaps
        gaps = [entry - exit for exit, entry in gaps if exit is not None]
        if len(gaps) > 0:
            # assert(min(gaps) > 0)
            return max(gaps + [0])
        else:
            return self._lib.inductionloop.getTimeSinceDetection(id)

    def _getTimeGapFromAreaDetector(self, id: DET_Base, numVeh: int, t: float) -> float:
        if not id in self._AREA_DETECTOR_TIME_GAP_CACHE:
            self._AREA_DETECTOR_TIME_GAP_CACHE[id] = -1
        if numVeh > 0:
            self._AREA_DETECTOR_TIME_GAP_CACHE[id] = t
        return t - self._AREA_DETECTOR_TIME_GAP_CACHE[id]

    def _getNumberOfNewVehicles(self, id: DET_Base, veh_list: List[str]) -> int:
        count = 0
        if not id in self._AREA_DETECTOR_VEH_ID_LIST_CACHE:
            self._AREA_DETECTOR_VEH_ID_LIST_CACHE[id] = veh_list
        prev_step_veh_list = self._AREA_DETECTOR_VEH_ID_LIST_CACHE[id]
        for veh in veh_list:
            if not veh in prev_step_veh_list:
                count += 1
        self._AREA_DETECTOR_VEH_ID_LIST_CACHE[id] = veh_list
        return count

    def retrieveDetectorValues(self, t: float) -> Mapping[DET_K048, Tuple[int, float, bool, int]]:
        """ returns (number of vehicles on detector, time gap, button press, new vehicle count) for each detector """
        detvalues = {}
        for key in SUMO_DET2ID_TYPE:
            if SUMO_DET2ID_TYPE[key] != None:
                sumo_id, type = SUMO_DET2ID_TYPE[key]
                if type == SUMO_DETECTOR_TYPE.INDUCTION_LOOP:
                    # time gap from induction loop - does not take into account vehicles standing on the detector
                    tgap = self._lib.inductionloop.getTimeSinceDetection(sumo_id)
                    # time gap from lane area detectors - unreliable when vehicles pass without touching between timesteps
                    vehIds = self._lib.lanearea.getLastStepVehicleIDs("l" + sumo_id)
                    vehNum = len(vehIds)
                    # vehNum = self._lib.lanearea.getLastStepVehicleNumber("l"+sumo_id)
                    tgap2 = self._getTimeGapFromAreaDetector(key, vehNum, t)
                    # use minimum of both to determine correct gap
                    gap = min(tgap, tgap2)
                    detvalues[key] = (int(gap < 1), gap, False, self._getNumberOfNewVehicles(key, vehIds))
                elif type == SUMO_DETECTOR_TYPE.AREA_DETECTOR:
                    vehIds = self._lib.lanearea.getLastStepVehicleIDs(sumo_id)
                    vehNum = len(vehIds)
                    detvalues[key] = (vehNum, self._getTimeGapFromAreaDetector(key, vehNum, t), False,
                                      self._getNumberOfNewVehicles(key, vehIds))
            # else:
            # simulate pedestrian detection
        return detvalues

    def reset_caches(self) -> None:
        self._INDUCTION_LOOP_EXIT_TIMES_CACHE.clear()
        self._AREA_DETECTOR_TIME_GAP_CACHE.clear()
        self._AREA_DETECTOR_VEH_ID_LIST_CACHE.clear()

    def setRedYellowGreenState(self, id: str, state: str) -> None:
        self._lib.trafficlight.setRedYellowGreenState(id, state)
