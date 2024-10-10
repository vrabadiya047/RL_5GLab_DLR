from .timer import Timer

class SLLogic:
    UNDEFINED = -1
    def __init__(self) -> None:
        self.phaseId = self.UNDEFINED
        self.requestId = self.UNDEFINED
        self.timer = Timer()

    def setPhase(self, phaseId: int, t: float) -> None:
        if not self.phaseId == phaseId:
            self.phaseId = phaseId
            self.timer.stopTimer(t)
            self.requestId = self.UNDEFINED

    def setRequestID(self, reqId: int, t: float) -> None:
        if not self.getRequestID() == reqId:
            if reqId >= self.getRequestID():
                if self.timer.isRunning():
                    self.timer.stopTimer(t)
                self.timer.startTimer(t)
            self.setIdPlain(reqId)

    def getRequestID(self) -> int:
        return self.requestId
    
    def setIdPlain(self, id: int) -> None:
        self.requestId = id
    
    def isRequested(self, reqId :int, req :bool, t :float) -> bool:
        if((self.getRequestID() == self.UNDEFINED or reqId < self.getRequestID()) and req) or self.getRequestID() == reqId:
            self.setRequestID(reqId, t)
            return True
        return False
    
    def evaluateExtension(self, ext :bool, t :float, minDur :float, maxDur :float) -> bool:
        if(self.getRequestDuration(t) >= minDur and not ext) or self.getRequestDuration(t) >= maxDur:
            return True
        return False

    def getRequestDuration(self, t: float) -> int:
        if not (self.requestId == self.UNDEFINED or self.phaseId == self.UNDEFINED):
            return self.timer.getDurationSinceStart(t)
        return self.UNDEFINED