from typing import List, Mapping, Tuple
from scenario.k048.enum import DET_Base, DET_K048


class VehicleCountEstimate:
    def __init__(self, max_count, clearing_phases: List[int], detectors: List[DET_Base]) -> None:
        self._max_count = max_count
        self._clearing_phases = clearing_phases
        self._detectors = detectors  # type: # List[int]
        self._count = 0
        return None

    def get_count(self) -> int:
        return min(self._count, self._max_count)

    def get_normalized_count(self) -> float:
        return self.get_count() / self._max_count

    def update(self, det_values: Mapping[DET_Base, Tuple[int, float, bool, int]], cur_phase: int) -> None:
        # det_values = {det_id: (number of vehicles on detector, time gap, button press, new vehicle count)}
        if cur_phase in self._clearing_phases:
            self._count = 0
        for det in self._detectors:
            self._count += det_values[det][3]
        return None

    def reset(self) -> None:
        self._count = 0
        return None


class K048_VehicleCountEstimate:
    def __init__(self) -> None:
        self._north = VehicleCountEstimate(6, [1], [DET_K048.VD11, DET_K048.VD11a])
        self._east = VehicleCountEstimate(1, [5], [DET_K048.D21])
        self._south = VehicleCountEstimate(9, [1], [DET_K048.VD31, DET_K048.VD31a, DET_K048.VD31b])
        self._west = VehicleCountEstimate(8, [2], [DET_K048.VD41, DET_K048.VD42])
        return None

    def update(self, det_values: Mapping[DET_Base, Tuple[int, float, bool, int]], cur_phase: int) -> None:
        self._north.update(det_values, cur_phase)
        self._east.update(det_values, cur_phase)
        self._west.update(det_values, cur_phase)
        self._south.update(det_values, cur_phase)
        return None

    def reset(self) -> None:
        self._north.reset()
        self._east.reset()
        self._south.reset()
        self._west.reset()
        return None

    def get_normalized_counts(self) -> Tuple[float, float, float, float]:
        return self._north.get_normalized_count(), self._east.get_normalized_count(), self._south.get_normalized_count(), self._west.get_normalized_count()

    def get_counts(self) -> Tuple[int, int, int, int]:
        return self._north.get_count(), self._east.get_count(), self._south.get_count(), self._west.get_count()
