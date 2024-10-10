import sys, os
from typing import Dict, Mapping, Tuple

sys.path.append(os.path.dirname(os.path.dirname(__file__) + "\\..\\"))
from ki_5g_env.ringbuffer import Ringbuffer
from scenario.tls_control_basics.enum_base import DET_Base


class DetectorDataAccumulation:
    def __init__(self, accumulation_length=60) -> None:
        self._accumulation_length = accumulation_length
        self._veh_count = Ringbuffer(accumulation_length)
        self._occupancy = Ringbuffer(accumulation_length)

    def get_accumulation_length(self) -> int:
        return self._accumulation_length

    def get_vehicle_count(self) -> int:
        return self._veh_count.get_sum()

    def get_occupancy(self) -> float:
        return self._occupancy.get_mean()

    def write(self, veh_count: int, occupancy: bool):
        self._veh_count.write(veh_count)
        self._occupancy.write(int(occupancy))


class DetectorDataAccumulationMap:
    def __init__(self, det_keys: DET_Base, accumulation_length=60) -> None:
        self._data = dict()  # type: Dict[DET_Base, DetectorDataAccumulation]
        self._accumulation_length = accumulation_length
        for key in det_keys:
            self._data[key] = DetectorDataAccumulation(accumulation_length)

    def get_accumulation_length(self) -> int:
        return self._accumulation_length

    def update(self, det_values: Mapping[DET_Base, Tuple[int, float, bool, int]]):
        for key in det_values:
            veh_count = det_values[key][3]
            occupancy = det_values[key][0]
            self._data[key].write(veh_count, occupancy)

    def get_data(self) -> Dict[DET_Base, DetectorDataAccumulation]:
        return self._data
