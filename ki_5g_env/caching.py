from typing import Mapping, Any, List, Callable

class StepCache:
    def __init__(self) -> None:
        self._data = dict() # type: Mapping[Callable, List[int, Any]]
        
    def get_value(self, fun : Callable, step : int) -> Any:
        if not fun in self._data:
            self._data[fun] = [step, fun()]
        if not step==self._get_step(fun):
            self._data[fun] = [step, fun()]
        return self._get_value(fun)
    
    
    def _get_value(self, fun : Callable) -> Any:
        return self._data[fun][1]
    
    
    def _get_step(self, fun : Callable) -> int:
        return self._data[fun][0]