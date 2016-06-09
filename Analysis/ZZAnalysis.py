import ROOT
import itertools 

import Analysis
import AnalysisHelpers as AH
import Constants

#======================================================================
        
class ZZAnalysis(Analysis.Analysis):
  """Analysis searching for the pair production of two Z bosons decaying to leptons."""
  def __init__(self, store):
      super(ZZAnalysis, self).__init__(store)

  
  def initialize(self):
      self.invMass1          =  self.addHistogram("invMass1",          ROOT.TH1D("invMass1",     "Invariant Mass of the Z boson 1;M_{Z1} [GeV]; Events", 30, 60,120))
      self.invMass2          =  self.addHistogram("invMass2",          ROOT.TH1D("invMass2",     "Invariant Mass of the Z boson 2;M_{Z2} [GeV]; Events", 30, 60,120))

      self.hist_leptn       =  self.addStandardHistogram("lep_n")
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
      

      # retrieve Leptons  
      goodLeptons = AH.selectAndSortContainer(self.Store.getLeptons(), isGoodLepton, lambda p: p.pt())
      if not len(goodLeptons) >= 4: return False
      if not goodLeptons[0].pt() > 25: return False

      # find ZZ Candidate
      candidate = self.ZZCandidate(goodLeptons)
      if candidate is None: return False;

      # test ZZ Candidate
      if self.DoubleZWindow(candidate) > 30: return False;
      self.countEvent("all passed", weight)
 
      # vertex histograms
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)

      # missing transverse momentum histograms
      etmiss    = self.Store.getEtMiss()
      self.hist_etmiss.Fill(etmiss.et(),weight)
      
      # ZZ system histograms
      self.invMass1.Fill((candidate[0].tlv() + candidate[1].tlv()).M(), weight)
      self.invMass2.Fill((candidate[2].tlv() + candidate[3].tlv()).M(), weight)
      
      # lepton histograms
      self.hist_leptn.Fill(len(goodLeptons), weight)
      [self.hist_leptpt.Fill(lep.pt(), weight) for lep in goodLeptons]
      [self.hist_lepteta.Fill(lep.eta(), weight) for lep in goodLeptons]
      [self.hist_leptE.Fill(lep.e(), weight) for lep in goodLeptons]
      [self.hist_leptphi.Fill(lep.phi(), weight) for lep in goodLeptons]
      [self.hist_leptch.Fill(lep.charge(), weight) for lep in goodLeptons]
      [self.hist_leptID.Fill(lep.pdgId(), weight) for lep in goodLeptons]
      [self.hist_leptptc.Fill(lep.isoptconerel30(), weight) for lep in goodLeptons]
      [self.hist_leptetc.Fill(lep.isoetconerel20(), weight) for lep in goodLeptons]
      [self.hist_lepz0.Fill(lep.z0(), weight) for lep in goodLeptons]
      [self.hist_lepd0.Fill(lep.d0(), weight) for lep in goodLeptons]
      return True
  
  def finalize(self):
      pass
    
  def ZWindow(self, lep1, lep2):
      return abs((lep1.tlv()+lep2.tlv()).M() - Constants.Z_Mass)
    
  def DoubleZWindow(self, candidate):
      return self.ZWindow(candidate[0], candidate[1]) + self.ZWindow(candidate[2], candidate[3])

  def ZZCandidate(self, leptons):
      def isValidCandidate(lep1, lep2):
          if lep1.charge()*lep2.charge() > 0: return False
          if abs(lep1.pdgId()) != abs(lep2.pdgId()): return False
          return True
    
      bestCandidate = None
      for p in itertools.permutations(leptons, 4):
         if not isValidCandidate(p[0], p[1]): continue
         if not isValidCandidate(p[2], p[3]): continue 
         if bestCandidate is None:
             bestCandidate = p            
         if self.DoubleZWindow(p) < self.DoubleZWindow(bestCandidate):
             bestCandidate = p
      return bestCandidate

  
def isGoodLepton(Lepton):
    if not Lepton.pt() > 10: return False
    if not Lepton.isoetconerel20() < 0.15: return False
    if not Lepton.isoptconerel30() < 0.15: return False
    return True;
  
