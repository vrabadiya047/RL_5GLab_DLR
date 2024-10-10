import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import sumolib
# import libsumo
import traci
import time
from typing import List, Dict, Tuple

sys.path.append(os.path.dirname(os.path.dirname(__file__) + "\\..\\"))
from scenario.demand import FLOW_DIRECTIONS

DIR_PATH = os.path.dirname(os.path.dirname(__file__) + "/../")

from scenario.k048.control import Siemens
from ki_5g_env.detector_data_accumulation import DetectorDataAccumulationMap
from ki_5g_env.waiting_vehicle_estimate import K048_VehicleCountEstimate
from ki_5g_env.caching import StepCache
from scenario.k048.enum import DET_K048


class SumoHandler:
    _EM_NOPHASE = 0
    _EM_PHASE1 = 1
    _EM_VEH_ID = "firecar"
    _EM_VEH_DESIRED_SPEED = 50.0 / 3.6
    _EM_VEH_MAX_DISTANCE = 1000.0

    def __init__(self, use_gui=False, model_name="test_model", sumo_output=False) -> None:
        self._use_gui = use_gui
        self._sumo_output = sumo_output
        if self._use_gui:
            self._sumo_binary = sumolib.checkBinary('sumo-gui')
            self._lib = traci
        else:
            self._sumo_binary = sumolib.checkBinary('sumo')
            self._lib = traci
        self.model_name = model_name

        self._step_length = 1
        self._sim_step = 0
        self._seed = 0
        self._is_running = False
        self._cache = StepCache()
        self._junction_control = Siemens(use_gui=self._use_gui)
        self._last_em_veh_distance_to_junction = self._EM_VEH_MAX_DISTANCE

        # self._accumulated_detector_data = DetectorDataAccumulationMap(DET_K048, 60)
        self._veh_estimate = K048_VehicleCountEstimate()

        self._ev_in_front_of_stopline = False

    def reset(self) -> None:
        self._set_simulation_step(0)
        self._junction_control = Siemens(use_gui=self._use_gui)
        self._ev_in_front_of_stopline = False
        self._veh_estimate.reset()

    def start_sumo(self) -> None:
        sumo_cmd = [self._sumo_binary,
                    "-c", DIR_PATH + "/scenario/tostmannplatz.sumocfg",
                    "--no-step-log", "true",
                    "-W",
                    "--duration-log.disable",
                    '--seed', str(self._seed),
                    # "--quit-on-end",
                    ]
        if self._sumo_output:
            sumo_cmd.extend(["--tripinfo-output", str(DIR_PATH) + "/outputs/sumo/" + self.model_name + "/tripinfo.xml",
                             "--tripinfo-output.write-unfinished", "True", '--output-prefix',
                             time.strftime("%Y%m%d-%H%M%S_")])
        # print("SUMO_CMD: ",sumo_cmd)
        self._start_sim(sumo_cmd)

    def stop_sumo(self) -> None:
        self._stop_sim()

    def sumo_is_running(self) -> bool:
        return self._is_running

    def set_seed(self, seed: int) -> None:
        self._seed = seed

    def do_simulation_step(self) -> None:
        self.increase_simulation_step()
        t = self.get_current_simulation_time()
        self._lib.simulationStep(t)
        self.get_junction_control().control(t)
        # self._accumulated_detector_data.update(self.get_junction_control().getController().detectorProcessing.getDetValues())
        self._veh_estimate.update(
            self.get_junction_control().getController().getDetValues(),
            self.get_junction_control().getController().getCurrentPhaseID())

    def _start_sim(self, sumo_cmd: List[str]) -> None:
        self._lib.start(sumo_cmd)
        self._is_running = True

    def _stop_sim(self) -> None:
        self._lib.close()
        self._is_running = False

    def get_veh_estimate(self) -> Tuple[float, float, float, float]:
        return self._veh_estimate.get_normalized_counts()

    def get_simulation_step(self) -> int:
        return self._sim_step

    def get_current_simulation_time(self) -> float:
        return self.get_simulation_step() * self.get_simulation_step_length()

    def get_simulation_step_length(self) -> float:
        return self._step_length

    def increase_simulation_step(self, steps=1) -> None:
        self._set_simulation_step(self.get_simulation_step() + steps)

    def _set_simulation_step(self, step: int) -> None:
        self._sim_step = step

    def get_junction_control(self) -> Siemens:
        return self._junction_control

    def request_em_phase(self) -> None:
        self.get_junction_control().getController().setEmergencyRequest(self.get_current_simulation_time(),
                                                                        self._EM_PHASE1)

    def release_em_phase(self) -> None:
        self.get_junction_control().getController().setEmergencyRequest(self.get_current_simulation_time(),
                                                                        self._EM_NOPHASE)

    def em_phase_is_requested(self) -> bool:
        return self.get_junction_control().getController().getConditions().getEmR().getValue(self._EM_PHASE1)

    def em_phase_is_running(self) -> bool:
        return self.get_junction_control().getController().getCurrentPhaseID() == 7 and self.get_junction_control().getController().getNextPhaseID() == -1

    def em_phase_transition_is_running(self) -> bool:
        return self.get_junction_control().getController().getNextPhaseID() == 7

    def _simulation_has_em_vehicle(self) -> bool:
        return self._EM_VEH_ID in self._lib.vehicle.getIDList()

    def simulation_has_em_vehicle(self) -> bool:
        return self._cache.get_value(self._simulation_has_em_vehicle, self.get_simulation_step())

    def insert_em_vehicle(self) -> None:
        route = self._EM_VEH_ID + '_route'
        veh_type = 'firecar'
        self._lib.route.add(route, [FLOW_DIRECTIONS[7][0], FLOW_DIRECTIONS[7][1]])
        self._lib.vehicle.add(self._EM_VEH_ID, route, veh_type, departSpeed="max")

    def _get_em_veh_distance_to_junction(self,
                                         EDGE_LENGTH_CACHE: Dict[str, float] = dict(),
                                         EDGE_ORDER: List[str] = ["gneE4", "51812159", "51812159.-60", "51932979"]
                                         ) -> float:

        def edge_length(edge_id: str) -> float:
            if not edge_id in EDGE_LENGTH_CACHE:
                EDGE_LENGTH_CACHE[edge_id] = self._lib.lane.getLength(edge_id + "_0")
            return EDGE_LENGTH_CACHE[edge_id]

        def get_distance(edge_id: str, dist: float):
            distance = -dist
            if edge_id in EDGE_ORDER:
                id = EDGE_ORDER.index(edge_id)
                for i in range(id, len(EDGE_ORDER)):
                    distance += edge_length(EDGE_ORDER[i])
            if distance < 0:
                distance = self._last_em_veh_distance_to_junction
            self._last_em_veh_distance_to_junction = min(distance, self._EM_VEH_MAX_DISTANCE)
            return self._last_em_veh_distance_to_junction

        if self.simulation_has_em_vehicle():
            edge = self._lib.vehicle.getRoadID(self._EM_VEH_ID)
            dist = self._lib.vehicle.getLanePosition(self._EM_VEH_ID)
            return get_distance(edge, dist)
        return self._EM_VEH_MAX_DISTANCE

    def get_em_veh_distance_to_junction(self) -> float:
        return self._cache.get_value(self._get_em_veh_distance_to_junction, self.get_simulation_step())

    def _get_em_veh_speed(self) -> float:
        if self.simulation_has_em_vehicle():
            return self._lib.vehicle.getSpeed(self._EM_VEH_ID)
        return self._EM_VEH_DESIRED_SPEED

    def get_em_veh_speed(self) -> float:
        return self._cache.get_value(self._get_em_veh_speed, self.get_simulation_step())

    def get_em_veh_desired_speed(self) -> float:
        return self._EM_VEH_DESIRED_SPEED

    def get_em_veh_max_distance(self) -> float:
        return self._EM_VEH_MAX_DISTANCE

    def _get_number_of_waiting_vehicles(self,
                                        EDGE_LIST=["-51812052", "-51812053", "-786367651", "-554747345", "51812134",
                                                   "51932979", "51812159.-60", "51812159"]
                                        ) -> int:
        waiting_vehicles = 0
        for edge in EDGE_LIST:
            waiting_vehicles += self._lib.edge.getLastStepHaltingNumber(edge)
        return waiting_vehicles

    def get_number_of_waiting_vehicles(self) -> int:
        return self._cache.get_value(self._get_number_of_waiting_vehicles, self.get_simulation_step())

    # def get_det_data(self) -> DetectorDataAccumulationMap:
    #     return self._accumulated_detector_data

    def remove_em_veh(self) -> None:
        self._lib.vehicle.remove(self._EM_VEH_ID)

    def _em_veh_passed_intersection(self) -> bool:
        edge_after_junction = "786367652"
        if self._EM_VEH_ID in self._lib.edge.getLastStepVehicleIDs(edge_after_junction):
            return True
        return False

    def em_veh_passed_intersection(self) -> bool:
        return self._cache.get_value(self._em_veh_passed_intersection, self.get_simulation_step())

    def _em_veh_passed_stopline(self) -> bool:
        edge_before_junction = "51932979"
        if self._EM_VEH_ID in self._lib.edge.getLastStepVehicleIDs(edge_before_junction):
            self._ev_in_front_of_stopline = True
        elif self._ev_in_front_of_stopline:
            return True
        return False

    def em_veh_passed_stopline(self) -> bool:
        return self._cache.get_value(self._em_veh_passed_stopline, self.get_simulation_step())
