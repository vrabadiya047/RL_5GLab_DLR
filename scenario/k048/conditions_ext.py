#!/usr/bin/env python3

from scenario.tls_control_basics.conditions import Condition, SignalExtension

class Ext_MainDirection(Condition):
    def update(self, ext_fz11 : SignalExtension, ext_fz31 : SignalExtension):
        self.setValue(ext_fz11.getValue() or ext_fz31.getValue())

class Ext_FZ21(Condition):
    def update(self, ext_fz21 : SignalExtension):
        self.setValue(ext_fz21.getValue())
        
class Ext_FZ40(Condition):
    def update(self, ext_fz41 : SignalExtension, ext_fz42 : SignalExtension):
        self.setValue(ext_fz41.getValue() or ext_fz42.getValue())