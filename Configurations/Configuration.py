Job = {
    "Batch"           : True,
    "Analysis"        : "TTbarAnalysis",
    "Fraction"        : 1,
    "MaxEvents"       : 1234567890,
    "OutputDirectory" : "results/"
}

#VBSAnalysis

Processes = {
  # Diboson processes
  "WW"                    : "Input/MC/mc_105985.WW.root",
  "ZZ"                    : "Input/MC/mc_105986.ZZ.root",
  "WZ"                    : "Input/MC/mc_105987.WZ.root",

  # single top processes
  "stop_tchan_top"        : "Input/MC/mc_110090.stop_tchan_top.root",
  "stop_tchan_antitop"    : "Input/MC/mc_110091.stop_tchan_antitop.root",
  "stop_schan"            : "Input/MC/mc_110119.stop_schan.root",
  "stop_wtchan"           : "Input/MC/mc_110140.stop_wtchan.root",

  # top pair processes
  "ttbar_had"             : "Input/MC/mc_117049.ttbar_had.root",
  "ttbar_lep"             : "Input/MC/mc_117050.ttbar_lep.root",

  # Z+jets processes
  "Zee"                   : "Input/MC/mc_147770.Zee.root",
  "Zmumu"                 : "Input/MC/mc_147771.Zmumu.root",
  "Ztautau"               : "Input/MC/mc_147772.Ztautau.root",

  # Low Mass Z+jets processes
  "DYeeM08to15"           : "Input/MC/mc_173041.DYeeM08to15.root",
  "DYeeM15to40"           : "Input/MC/mc_173042.DYeeM15to40.root",
  "DYmumuM08to15"         : "Input/MC/mc_173043.DYmumuM08to15.root",
  "DYmumuM15to40"         : "Input/MC/mc_173044.DYmumuM15to40.root",
  "DYtautauM08to15"       : "Input/MC/mc_173045.DYtautauM08to15.root",
  "DYtautauM15to40"       : "Input/MC/mc_173046.DYtautauM15to40.root",

  # W+jets processes
  "WenuWithB"             : "Input/MC/mc_167740.WenuWithB.root",
  "WenuJetsBVeto"         : "Input/MC/mc_167741.WenuJetsBVeto.root",
  "WenuNoJetsBVeto"       : "Input/MC/mc_167742.WenuNoJetsBVeto.root",
  "WmunuWithB"            : "Input/MC/mc_167743.WmunuWithB.root",
  "WmunuJetsBVeto"        : "Input/MC/mc_167744.WmunuJetsBVeto.root",
  "WmunuNoJetsBVeto"      : "Input/MC/mc_167745.WmunuNoJetsBVeto.root",
  "WtaunuWithB"           : "Input/MC/mc_167746.WtaunuWithB.root",
  "WtaunuJetsBVeto"       : "Input/MC/mc_167747.WtaunuJetsBVeto.root",
  "WtaunuNoJetsBVeto"     : "Input/MC/mc_167748.WtaunuNoJetsBVeto.root",

  # Higgs Processes
  "ggH125_ZZ4lep"         : "Input/MC/mc_160155.ggH125_ZZ4lep.root",
  "VBFH125_ZZ4lep"        : "Input/MC/mc_160205.VBFH125_ZZ4lep.root",
  "ggH125_WW2lep"         : "Input/MC/mc_161005.ggH125_WW2lep.root",
  "VBFH125_WW2lep"        : "Input/MC/mc_161055.VBFH125_WW2lep.root",

  # ZPrime Processes
  "ZPrime400"             : "Input/MC/mc_110899.ZPrime400.root",
  "ZPrime500"             : "Input/MC/mc_110901.ZPrime500.root",
  "ZPrime750"             : "Input/MC/mc_110902.ZPrime750.root",
  "ZPrime1000"            : "Input/MC/mc_110903.ZPrime1000.root",
  "ZPrime1250"            : "Input/MC/mc_110904.ZPrime1250.root",
  "ZPrime1500"            : "Input/MC/mc_110905.ZPrime1500.root",
  "ZPrime1750"            : "Input/MC/mc_110906.ZPrime1750.root",
  "ZPrime2000"            : "Input/MC/mc_110907.ZPrime2000.root",
  "ZPrime2250"            : "Input/MC/mc_110908.ZPrime2250.root",
  "ZPrime2500"            : "Input/MC/mc_110909.ZPrime2500.root",
  "ZPrime3000"            : "Input/MC/mc_110910.ZPrime3000.root",

  # Data
  "data_Egamma"           : "Input/Data/DataEgamma*.root",
  "data_Muons"            : "Input/Data/DataMuons*.root",
}