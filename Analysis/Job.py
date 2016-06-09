import ROOT
import glob
import importlib
import sys
import time

import JobStatistics

#======================================================================

class Job(object):
    """This class is a carrier class for a given analysis. It takes care of the technical details like
    file writing, setting up the input tree and providing statistics about the status of the analysis.    
    """
    def __init__(self, processName, configuration, inputLocation):
        super(Job, self).__init__()
        #Configurables
        self.Name       = processName
        self.Configuration = configuration
        self.MaxEvents     = configuration["MaxEvents"]
        self.InputFiles    = glob.glob(inputLocation)

        # Outputs
        self.OutputFileLocation = configuration["OutputDirectory"] + processName
        self.OutputFile = None

        # Classes - InputTree and Analysis have to be created later otherwise parallel running does not work
        self.InputTree     = None
        self.Analysis      = None
        self.JobStatistics = JobStatistics.JobStatistics(self.Configuration["MaxEvents"], self.Configuration["Batch"])

    #Setup functions
    def setupTree(self):
      tree = ROOT.TChain("mini")
      for filename in self.InputFiles:
        self.log("Adding file: " + filename)
        tree.Add(filename)
      return tree
                    
    def createAnalysis(self, analysisName):
        analysisName = self.Configuration["Analysis"]
        importedAnalysisModule = importlib.import_module("Analysis." + analysisName)
        analysis = getattr(importedAnalysisModule, analysisName)(self.Name)
        analysis.Store.initializeTuple(self.InputTree)
        analysis.setIsData("data" in self.Name.lower())
        return analysis
    
    #Execution functions                    
    def run(self):
      self.initialize()
      self.execute()
      self.finalize()
      
    def initialize(self):
      self.log("Intialization phase")
      self.JobStatistics.resetTimer()
      self.OutputFile = ROOT.TFile.Open(self.OutputFileLocation + ".root","RECREATE")
      self.InputTree = self.setupTree()
      self.Analysis  = self.createAnalysis(self.Configuration["Analysis"])
      self.determineMaxEvents()
      self.Analysis.doInitialization()
        
    def execute(self):
      self.log("Now looping over %d events" % self.MaxEvents)
      for n in xrange(self.MaxEvents):
        self.JobStatistics.updateStatus(n)
        self.InputTree.GetEntry(n)
        self.Analysis.doAnalysis()
            
    def finalize(self):
      self.JobStatistics.updateStatus(self.MaxEvents, True)
      if not self.Configuration["Batch"]:
          print ""
      self.Analysis.doFinalization()
      self.OutputFile.Close()
      self.log("finished successfully. Total time: %4.0fs" % self.JobStatistics.elapsedTime())


    # Helper functions
    def determineMaxEvents(self):
      nentries = self.InputTree.GetEntries()
      if nentries==0:
        self.log("Empty files! Abort!")
        sys.exit(1)
      
      if self.MaxEvents > nentries:
        self.MaxEvents = nentries
      
      self.MaxEvents = int(self.MaxEvents*self.Configuration["Fraction"]) 
      self.JobStatistics.setMaxEvents(self.MaxEvents)

    def log(self, message):
      print time.ctime() + " Job " + self.Name + ": " + message
              
        

