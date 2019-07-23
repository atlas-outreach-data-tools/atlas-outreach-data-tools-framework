import ROOT
from array import array

#======================================================================

class TupleReader(object):
    """ This class implements the rules that govern the readout of the ROOT tuples and and provide a caching facility.
    Caching improves the readout by eliminating the need for branch address lookup each time the variable is accessed.
    """

    def __init__(self):
        super(TupleReader, self).__init__()
        self.Tree = None
        
    def initializeTuple(self,tree):
        """The initial setup of the caching is done here. Branches in the TTree may be deactivated using SetBranchStatus to
        increase readout speed. Only necessary branches are activated and their contents are bound to datamembers of the
        tuple reader.
        """
        self.Tree = tree
        self.Tree.SetBranchStatus("*",0)
        
        #EventInfo 
        self.eventNumber      = self.activate("i", "eventNumber",            1)
        self.runNumber        = self.activate("i", "runNumber" ,             1)
        self.mcWeight         = self.activate("f", "mcWeight",               1)
                                                                             
        self.passGRL          = self.activate("b", "passGRL" ,               1)
        self.hasGoodVertex    = self.activate("b", "hasGoodVertex",          1)
        self.trigE            = self.activate("b", "trigE",                  1)
        self.trigM            = self.activate("b", "trigM",                  1)
                                                                             
        self.SF_Pileup        = self.activate("f", "scaleFactor_PILEUP",     1)
        self.SF_Ele           = self.activate("f", "scaleFactor_ELE",        1)
        self.SF_Mu            = self.activate("f", "scaleFactor_MUON",       1)
        self.SF_BTag          = self.activate("f", "scaleFactor_BTAG",       1)
        self.SF_Trigger       = self.activate("f", "scaleFactor_TRIGGER",    1)
        self.SF_JVF           = self.activate("f", "scaleFactor_JVFSF",      1)
        self.SF_ZVertex       = self.activate("f", "scaleFactor_ZVERTEX",    1)
        self.vxp_z            = self.activate("f", "vxp_z",                  1)
        self.pvxp_n           = self.activate("i", "pvxp_n",                 1)

        self.EventInfo = EventInfo(self)
        

        #LeptonInfo
        max_Lep = self.GetMaximum("lep_n")
        max_Lep = min(abs(max_Lep), 20)
        self.Lep_n         = self.activate("i", "lep_n",                    1)
        self.Lep_pt        = self.activate("f", "lep_pt",                   max_Lep) 
        self.Lep_eta       = self.activate("f", "lep_eta",                  max_Lep) 
        self.Lep_phi       = self.activate("f", "lep_phi",                  max_Lep)
        self.Lep_e         = self.activate("f", "lep_E",                    max_Lep)
        self.Lep_pdgid     = self.activate("i", "lep_type",                 max_Lep)
        self.Lep_charge    = self.activate("f", "lep_charge",               max_Lep)
        self.Lep_ptcone30  = self.activate("f", "lep_ptcone30",             max_Lep)
        self.Lep_etcone20  = self.activate("f", "lep_etcone20",             max_Lep)                    
        self.Lep_d0        = self.activate("f", "lep_trackd0pvunbiased",    max_Lep)
        self.Lep_d0Sig     = self.activate("f", "lep_tracksigd0pvunbiased", max_Lep)
        self.Lep_trigMatch = self.activate("b", "lep_trigMatched",          max_Lep)
        self.Lep_z0        = self.activate("f", "lep_z0",                   max_Lep)
        self.Lep_flag      = self.activate("i", "lep_flag",                 max_Lep)

        self.Leptons = [Lepton(i,self) for i in range(0,max_Lep)]

         
        #JetInfo
        max_Jet = self.GetMaximum("alljet_n")
        max_Jet = min(abs(max_Jet), 20)
        self.Jet_n        = self.activate("i", "alljet_n",     1)
        self.Jet_pt       = self.activate("f", "jet_pt",       max_Jet)
        self.Jet_eta      = self.activate("f", "jet_eta",      max_Jet)
        self.Jet_e        = self.activate("f", "jet_E",        max_Jet)
        ## self.Jet_flag     = self.activate("i", "jet_flag",     max_Jet)
        self.Jet_phi      = self.activate("f", "jet_phi",      max_Jet)
        self.Jet_mass     = self.activate("f", "jet_m",        max_Jet)
        self.Jet_jvf      = self.activate("f", "jet_jvf",      max_Jet)
        self.Jet_mv1      = self.activate("f", "jet_MV1",      max_Jet)
         
        self.Jets = [Jet(i, self) for i in range(0,max_Jet)]
         
        #EtMissInfo
        self.Met_et   = self.activate( "f", "met_et",  1)
        self.Met_phi  = self.activate( "f", "met_phi", 1)
        
        self.EtMiss = EtMiss(self)
                
                
    def activate(self, vartype,  branchname, maxlength):
        variable = array(vartype,[0]*maxlength)
        self.Tree.SetBranchStatus(branchname,1)
        self.Tree.SetBranchAddress( branchname, variable)   
        return variable
    
    # Used for a quick scan to get the largest value encountered in the tuple
    def GetMaximum(self,branchname):
        self.Tree.SetBranchStatus(branchname,1)
        return int(self.Tree.GetMaximum(branchname))
    
    # Functions to retrieve object collections (Tuplereader is called Store in the analysis code)
    def getEtMiss(self):
        return self.EtMiss
        
    def getEventInfo(self):
        return self.EventInfo
        
    def getLeptons(self):
        return self.Leptons[:self.Lep_n[0]]
    
    def getJets(self):
        return self.Jets[:self.Jet_n[0]]

#===========================================================

