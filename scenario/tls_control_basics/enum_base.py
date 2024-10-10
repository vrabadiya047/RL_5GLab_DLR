#!/usr/bin/env python3

from enum import Enum, unique

@unique
class SGR_Base(Enum):
    """
    Base enumeration for signal groups
    """
    pass

@unique
class DET_Base(Enum):
    """
    Base enumeration for detectors
    """
    pass

@unique
class SignalState(Enum):
    """
    Base enumeration for signal states
    """
    STOP        = 0
    GO          = 1
    T_GO_STOP   = 2
    T_STOP_GO   = 3
    OFF         = 4

@unique
class SignalPattern(Enum):
    """
    Base enumeration for signal patterns
    """
    RED         = 0
    GREEN       = 1
    YELLOW      = 2
    REDYELLOW   = 3
    DARK        = 4    