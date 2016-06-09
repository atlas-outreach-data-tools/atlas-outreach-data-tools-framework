"""The functionality found here implements a metadata database used to manipulate the histograms
It also implements the possibulity to do rebinning. which can be enabled in the configuration yaml
for plotting via:
    histogram          : {rebin = 2}
with the number specifying the number of bins that will be merged into one.
"""

import ROOT
from collections import OrderedDict

import infofile

config      = dict()
histoptions = OrderedDict()
rootFiles   = dict()
scaleDB     = infofile.infos

def getScaleFactor(scalingkey):
    """Scaling is done by calculating the luminosity of the sample via xsec/(sumw*red_eff) and
    multiplying the target luminosity"""
    entry = scaleDB[scalingkey]
    return config["Luminosity"]*entry["xsec"]/(entry["sumw"]*entry["red_eff"])
    
def UpdateDataBase(configuration, histogramName):
    global histoptions
    config["HistLocation"]   = histogramName
    config["InputDirectory"] = configuration["InputDirectory"]
    config["Luminosity"]     = configuration["Luminosity"]
    histoptions = configuration["Histograms"][histogramName]

def getHistogram(subcontribution, doScaling):
    # Check whether root file has been opened yet and add it to dictionary of root files
    if subcontribution not in rootFiles:
      rootFiles[subcontribution] = ROOT.TFile.Open( "%s/%s.root" % (config["InputDirectory"], subcontribution), "READ")
      return getHistogram(subcontribution, doScaling)
    
    # Retrieve histogram
    hist = rootFiles[subcontribution].Get(config["HistLocation"]).Clone()
    if doScaling:
      hist.Scale(getScaleFactor(subcontribution))
    if "rebin" in histoptions: hist.Rebin(histoptions["rebin"])
    return hist    
    
    