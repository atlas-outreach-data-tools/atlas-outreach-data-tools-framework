"""Here, the various paintables are defined. The idea behind the paintable is to split the problem of
plotting something into logical pieces. A paintable represents a commonly encountered representation of 
data. The usual way to plot these representations is encoded in the deriving classes.
Available paintables are:
StackPaintable:   usually used to plot the various contributions from simulated data in a stacked fashion 
DataPaintable:    used to paint the data measured
OverlayPaintable: used to overlay distributions, e.g. some exotic signal to compare its shape to that of the
                  other contributions.
"""

import ROOT
import PlotStyle as PS
import Database as DB
    
class Paintable(object):
    """Baseclass for all paintables. The definition data member is a dictionary that holds information 
    needed for painting as well as options that may be used for additional uses and will be documented
    accordingly.
    Used keys:
    Contributions: is a list of processes as defined in the Configurations.py. All of the contributions
                   will be added to a summary histogram
    """
    def __init__(self, name, definition):
        super(Paintable, self).__init__()
        self.definition = definition
        self.name = name
        self.drawOption = ""

    def getNumberOfLegendItems(self):
        return 1
             
    def getContribution(self, contributiondata, doScaling = True):
        sumhist = None
        for subcontribution in contributiondata["Contributions"]:
          hist = DB.getHistogram(subcontribution, doScaling)
          if sumhist:
            sumhist.Add(hist)
          else:
            sumhist = hist
        return sumhist


class StackPaintable(Paintable):
    """The StackPaintable is used to represent a stack of contributions that may represent the composition
    of the theoretical predicitions. Each contribution has its own colour definition.
    """
    def __init__(self, name, definition):
        super(StackPaintable, self).__init__(name, definition)
        self.stack = ROOT.THStack()
        self.legendData = []
        self.createPaintable()

    def createPaintable(self):
        for process in self.definition["Order"]:  
            contributiondata = self.definition["Processes"][process]
            sumhist = self.getContribution(contributiondata)
            sumhist.SetFillColor(ROOT.TColor.GetColor(contributiondata["Color"]))
            contributiondata["hist"] = sumhist
            self.legendData.append((contributiondata["hist"], process, "f"))
            self.stack.Add(sumhist)

    def getNumberOfLegendItems(self):
        return len(self.legendData)

    def addToLegend(self, legend):
        for item in self.legendData:
            legend.AddEntry(item[0], item[1], item[2])
    
    def getMaximum(self):
        return self.stack.GetMaximum()
    
    def getHistogram(self):
        stack = self.stack.GetStack()
        return stack[len(stack)-1]
    
    def draw(self, option = ""):
        self.stack.Draw("hist" + option)
        self.stack.SetTitle(self.stack.GetHists()[0].GetTitle())
        self.stack.GetXaxis().SetTitle(self.stack.GetHists()[0].GetXaxis().GetTitle())
        self.stack.GetYaxis().SetTitle(self.stack.GetHists()[0].GetYaxis().GetTitle())
         
         
class DataPaintable(Paintable):
    """The DataPaintable implements the usual data depiction via markers and 
    statistical error bars.
    """
    def __init__(self, name, definition):
        super(DataPaintable, self).__init__(name, definition)
        self.datahist = None
        self.createPaintable()
        self.drawOption = "E"
        
    def createPaintable(self):
        self.datahist = self.getContribution(self.definition, False) 
        self.definition['hist'] = self.datahist

    def addToLegend(self, legend):
        legend.AddEntry(self.datahist, "Data", "p")
        
    def getMaximum(self):
        return self.datahist.GetMaximum()    
    
    def getHistogram(self):
        return self.datahist
    
    def draw(self, option = ""):
        self.datahist.Draw(option)

class OverlayPaintable(Paintable):
    """The OverlayPaintable may be used to depict the shape of multiple signal hypotheses
    Two option are given:
    Color : determines the color in hex code that the overlay is drawn in
    Scale : a scaling can be applied in case the overlay is very small    
    """
    def __init__(self, name, definition):
        super(OverlayPaintable, self).__init__(name, definition)
        self.hist = None
        self.drawOption = "hist"
        self.scale = 1
        self.createPaintable()
        
    def createPaintable(self):
        self.hist = self.getContribution(self.definition, True) 
        self.hist.SetLineColor(ROOT.TColor.GetColor(self.definition["Color"]))
        self.hist.SetLineWidth(2)
        self.scale = self.definition['Scale'] if 'Scale' in self.definition else 1
        self.hist.Scale(self.scale)

        self.definition['hist'] = self.hist

    def addToLegend(self, legend):
        addition = "" if self.scale == 1 else " x " + str(self.scale)
        legend.AddEntry(self.hist, self.name+addition, "l")
        
    def getMaximum(self):
        return self.hist.GetMaximum()    
    
    def getHistogram(self):
        return self.hist
    
    def draw(self, option = ""):
        self.hist.Draw(self.drawOption + option)
