import time
import sys

#======================================================================

class JobStatistics(object):
    """JobStatistics provides the functionality for monitoring the progess of the current analysis"""
    def __init__(self, maxEvents, isBatch):
        super(JobStatistics, self).__init__()
        self.startTime  = time.time()
        self.MaxEvents  = maxEvents
        self.IsBatch    = isBatch

    def setMaxEvents(self, maxEvents):
        self.MaxEvents = maxEvents

    def resetTimer(self):
        self.startTime = time.time()

    def elapsedTime(self):
        return abs(time.time() - self.startTime)
        
    def updateStatus(self, n, force = False):
        if self.IsBatch: return
        if n % 10000 != 0 and not force: return
        fractionDone = float(n)/float(self.MaxEvents)
        if fractionDone == 0: return
        eft = self.elapsedTime()*(self.MaxEvents/float(n)-1)
        sys.stdout.write('\r')
        sys.stdout.write("%-120s\r" % "")
        sys.stdout.write("[%-20s] %d%% EFT: %4.0fs" % ('='*int(fractionDone*20), fractionDone*100, abs(eft)))
        sys.stdout.flush()