class EtMiss(object):
    """Missing Transverse Momentum Object.
    Missing Transverse Momentum has only two variables, its magnitude (et) and its azimuthal angle (phi).
    It is used as a proxy for all particles that escaped detection (neutrinos and the likes).
    """
    def __init__(self, branches):
        super(EtMiss, self).__init__()
        self.Branches = branches
        self._tlv     = None
    
    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.et() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.et(), 0, self.phi(), self.et())
      return self._tlv
    
    def et(self):
      return self.Branches.Met_et[0]*0.001

    def phi(self):
      return self.Branches.Met_phi[0]

    def __str__(self):
        return "MET: et: %4.3f  phi: %4.3f" % (self.et(), self.phi())

#===========================================================

class EventInfo(object):
    """EventInfo class holding information about the event
    Information that can be accessed may either be metadata about the event (eventNumber, runNumber),
    information regarding the weight an event has (eventWeight, scalefactor, mcWeight, primaryVertexPosition) or
    information that may be used for selection purposes (passGRL, hasGoodVertex, numberofVertices, triggeredByElectron, 
    triggeredByMuon)
    """
    def __init__(self, branches):
        super(EventInfo, self).__init__()
        self.Branches = branches

    def eventNumber(self):
      return self.Branches.eventNumber[0]

    def runNumber(self):
      return self.Branches.runNumber[0]

    def eventWeight(self):
      return self.Branches.mcWeight[0]*self.Branches.SF_Pileup[0]*self.Branches.SF_ZVertex[0]

    def scalefactor(self):
      return self.Branches.SF_Ele[0]*self.Branches.SF_Mu[0]*self.Branches.SF_Trigger[0]    

    def passGRL(self):
      return self.Branches.passGRL[0]
     
    def mcWeight(self):
      return self.Branches.mcWeight[0]
    
    def hasGoodVertex(self):
      return self.Branches.hasGoodVertex[0]
    
    def numberOfVertices(self):
      return self.Branches.pvxp_n[0]

    def primaryVertexPosition(self):
      return self.Branches.vxp_z[0]

    def triggeredByElectron(self):
      return self.Branches.trigE[0]

    def triggeredByMuon(self):
      return self.Branches.trigM[0]

    def __str__(self):
        return "EventInfo: run: %i  event: %i  eventweight: %4.2f" % (self.runNumber(), self.eventNumber(), self.eventWeight())


#===========================================================

class Lepton(object):
    """Leptons may either be electrons or muons (checkable via the pdgId, 11 is for electrons, 13 for muons, 
    negative values signify anti-particles) Accessible information includes the kinematics (pt, eta, phi, e),
    the quality of the reconstruction result (isTight), and auxillary information
    (pdgId, charge, isolation variables like isoptcone30, d0, z0...).
    """
    def __init__(self, idNr, branches):
        super(Lepton, self).__init__()
        self.Branches = branches
        self.idNr = idNr
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv
      
    def pt(self):
      return self.Branches.Lep_pt[self.idNr]*0.001

    def eta(self):
      return self.Branches.Lep_eta[self.idNr]

    def phi(self):
      return self.Branches.Lep_phi[self.idNr]

    def e(self):
      return self.Branches.Lep_e[self.idNr]*0.001

    def isTight(self):
      return bool(self.Branches.Lep_flag[self.idNr] & 512)

    def pdgId(self):
      return self.Branches.Lep_pdgid[self.idNr]
 
    def charge(self):
      return self.Branches.Lep_charge[self.idNr]
    
    def isoptcone30(self):
      return self.Branches.Lep_ptcone30[self.idNr]                

    def isoetcone20(self):
      return self.Branches.Lep_etcone20[self.idNr]                

    def isoptconerel30(self):
      return self.Branches.Lep_ptcone30[self.idNr]/self.Branches.Lep_pt[self.idNr]                

    def isoetconerel20(self):
      return self.Branches.Lep_etcone20[self.idNr]/self.Branches.Lep_pt[self.idNr]                

    def d0(self):
      return self.Branches.Lep_d0[self.idNr]
    
    def d0Significance(self):
      return self.Branches.Lep_d0Sig[self.idNr]
    
    def isTriggerMatched(self):
      return self.Branches.Lep_trigMatch[self.idNr]

    def z0(self):
      return self.Branches.Lep_z0[self.idNr]
         
    def __str__(self):
        return "Lepton %d: pdgId: %d  pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pdgId(), self.pt(), self.eta(), self.phi())
        
#===========================================================

class Jet(object):
    """Jet objects have accessors regarding their kinematic information (pt, eta, phi, e), their properties (m), and
    auxillary information (mv1, jvf). Truth information regarding the flavour of the quark they com from (truepdgid)
    and whether they were matched to a true jet (isTrueJet) is available.
    """
    def __init__(self, idNr, branches):
        super(Jet, self).__init__()
        self.idNr = idNr
        self.Branches = branches
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv
    
    def pt(self):
      return self.Branches.Jet_pt[self.idNr]*0.001
    
    def eta(self):
      return self.Branches.Jet_eta[self.idNr]
    
    def phi(self):
      return self.Branches.Jet_phi[self.idNr]
    
    def e(self):
      return self.Branches.Jet_e[self.idNr]*0.001
    
    def m(self):
      return self.Branches.Jet_mass[self.idNr]

    def mv1(self):
      return self.Branches.Jet_mv1[self.idNr]
      
    def jvf(self):
      return self.Branches.Jet_jvf[self.idNr]

    def truepdgid(self):
      return self.Branches.Jet_trueflav[self.idNr]

    def isTrueJet(self):
      return bool(self.Branches.Jet_truthMatched[self.idNr])
         
    def __str__(self):
        return "Jet %d: pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pt(), self.eta(), self.phi())
