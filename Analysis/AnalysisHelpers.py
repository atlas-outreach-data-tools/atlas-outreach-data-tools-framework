import math

"""These helper functions implement three commonly used functionalities:
The Object Selection Helpers represent standard object selections that serve as a starting point for
self defined object selection strategies.
The selectAndSortContainer function can be used to do selecting and sorting in a one liner.
The StandardEventCuts function implements three standard cuts used in essentially all analyses.
"""


# Object Selection Helpers
def isGoodLepton(Lepton):
    if (abs(Lepton.pdgId()) == 11 and isGoodElectron(Lepton)): return True;
    if (abs(Lepton.pdgId()) == 13 and isGoodMuon(Lepton)): return True;
    return False;
    
def isGoodElectron(Lepton):
    if not Lepton.isTight(): return False
    if not Lepton.pt() > 25: return False
    if not Lepton.isoetconerel20() < 0.15: return False
    if not Lepton.isoptconerel30() < 0.15: return False
    return True;
    
def isGoodMuon(Lepton):
    if not Lepton.isTight(): return False
    if not Lepton.pt() > 25: return False
    if not Lepton.isoetconerel20() < 0.15: return False
    if not Lepton.isoptconerel30() < 0.15: return False
    return True;
    
def isGoodJet(jet):
    if jet.pt() < 25: return False
    if abs(jet.eta() > 2.5): return False
    if jet.pt() < 50 and abs(jet.eta() < 2.4) and jet.jvf() < 0.5: return False
    return True

# Utility function
def selectAndSortContainer(container, selectingFunction, sortingFunction):
    selectedContainer = [particle for particle in container if selectingFunction(particle)]
    return sorted(selectedContainer, key=sortingFunction, reverse=True)

# Event Selection Helpers
def StandardEventCuts(eventinfo):
    if not (eventinfo.triggeredByElectron() or eventinfo.triggeredByMuon()): return False
    if not eventinfo.passGRL(): return False
    if not eventinfo.hasGoodVertex(): return False
    return True;
    
    
# Variable Definitions:
def WTransverseMass(lepton, etmiss):
    return math.sqrt(2*lepton.pt()*etmiss.et()*(1-math.cos(lepton.tlv().DeltaPhi(etmiss.tlv()))));