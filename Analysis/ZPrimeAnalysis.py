import ROOT
import math

import Analysis
import AnalysisHelpers as AH

#======================================================================
        
class ZPrimeAnalysis(Analysis.Analysis):
  """Analysis searching for an exotic Z' particle in a semileptonic top pair topology."""
  def __init__(self, store):
      super(ZPrimeAnalysis, self).__init__(store)
  
  def initialize(self):
      self.WtMass            = self.addStandardHistogram("WtMass")

      self.hist_leptpt      =  self.addStandardHistogram("lep_pt")
      self.hist_lepteta     =  self.addStandardHistogram("lep_eta")
      self.hist_leptE       =  self.addStandardHistogram("lep_E")
      self.hist_leptphi     =  self.addStandardHistogram("lep_phi")
      self.hist_leptch      =  self.addStandardHistogram("lep_charge")
      self.hist_leptID      =  self.addStandardHistogram("lep_type")
      self.hist_leptptc     =  self.addStandardHistogram("lep_ptconerel30")
      self.hist_leptetc     =  self.addStandardHistogram("lep_etconerel20")
      self.hist_lepz0       =  self.addStandardHistogram("lep_z0")
      self.hist_lepd0       =  self.addStandardHistogram("lep_d0")

      self.hist_njets       =  self.addStandardHistogram("n_jets")       
      self.hist_jetspt      =  self.addStandardHistogram("jet_pt")       
      self.hist_jetm        =  self.addStandardHistogram("jet_m")        
      self.hist_jetJVF      =  self.addStandardHistogram("jet_jvf")      
      self.hist_jeteta      =  self.addStandardHistogram("jet_eta")      
      self.hist_jetmv1      =  self.addStandardHistogram("jet_MV1")      

      self.hist_etmiss      = self.addStandardHistogram("etmiss")
      self.hist_vxp_z       = self.addStandardHistogram("vxp_z")
      self.hist_pvxp_n      = self.addStandardHistogram("pvxp_n")
  
  def analyze(self):
      # retrieving objects
      eventinfo = self.Store.getEventInfo()
      weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1
      self.countEvent("no cut", weight)
      
      # apply standard event based selection
      if not AH.StandardEventCuts(eventinfo): return False
      self.countEvent("EventCuts", weight)

      # Lepton Requirements
      goodLeptons = AH.selectAndSortContainer(self.Store.getLeptons(), AH.isGoodLepton, lambda p: p.pt())
      if not (len(goodLeptons) == 1): return False
      self.countEvent("1 high pt Leptons", weight)


      etmiss = self.Store.getEtMiss()
      if not etmiss.et() > 30.: return False
      self.countEvent("etmiss", weight)


      goodJets = AH.selectAndSortContainer(self.Store.getJets(), AH.isGoodJet, lambda p: p.pt())
      if not len(goodJets) >= 4: return False
      self.countEvent("4 jets", weight)

      if not sum([1 for jet in goodJets if jet.mv1() >= 0.7892]) >= 1: return False
      self.countEvent("btag", weight)

      lepton = goodLeptons[0]
      mTW = AH.WTransverseMass(lepton, etmiss)
      if not mTW > 30: return False;
      if not mTW + etmiss.et() > 60: return False
      self.countEvent("masses", weight)
      
      # vertex histograms
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)

      # W boson histogram
      self.WtMass.Fill(mTW, weight)

      # missing transverse momentum histogram
      self.hist_etmiss.Fill(etmiss.et(), weight)

      # lepton histograms
      self.hist_leptpt.Fill(lepton.pt(), weight)
      self.hist_lepteta.Fill(lepton.eta(), weight)
      self.hist_leptE.Fill(lepton.e(), weight)
      self.hist_leptphi.Fill(lepton.phi(), weight)
      self.hist_leptch.Fill(lepton.charge(), weight)
      self.hist_leptID.Fill(lepton.pdgId(), weight)
      self.hist_leptptc.Fill(lepton.isoptconerel30(), weight)
      self.hist_leptetc.Fill(lepton.isoetconerel20(), weight)
      self.hist_lepz0.Fill(lepton.z0(), weight)
      self.hist_lepd0.Fill(lepton.d0(), weight)

      # jet histograms
      self.hist_njets.Fill(len(goodJets), weight)
      [self.hist_jetm.Fill(jet.m(), weight) for jet in goodJets]
      [self.hist_jetspt.Fill(jet.pt(), weight) for jet in goodJets]
      [self.hist_jetJVF.Fill(jet.jvf(), weight) for jet in goodJets]
      [self.hist_jeteta.Fill(jet.eta(), weight) for jet in goodJets]
      [self.hist_jetmv1.Fill(jet.mv1(), weight) for jet in goodJets]
      return True
  
  def finalize(self):
      pass

