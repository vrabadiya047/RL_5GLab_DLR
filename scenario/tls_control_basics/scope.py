#!/usr/bin/env python3

from typing import Tuple, Sequence

class Scope:
    """
    Permission scopes for phases, phase transitions etc. 
    """
    def __init__(self) -> None:
        self.scopes = [] # type: Sequence[Tuple[float, float]]
        
    def addScope(self, value : Tuple[float, float]) -> None:
        self.scopes = self.scopes + value
        
    def setScopes(self, values : Sequence[Tuple[float, float]]) -> None:
        self.scopes = values
        
    def getScope(self, id : int) -> Tuple[float, float]:
        return self.scopes[id]
    
    def isInScope(self, id : int, t : float) -> bool:
        return self.scopes[id][0] <= t and t <= self.scopes[id][1]