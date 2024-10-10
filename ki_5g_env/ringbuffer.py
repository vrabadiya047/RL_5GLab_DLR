from statistics import mean
from typing import List
from random import random

class Ringbuffer:
    
    def __init__(self, length: int, fill_value = 0) -> None:
        assert length > 0, "Length of Ringbuffer must be at least 1."
        self._length = length
        self._data = [fill_value for _ in range(length)]
        self._current_id = 0
        
        
    def write(self, value: float) -> None:
        self._data[self._current_id] = value
        self.increase_current_id()
        
        
    def increase_current_id(self) -> None:
        self._current_id = (self._current_id+1)%self._length
        
    
    def get_mean(self) -> float:
        return mean(self._data)
    
    
    def get_sum(self) -> float:
        return sum(self._data)
    
    
    def get_length(self) -> int:
        return self._length
    
    
    def get_data(self) -> List[float]:
        return self._data
    
    
    def get_sorted_data(self) -> List[float]:
        out = []
        for i in range(self.get_length()):
            out.append(self._data[(self._current_id+i)%self.get_length()])
        out.reverse()
        return out
    
    
    def _print(self) -> None:
        out = self.get_sorted_data()
        print(out)
        return None
        
    
    def reset(self, fill_value = 0) -> None:
        self._data = [fill_value for _ in range(len(self._data))]
        return None