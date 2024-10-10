#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)+"\\..\\..\\"))
from scenario.k048.detector_processing import K048_DetectorProcessing
from scenario.k048.constants import K048_PhasesAndTransitions
from scenario.k048.conditions import K048_Conditions
from typing import Mapping, Tuple
from scenario.tls_control_basics.phase import Phase, PhaseTransition
from scenario.tls_control_basics.sl_logic import SLLogic
import scenario.k048.sumo_interfacing as si
class Controller:
    def __init__(self, use_gui: bool = False) -> None:
        ppt = K048_PhasesAndTransitions()
        self.phases = {
            1: ppt.phase_1,
            2: ppt.phase_2,
            3: ppt.phase_3,
            4: ppt.phase_4,
            5: ppt.phase_5,
            6: ppt.phase_6,
            # 7 : ppt.phase_7,
            # 8 : ppt.phase_8,
            7: ppt.phase_fw1,
            8: ppt.phase_fw2,
            9: ppt.aus_um
        }  # type: Mapping[int, Phase]

        self.transitions = {
            (1, 2): ppt.trans_1_2,
            (1, 3): ppt.trans_1_3,
            (1, 5): ppt.trans_1_5,
            (2, 3): ppt.trans_2_3,
            (2, 5): ppt.trans_2_5,
            (3, 4): ppt.trans_3_4,
            (4, 5): ppt.trans_4_5,
            (4, 1): ppt.trans_4_1,
            (5, 6): ppt.trans_5_6,
            (6, 1): ppt.trans_6_1,
            (1, 7): ppt.trans_1_fw1,
            (4, 7): ppt.trans_4_fw1,
            (6, 7): ppt.trans_6_fw1,
            (1, 8): ppt.trans_1_fw2,
            (4, 8): ppt.trans_4_fw2,
            (6, 8): ppt.trans_6_fw2,
            (7, 1): ppt.trans_fw1_1,
            (8, 1): ppt.trans_fw2_1
        }  # type: Mapping[Tuple[int, int], PhaseTransition]

        self.currentPhaseID = 1
        self.nextPhaseID = -1

        self.conditions = K048_Conditions()
        self.detectorProcessing = K048_DetectorProcessing()
        self.sllogic = SLLogic()
        self.sumo_sig_grp = si.K048_SUMO_Signals()
        self._sif = si.SumoInterfaceFunctions(use_gui)

    def newStringAvailable(self, t: float) -> bool:
        sgr2state = {}
        for sgr in self.sumo_sig_grp.getSignals():
            sgr2state[sgr] = self.sumo_sig_grp.getSignals()[sgr].getSignalState(t)
        if sgr2state != self.sumo_sig_grp.getLastStates():
            self.sumo_sig_grp.setLastStates(sgr2state)
            return True
        return False
    
    def getDetValues(self):
        return self.detectorProcessing.getDetValues()
    
    def preparationLogic(self, t : float) -> None:
        self.detectorProcessing.reset()
        self.detectorProcessing.updateDetValues(self._sif.retrieveDetectorValues(t))
        self.detectorProcessing.process(self.sumo_sig_grp.getSignals(), t)
        DAN = True
        for sig in self.sumo_sig_grp.getSignals():
            if not self.sumo_sig_grp.getSignals()[sig].isStateMinDurationReached(t):
                DAN = False
                break
        self.getConditions().update(t, self.detectorProcessing, DAN)

    def getConditions(self) -> K048_Conditions:
        return self.conditions

    def getSUMOCtrlString(self, t: float) -> str:
        return si.buildSUMOControlString(t, self.sumo_sig_grp)

    def setEmergencyRequest(self, t: float, rId: int) -> None:
        self.getConditions().getEmR().requestEmergencyPhase(t, rId)

    def getCurrentPhaseID(self) -> int:
        return self.currentPhaseID

    def setCurrentPhaseID(self, id: int):
        self.currentPhaseID = id

    def getNextPhaseID(self) -> int:
        return self.nextPhaseID

    def setNextPhaseID(self, i: int) -> None:
        self.nextPhaseID = i

    def getCurrentPhase(self) -> Phase:
        return self.phases[self.getCurrentPhaseID()]
    
    def currentPhaseIsActive(self) -> bool:
        return self.getCurrentPhase().isActive()

    def getCurrentPhaseDuration(self, t: float):
        return self.getCurrentPhase().getDuration(t)

    def getCurrentPhaseTransitionDuration(self, t: float):
        return self.transitions[(self.getCurrentPhaseID(), self.getNextPhaseID())].getDuration(t)
    
    def somePhaseIsActive(self) -> bool:
        return self.getNextPhaseID() == -1
    
    def somePhaseTransitionIsActive(self) -> bool:
        return not self.somePhaseIsActive()

    def getDANDuration(self, t: float) -> float:
        return self.getConditions().getReq().dan.getDuration(t)

    def runCurrentPhase(self, t: float) -> None:
        self.getCurrentPhase().run(t, self.sumo_sig_grp.getSignals())

    def runTransition(self, t: float) -> bool:
        return self.transitions[(self.getCurrentPhaseID(), self.getNextPhaseID())].run(t, self.sumo_sig_grp.getSignals())
    
    def determineNextPhase(self, t : float) -> None:
        """ once a request is issued, no other request is considered anymore and a timer is started to measure min and max extension times since the start of the request
        """
        # min durations for signals are reached
        if self.getDANDuration(t) >= 0:
            # from phase 1
            if self.getCurrentPhaseID() == 1:
                self.sllogic.setPhase(1, t)
                if   self.sllogic.isRequested(1, self.getConditions().getEmR().getValue(1), t):
                    if self.sllogic.evaluateExtension(False, t, 5, 6554):
                        self.setNextPhaseID(7)
                elif self.sllogic.isRequested(2, self.getConditions().getEmR().getValue(2), t):
                    if self.sllogic.evaluateExtension(False, t, 5, 6554):
                        self.setNextPhaseID(8)
                elif self.sllogic.isRequested(3, self.getConditions().getReq().fz21.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 15):
                        self.setNextPhaseID(2)
                elif self.sllogic.isRequested(4, self.getConditions().getReq().ph2_f100.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 10):
                        self.setNextPhaseID(2)
                elif self.sllogic.isRequested(5, self.getConditions().getReq().ph2_fz40.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 15):
                        self.setNextPhaseID(2)
                elif self.sllogic.isRequested(6, self.getConditions().getReq().ph2_fg300.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 10):
                        self.setNextPhaseID(2)
                elif self.sllogic.isRequested(7, self.getConditions().getReq().fz21.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 22):
                        self.setNextPhaseID(3)
                elif self.sllogic.isRequested(8, self.getConditions().getReq().f100.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 15):
                        self.setNextPhaseID(3)
                elif self.sllogic.isRequested(9, self.getConditions().getReq().fz40.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 22):
                        self.setNextPhaseID(5)
                elif self.sllogic.isRequested(10,self.getConditions().getReq().fg300.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().maindirection.getValue(), t, 5, 15):
                        self.setNextPhaseID(5)
            # from phase 2
            elif self.getCurrentPhaseID() == 2:
                self.sllogic.setPhase(2, t)
                if self.getConditions().getReq().fz21.getValue():
                    self.setNextPhaseID(3)
                elif self.getConditions().getReq().f100.getValue():
                    self.setNextPhaseID(3)
                elif self.getConditions().getReq().dan.getValue():
                    self.setNextPhaseID(5)
            # from phase 3
            elif self.getCurrentPhaseID() == 3:
                self.sllogic.setPhase(3, t)
                if self.getConditions().getReq().dan.getValue():
                    self.setNextPhaseID(4)
            # from phase 4
            elif self.getCurrentPhaseID() == 4:
                self.sllogic.setPhase(4, t)
                if self.sllogic.isRequested(1, self.getConditions().getEmR().getValue(1), t):
                    if self.sllogic.evaluateExtension(False, t, 0, 6554):
                        self.setNextPhaseID(7)
                elif self.sllogic.isRequested(2, self.getConditions().getEmR().getValue(2), t):
                    if self.sllogic.evaluateExtension(False, t, 0, 6554):
                        self.setNextPhaseID(8)
                elif self.sllogic.isRequested(3, self.getConditions().getReq().fz40.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().fz21.getValue(), t, 0, 5):
                        self.setNextPhaseID(5)
                elif self.sllogic.isRequested(4, self.getConditions().getReq().fg300.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().fz21.getValue(), t, 0, 5):
                        self.setNextPhaseID(5)
                elif self.sllogic.isRequested(5, self.getConditions().getReq().dan.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().fz21.getValue(), t, 0, 5):
                        self.setNextPhaseID(1)
            # from phase 5
            elif self.getCurrentPhaseID() == 5:
                self.sllogic.setPhase(5, t)
                if self.getConditions().getReq().dan.getValue():
                    self.setNextPhaseID(6)
            # from phase 6
            elif self.getCurrentPhaseID() == 6:
                self.sllogic.setPhase(6, t)
                if   self.sllogic.isRequested(1, self.getConditions().getEmR().getValue(1), t):
                    if self.sllogic.evaluateExtension(False, t, 0, 6554):
                        self.setNextPhaseID(7)
                elif self.sllogic.isRequested(2, self.getConditions().getEmR().getValue(2), t):
                    if self.sllogic.evaluateExtension(False, t, 0, 6554):
                        self.setNextPhaseID(8)
                elif self.sllogic.isRequested(3, self.getConditions().getReq().dan.getValue(), t):
                    if self.sllogic.evaluateExtension(self.getConditions().getExt().fz40.getValue(), t, 0, 10):
                        self.setNextPhaseID(1)
            # from fw1
            elif self.getCurrentPhaseID() == 7:
                self.sllogic.setPhase(7, t)
                if self.getConditions().getEmR().getValue(0):
                    self.setNextPhaseID(1)
            # from fw2
            elif self.getCurrentPhaseID() == 8:
                self.sllogic.setPhase(8, t)
                if self.getConditions().getEmR().getValue(0):
                    self.setNextPhaseID(1)

    def run(self, t: float) -> None:
        # process detector data, update conditions
        self.preparationLogic(t)
        if self.somePhaseIsActive():
            self.determineNextPhase(t)
        if self.somePhaseTransitionIsActive():
            if self.currentPhaseIsActive():
                self.getCurrentPhase().end(t)
            if not self.runTransition(t):
                self.setCurrentPhaseID(self.getNextPhaseID())
                self.setNextPhaseID(-1)
        # execute current phase if transition is inactive or ended in previous step
        if self.somePhaseIsActive():
            self.runCurrentPhase(t)


class Siemens:
    def __init__(self, start_time: float = 0.0, step_length: float = 1.0, use_gui: bool = False) -> None:
        self.controller = Controller(use_gui=use_gui)
        self.id = "K048"
        self.step_length = step_length
        self.current_time = start_time
        
    def getController(self):
        return self.controller

    def control(self, t: float) -> None:
        if t > self.current_time:
            self.current_time += self.step_length
            self.controller.run(t)
            if self.controller.newStringAvailable(t):
                sigstr = self.controller.getSUMOCtrlString(t)
                self.getController()._sif.setRedYellowGreenState(self.id, sigstr)
                # print(t, self.controller.getCurrentPhaseID(), self.controller.getNextPhaseID(),
                #       sigstr,
                #       #       [v for v in self.controller.detectorProcessing.det_values[DET_K048.D21]], 
                #       #       self.controller.detectorProcessing.getReq().getValue(SGR_K048.FZ21).getValue(),

                #       )
                
            # print(round(self.controller.detectorProcessing.getDetValue(DET_K048.VD11a,1),1))
            # print(self.controller.sllogic.requestID)
            # print(self.controller.getConditions().getReq().ph2_fz40.getValue())
