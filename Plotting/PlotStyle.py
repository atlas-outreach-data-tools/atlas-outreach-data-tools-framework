"""The general style that is to be applied is defined here. Note that it is not an official ATLAS style but
has been adapted to the personal tastes of the author. Change it if it does not fit your taste but take note 
that ROOT sometimes has a will of its own and you may find yourself frustrated sooner than later.
"""

import ROOT

def setStyle():
  atlasStyle = ROOT.TStyle("ATLAS","Atlas style")

  # use plain black on white colors
  icol = 0 # WHITE
  atlasStyle.SetFrameBorderMode(icol)
  atlasStyle.SetFrameFillColor(icol)
  atlasStyle.SetCanvasBorderMode(icol)
  atlasStyle.SetCanvasColor(icol)
  atlasStyle.SetPadBorderMode(icol)
  atlasStyle.SetPadColor(icol)
  atlasStyle.SetStatColor(icol)

  # set the paper & margin sizes
  atlasStyle.SetPaperSize(20,26)

  # set margin sizes
  atlasStyle.SetPadTopMargin(0.10)
  atlasStyle.SetPadRightMargin(0.05)
  atlasStyle.SetPadBottomMargin(0.16)
  atlasStyle.SetPadLeftMargin(0.16)

  # set title offsets (for axis label)
  atlasStyle.SetTitleStyle(0)
  atlasStyle.SetTitleBorderSize(0)
  atlasStyle.SetTitleX(0.5)
  atlasStyle.SetTitleY(0.97)
  atlasStyle.SetTitleAlign(23);
  atlasStyle.SetTitleXOffset(2)
  atlasStyle.SetTitleYOffset(2)

  # use large fonts
  font  = 43   # Helvetica
  tsize = 25
  atlasStyle.SetTextFont(42)
  atlasStyle.SetTextSize(0.03)

  atlasStyle.SetLabelFont(font,"x")
  atlasStyle.SetTitleFont(font,"x")
  atlasStyle.SetLabelFont(font,"y")
  atlasStyle.SetTitleFont(font,"y")
  atlasStyle.SetLabelFont(font,"z")
  atlasStyle.SetTitleFont(font,"z")
  
  atlasStyle.SetLabelSize(tsize,"x")
  atlasStyle.SetTitleSize(tsize,"x")
  atlasStyle.SetLabelSize(tsize,"y")
  atlasStyle.SetTitleSize(tsize,"y")
  atlasStyle.SetLabelSize(tsize,"z")
  atlasStyle.SetTitleSize(tsize,"z")

  # use bold lines and markers
  atlasStyle.SetMarkerStyle(20)
  atlasStyle.SetMarkerSize(1)
  atlasStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

  # get rid of X error bars and y error bar caps
  atlasStyle.SetErrorX(0.001)

  # do not display any of the standard histogram decorations
  atlasStyle.SetOptTitle(1)
  atlasStyle.SetOptStat(0)
  atlasStyle.SetOptFit(0)

  # put tick marks on top and RHS of plots
  atlasStyle.SetPadTickX(1)
  atlasStyle.SetPadTickY(1)

  # enforce the style
  ROOT.gROOT.SetStyle("ATLAS");
  ROOT.gROOT.ForceStyle();