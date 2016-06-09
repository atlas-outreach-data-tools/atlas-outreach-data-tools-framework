import ROOT
import itertools 

import Analysis
import AnalysisHelpers as AH
import Constants

#======================================================================
        
class WZAnalysis(Analysis.Analysis):
  """Analysis searching for the pair production of WZ with both boson decaying to leptons"""
  def __init__(self, store):
      super(WZAnalysis, self).__init__(store)

  
  def initialize(self):
      self.invMass          =  self.addStandardHistogram("invMass")
      self.WtMass           =  self.addStandardHistogram("WtMass")
      
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


  def ZWindow(self, lep1, lep2):
      return abs((lep1.tlv()+lep2.tlv()).M() - Constants.Z_Mass)
    
  def TestWZCandidate(self, candidate):
      return self.ZWindow(candidate[0], candidate[1])

  def WZCandidate(self, leptons):
      def isValidCandidate(lep1, lep2):
          if lep1.charge()*lep2.charge() > 0: return False
          if abs(lep1.pdgId()) != abs(lep2.pdgId()): return False
          return True
    
      bestCandidate = None
      for p in itertools.permutations(leptons, 3):
         if not isValidCandidate(p[0], p[1]): continue
         if bestCandidate is None:
             bestCandidate = p            
         if self.TestWZCandidate(p) < self.TestWZCandidate(bestCandidate):
             bestCandidate = p
      return bestCandidate
    
  def analyze(self):
      # retrieving objects
      eventinfo = self.Store.getEventInfo()
      weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1
            
      # apply standard event based selection
      if not AH.StandardEventCuts(eventinfo): return False
      self.countEvent("EventCuts", weight)
       
      # Lepton Requirements
      goodLeptons = AH.selectAndSortContainer(self.Store.getLeptons(), AH.isGoodLepton, lambda p: p.pt())
      if not (len(goodLeptons) == 3): return False
      self.countEvent("3 high pt Leptons", weight)

      # find candidate for WZ system
      candidate = self.WZCandidate(goodLeptons)
      if candidate is None: return False;

      z1Lepton = candidate[0]
      z2Lepton = candidate[1]
      wLepton  = candidate[2]
      etmiss = self.Store.getEtMiss()

      # test candidate for WZ system
      if not self.ZWindow(z1Lepton, z2Lepton) < 10: return False;
      if not AH.WTransverseMass(wLepton, etmiss) > 30: return False;

      # histograms for missing et
      self.hist_etmiss.Fill(etmiss.et(),weight)  
      
      # vertex histograms
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)
      
      # WZ system histograms
      self.invMass.Fill((z1Lepton.tlv() + z2Lepton.tlv()).M(), weight)
      self.WtMass.Fill(AH.WTransverseMass(wLepton, etmiss), weight)

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
