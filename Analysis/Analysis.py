import ROOT
import time

import TupleReader as reader
import HistManager
import EventCounter

#======================================================================

class Analysis(object):
    """Baseclass for all analyses. Common functionality should go here.
    This class handles some of the technicalities that are common to all analyses.    
    """

    def __init__(self, auxName):
        super(Analysis, self).__init__()
        # Configurables
        self.Name         = type(self).__name__
        self.TotName      = auxName + "." + self.Name
        self.isData       = False

        # Functionality providers
        self.Store        = reader.TupleReader()
        self.EventCounter = EventCounter.EventCounter(self.TotName)
        self.HistManager  = HistManager.HistManager(self.TotName)

    #Getters and Setters
    def setIsData(self, isData):
        self.isData = isData

    def getIsData(self):
        return self.isData

    #Execution functions
    def doInitialization(self):
        self.initialize()
      
    def initialize(self):
        pass
        
    def doAnalysis(self):
        eventinfo = self.Store.getEventInfo()
        weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1
        self.countEvent("all", weight)
        if self.analyze():
            self.countEvent("final", weight)
        
    def analyze(self):
        return True
    
    def doFinalization(self):
        self.HistManager.writeHistograms()
        self.EventCounter.printResults()
        self.finalize()

    def finalize(self):
        pass

    #Forwarding functions
    def addHistogram(self, histName, histogram):
        return self.HistManager.addHistogram(histName, histogram)
        
    def addStandardHistogram(self, histName):
        return self.HistManager.addStandardHistogram(histName)

    def getHistogram(self, histName):
        return self.HistManager.getHistogram(histName)
  
    def countEvent(self, cut, weight):
        self.EventCounter.update(cut, weight)
