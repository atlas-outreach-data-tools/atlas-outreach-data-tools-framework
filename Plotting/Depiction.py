"""Depictions define certain standardized plot varieties. Each depiction class specifies how the plot variety
at hand is implemented. The contents of these depictions are the individual paintables.
Currently available depictions are:
MainDepiction: Simple plot that shows the contributions of various Paintables
Ratio:         shows the ratio between two Paintables
Agreement:     similar to ratio but emphasises the region around a ratio of 1, usually used to test data/mc agreement
"""
import ROOT
import PlotStyle as PS
import Database as DB

class Depiction(object):
    """Base class for all other depictions
    name: names the TPad that will be drawn
    configuration: is a dictionary specifying the way the depiction is painted
        Paintables: gives the painting order in which the paintables are considered
    """
    def __init__(self, configuration, name):
        super(Depiction, self).__init__()
        self.name          = name
        self.configuration = configuration
        self.pad           = None
        self.PaintingOrder = configuration["Paintables"]

    def initializeDepiction(self, x1, y1, x2, y2, topMargin, bottomMargin):
        self.pad = ROOT.TPad(self.name,self.name,x1, y1,x2, y2);
        self.pad.SetBottomMargin(bottomMargin);
        self.pad.SetTopMargin(topMargin);
        self.pad.Draw()


class MainDepiction(Depiction):
    """MainDepiction implements a simple plot which shows the results of various predictions or the data.
    The painting order is important as paintables later in the order may mask earlier paintables.
    MainDepiction is sensitive to the following hist_options:
    log_y : shows the contents in logarithmic scale (do histogram : {log_y = True})
    """
    def __init__(self, configuration, name):
        super(MainDepiction, self).__init__(configuration, name)
        
    def drawDepiction(self, paintables):
        self.pad.cd()
        if "log_y" in DB.histoptions: self.pad.SetLogy(int(DB.histoptions["log_y"]))
        paintablesToPaint = [paintables[key] for key in self.PaintingOrder]
        margin = DB.histoptions.get("y_margin", 0.1)
        maximum = max(item.getMaximum() for item in paintablesToPaint)*(margin+1)
        paintablesToPaint[0].getHistogram().SetMaximum(maximum)
        paintablesToPaint[0].getHistogram().SetMinimum(0.1)

        option = ""
        for paintable in paintablesToPaint:
            paintable.draw(paintable.drawOption + option)
            option = "same"
 
class RatioDepiction(Depiction):
    """RatioDepiction shows the ratio between the first paintable and the second paintable"""
    def __init__(self, configuration, name):
        super(RatioDepiction, self).__init__(configuration, name)

    def drawDepiction(self, paintables):
        self.extractRatioHistogram(paintables)
        self.drawRatioHistogram()
    
    def extractRatioHistogram(self, paintables):
        ROOT.TH1.AddDirectory(False)
        self.ratioHistogram = paintables[self.PaintingOrder[0]].getHistogram().Clone()
        self.ratioHistogram.Divide(paintables[self.PaintingOrder[1]].getHistogram())
    
    def drawRatioHistogram(self):
        self.pad.cd()
        self.setBounds()
        self.ratioHistogram.GetYaxis().SetTitle(self.name)
        self.ratioHistogram.GetYaxis().SetNdivisions(505)
        self.ratioHistogram.SetTitle("")
        self.ratioHistogram.SetFillColor(ROOT.kWhite)
        self.ratioHistogram.SetLineColor(ROOT.kBlack)
        self.ratioHistogram.Draw("")

    def setBounds(self):
        histmax = self.ratioHistogram.GetBinContent(self.ratioHistogram.GetMaximumBin())
        self.ratioHistogram.SetMaximum(histmax*1.1)
        self.ratioHistogram.SetMinimum(0.0)

                
class AgreementDepiction(RatioDepiction):
    """AgreementDepiction shows the ratio between the first paintable and the second paintable with a
    special emphasis of the ratio region around 1.
    """
    def __init__(self, configuration, name):
        super(AgreementDepiction, self).__init__(configuration, name)

    def drawDepiction(self, paintables):
        self.extractRatioHistogram(paintables)
        self.drawRatioHistogram()
        self.drawReferenceLine()
        self.drawOverallAgreement(paintables)
    
    def setBounds(self):
        self.ratioHistogram.SetMaximum(2)
        self.ratioHistogram.SetMinimum(0.5)
        
    def drawReferenceLine(self):
        self.pad.cd()
        self.line = ROOT.TLine(self.ratioHistogram.GetXaxis().GetXmin(),1, self.ratioHistogram.GetXaxis().GetXmax(), 1)
        self.line.SetLineStyle(2)
        self.line.SetLineColor(ROOT.kGray+3)
        self.line.Draw("same")

    def drawOverallAgreement(self, paintables):
        self.pad.cd()
        meanvalue = paintables[self.PaintingOrder[0]].getHistogram().Integral()/paintables[self.PaintingOrder[1]].getHistogram().Integral()
        self.mean = ROOT.TLine(self.ratioHistogram.GetXaxis().GetXmin(),meanvalue, self.ratioHistogram.GetXaxis().GetXmax(), meanvalue)
        self.mean.SetLineStyle(3)
        self.mean.Draw("same")
                
