import ROOT
import time
import StandardHistograms as SH

#======================================================================

class HistManager(object):    
    """Histogram managing tool for the analysis class."""
    def __init__(self, name):
        super(HistManager, self).__init__()
        # Configurable
        self.Name = name

        self.Histograms = {}


    def getHistogram(self, histName):
        return self.HistManager.getHistogram(histName)
        if histName in self.Histograms:
            return self.Histograms[histName]
        else:
            self.log("Histogram with name " + histName + " not found")
            return None

    def addHistogram(self, histName, histogram):
        if histName in self.Histograms:
            print "Histogram with name " + histName + " already defined!"
        else:
            self.Histograms[histName] = histogram
        return histogram
        
    def addStandardHistogram(self, histName):
        histogram = SH.getStandardHistogram(histName)
        if histogram is None: 
            self.log("Histogram with name " + histName + " not found")
            return None
        return self.addHistogram(histName, histogram)

    def writeHistograms(self):
        [hist.Write() for hist in self.Histograms.values()]

    # Utility function
    def log(self, message):
        print time.ctime() + " HistManager " + self.Name + ": " + message
        
