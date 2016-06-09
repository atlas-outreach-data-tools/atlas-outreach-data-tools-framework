import ROOT

import Analysis
import AnalysisHelpers as AH
import Constants

#======================================================================

class ZAnalysis(Analysis.Analysis):
  """Analysis searching for events where Z bosons decay to two leptons of same flavour and opposite charge.
  """
  def __init__(self, store):
    super(ZAnalysis, self).__init__(store)
  
  def initialize(self):
      self.invMass              =  self.addStandardHistogram("invMass")

      self.hist_leptn           =  self.addStandardHistogram("lep_n")

      self.hist_leadleptpt      =  self.addStandardHistogram("leadlep_pt")
      self.hist_leadlepteta     =  self.addStandardHistogram("leadlep_eta")
      self.hist_leadleptE       =  self.addStandardHistogram("leadlep_E")
      self.hist_leadleptphi     =  self.addStandardHistogram("leadlep_phi")
      self.hist_leadleptch      =  self.addStandardHistogram("leadlep_charge")
      self.hist_leadleptID      =  self.addStandardHistogram("leadlep_type")
      self.hist_leadleptptc     =  self.addStandardHistogram("leadlep_ptconerel30")
      self.hist_leadleptetc     =  self.addStandardHistogram("leadlep_etconerel20")
      self.hist_leadlepz0       =  self.addStandardHistogram("leadlep_z0")
      self.hist_leadlepd0       =  self.addStandardHistogram("leadlep_d0")

      self.hist_trailleptpt     =  self.addStandardHistogram("traillep_pt")
      self.hist_traillepteta    =  self.addStandardHistogram("traillep_eta")
      self.hist_trailleptE      =  self.addStandardHistogram("traillep_E")
      self.hist_trailleptphi    =  self.addStandardHistogram("traillep_phi")
      self.hist_trailleptch     =  self.addStandardHistogram("traillep_charge")
      self.hist_trailleptID     =  self.addStandardHistogram("traillep_type")
      self.hist_trailleptptc    =  self.addStandardHistogram("traillep_ptconerel30")
      self.hist_trailleptetc    =  self.addStandardHistogram("traillep_etconerel20")
      self.hist_traillepz0      =  self.addStandardHistogram("traillep_z0")
      self.hist_traillepd0      =  self.addStandardHistogram("traillep_d0")

      self.hist_njets           =  self.addStandardHistogram("n_jets")       
      self.hist_jetspt          =  self.addStandardHistogram("jet_pt")       
      self.hist_jetm            =  self.addStandardHistogram("jet_m")        
      self.hist_jetJVF          =  self.addStandardHistogram("jet_jvf")      
      self.hist_jeteta          =  self.addStandardHistogram("jet_eta")      
      self.hist_jetmv1          =  self.addStandardHistogram("jet_MV1")      

      self.hist_etmiss          = self.addStandardHistogram("etmiss")
      self.hist_vxp_z           = self.addStandardHistogram("vxp_z")
      self.hist_pvxp_n          = self.addStandardHistogram("pvxp_n")
  
  def analyze(self):
      # retrieving objects
      eventinfo = self.Store.getEventInfo()
      weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1
      self.countEvent("no cut", weight)
      
      # apply standard event based selection
      if not AH.StandardEventCuts(eventinfo): return False
      self.countEvent("EventCuts", weight)

      # Lepton Requirements
      GoodLeptons = AH.selectAndSortContainer(self.Store.getLeptons(), AH.isGoodLepton, lambda p: p.pt())
      if not (len(GoodLeptons) == 2): return False
      self.countEvent("2 high pt Leptons", weight)

      leadLepton  = GoodLeptons[0]
      trailLepton = GoodLeptons[1]

      # test Z candidate
      if not (leadLepton.charge() * trailLepton.charge() < 0): return False
      if not (abs(leadLepton.pdgId()) == abs(trailLepton.pdgId())): return False
      if not (abs((leadLepton.tlv() + trailLepton.tlv()).M() - Constants.Z_Mass) < 20): return False

      # Vertex Histograms
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)

      # Z boson Histograms
      self.invMass.Fill((leadLepton.tlv() + trailLepton.tlv()).M(), weight)

      # Missing Et Histograms
      etmiss    = self.Store.getEtMiss()
      self.hist_etmiss.Fill(etmiss.et(),weight)

      self.hist_leptn.Fill(len(GoodLeptons), weight)

      # Leading Lepton Histograms
      self.hist_leadleptpt.Fill(leadLepton.pt(), weight)
      self.hist_leadlepteta.Fill(leadLepton.eta(), weight)
      self.hist_leadleptE.Fill(leadLepton.e(), weight)
      self.hist_leadleptphi.Fill(leadLepton.phi(), weight)
      self.hist_leadleptch.Fill(leadLepton.charge(), weight)
      self.hist_leadleptID.Fill(leadLepton.pdgId(), weight)
      self.hist_leadleptptc.Fill(leadLepton.isoptconerel30(), weight)
      self.hist_leadleptetc.Fill(leadLepton.isoetconerel20(), weight)
      self.hist_leadlepz0.Fill(leadLepton.z0(), weight)
      self.hist_leadlepd0.Fill(leadLepton.d0(), weight)

      # Trailing Lepton Histograms
      self.hist_trailleptpt.Fill(trailLepton.pt(), weight)
      self.hist_traillepteta.Fill(trailLepton.eta(), weight)
      self.hist_trailleptE.Fill(trailLepton.e(), weight)
      self.hist_trailleptphi.Fill(trailLepton.phi(), weight)
      self.hist_trailleptch.Fill(trailLepton.charge(), weight)
      self.hist_trailleptID.Fill(trailLepton.pdgId(), weight)
      self.hist_trailleptptc.Fill(trailLepton.isoptconerel30(), weight)
      self.hist_trailleptetc.Fill(trailLepton.isoetconerel20(), weight)
      self.hist_traillepz0.Fill(trailLepton.z0(), weight)
      self.hist_traillepd0.Fill(trailLepton.d0(), weight)

      # Jet Histograms
      jets = AH.selectAndSortContainer(self.Store.getJets(), AH.isGoodJet, lambda p: p.pt())
      self.hist_njets.Fill(len(jets), weight)
      [self.hist_jetm.Fill(jet.m(), weight) for jet in jets]
      [self.hist_jetspt.Fill(jet.pt(), weight) for jet in jets]
      [self.hist_jetJVF.Fill(jet.jvf(), weight) for jet in jets]
      [self.hist_jeteta.Fill(jet.eta(), weight) for jet in jets]
      [self.hist_jetmv1.Fill(jet.mv1(), weight) for jet in jets]
      
      return True
  
  def finalize(self):
      pass
