#!/usr/bin/env python3

class Timer:
    def __init__(self) -> None:
        self.startTime = 0.0
        self.stopTime = 0.0
        self.running = False
        
    def getDurationSinceStart(self, t : float) -> float:
        return t - self.startTime
    
    def getDurationSinceStop(self, t : float) -> float:
        return t - self.stopTime
    
    def isRunning(self) -> bool:
        return self.running
    
    def startTimer(self, t : float) -> None:
        self.startTime = t
        self.running = True
        
    def stopTimer(self, t : float) -> None:
        self.stopTime = t
        self.running = False