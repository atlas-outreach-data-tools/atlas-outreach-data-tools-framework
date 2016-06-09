import ROOT
import math
import Analysis
import AnalysisHelpers as AH
import Constants

#======================================================================

class HWWAnalysis(Analysis.Analysis):
  """HWWAnalysis implementing an abridged version of the analysis carried out by ATLAS.
  The code assumes that both W bosons decay to leptons (lvlv finalstate).
  Only the 0-Jet bin is considered.
  """
  def __init__(self, store):
      super(HWWAnalysis, self).__init__(store)

  def initialize(self):
      self.hist_vismass         = self.addHistogram("vismass",            ROOT.TH1D("vismass", "Visible Mass; M^{vis}_{ll};Events", 20, 0, 200))
      self.hist_ptLL            = self.addHistogram("ptll",               ROOT.TH1D("ptll", "Tranvsere Momentum of Dilepton System; p_{T,ll};Events", 20,0,200))
      self.hist_deltaPhiLL      = self.addHistogram("deltaphill",         ROOT.TH1D("deltaphill", "Azimuthal Opening Angle between Leptons; #|Delta#phi_{ll}|;Events", 16, 0, 1.6))

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

      jets = AH.selectAndSortContainer(self.Store.getJets(), AH.isGoodJet, lambda p: p.pt())
      if not len(jets) == 0: return False
      self.countEvent("Jets", weight)

      etmiss    = self.Store.getEtMiss() 

      # background suppresion
      combTLV = leadLepton.tlv() + trailLepton.tlv() 
      mll = combTLV.M()
      if not leadLepton.charge()*trailLepton.charge() < 0: return False
      if (abs(leadLepton.pdgId()) == abs(trailLepton.pdgId())):
          if not mll > 12: return False
          if not abs(mll - Constants.Z_Mass) > 15: return False
          if not etmiss.et() > 40: return False
      else:
          if not mll > 10: return False
          if not etmiss.et() > 20: return False

      if not combTLV.Pt() > 30: return False
      if not combTLV.DeltaPhi(etmiss.tlv()) > math.pi/2.0: return False

      # Higgs to WW topology
      if not combTLV.M() < 55: return False
      if not leadLepton.tlv().DeltaPhi(trailLepton.tlv()) < 1.8: return False

      # Missing Et histograms
      self.hist_etmiss.Fill(etmiss.et(),weight)

      # Eventwise quantity histograms
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)
      
      self.hist_vismass.Fill(combTLV.M(), weight)
      self.hist_ptLL.Fill(combTLV.Pt(), weight)
      self.hist_deltaPhiLL.Fill(abs(leadLepton.tlv().DeltaPhi(trailLepton.tlv())), weight)

      # Leading Lepton histograms
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

      # Trailing Lepton histograms
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
      return True

  def finalize(self):
      pass