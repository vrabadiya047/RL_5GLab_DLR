#!/usr/bin/env python3

from enum import unique
from scenario.tls_control_basics.enum_base import SGR_Base, DET_Base

@unique
class SGR_K048(SGR_Base):
    """
    Specific enumeration for signalgroupes of K048, child of SGR_Base
    """
    FZ11 = 1
    FZ12 = 2
    FZ21 = 3
    FZ31 = 4
    FZ32 = 5
    FZ33 = 6
    FZ41 = 7
    FZ42 = 8
    R11 = 9
    R21 = 10
    R31 = 11
    R41 = 12
    F101 = 13
    F102 = 14
    F103 = 15
    F104 = 16
    F201_202 = 17
    F301 = 18
    F302 = 19
    F303 = 20
    F304 = 21
    F401 = 22
    F402 = 23
    F403_404 = 24

@unique
class DET_K048(DET_Base):
    """
    Specific enumeration for detectors of K048, child of DET_Base
    """
    VD11 = 1
    VD11a = 2
    D21 = 3
    VD31 = 4
    VD31a = 5
    VD31b = 6
    D32 = 7
    D41 = 8
    VD41 = 9
    D42 = 10
    VD42 = 11
    T_R21 = 12
    T_R41 = 13
    T_F101 = 14
    T_F102 = 15
    T_F103 = 16
    T_F104 = 17
    T_F301 = 18
    T_F302 = 19
    T_F303 = 20
    T_F304 = 21