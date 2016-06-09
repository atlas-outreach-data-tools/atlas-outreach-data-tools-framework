import argparse
import sys
import os
import glob
import ROOT
import importlib
import Analysis.Job as Job
import Analysis.Disclaimer as DC
from multiprocessing import Pool 

def buildProcessingDict(configuration, samples):
    if samples == "": 
        return configuration.Processes
    processingDict = {}
    listOfSamples = [substring.strip() for substring in samples.split(',')]
    for sample in listOfSamples:
        try:
            processingDict[sample] = configuration.Processes[sample]
        except :
            print "Name of Sample %s not recognized. Sample was not added to processing list!" % sample
    return processingDict

def checkAnalysis(configuration, analysisOption):
    analysisName = analysisOption if analysisOption != "" else configuration.Job["Analysis"]
    try:
        importedAnalysisModule = importlib.import_module("Analysis." + analysisName)
        configuration.Job["Analysis"] = analysisName
    except ImportError:
        print "Error when trying to read the analysis code for %s. Please check name validity" % analysisName
        sys.exit(1)

def BuildJob(configuration, processName, fileLocation):
    job = Job.Job(processName, configuration, fileLocation )
    return job


def SortJobsBySize(jobs):  
    def jobSize(job):
        return sum([os.lstat(f).st_size for f in job.InputFiles])
    return sorted(jobs, key=jobSize, reverse=True)

def RunJob(job):
    job.run()

 
#======================================================================
def main( argv ):
    """
    Main function to be executed when starting the code.
    """
    DC.printDisclaimer()
    
    # global configuration
    parser = argparse.ArgumentParser( description = 'Analysis Tool using XMLs' )
    parser.add_argument('-n', '--nWorkers',   default=4,                                 type=int,   help='number of workers' )  
    parser.add_argument('-p', '--parallel',   default=False,   action='store_const',     const=True, help='enables running in parallel')
    parser.add_argument('-c', '--configfile', default="Configurations/Configuration.py", type=str,   help='files to be analysed')
    parser.add_argument('-a', '--analysis',   default=""                               , type=str,   help='overrides the analysis specified in configuration file')
    parser.add_argument('-s', '--samples',    default=""                               , type=str,   help='string with comma separated list of samples to analyse')
    parser.add_argument('-o', '--output',     default=""                               , type=str,   help='name of the output directory')
    args = parser.parse_args()
    
    configModuleName = args.configfile.replace("/", ".").replace(".py","")
    configuration = importlib.import_module(configModuleName)
  
    configuration.Job["OutputDirectory"] = args.output + "/" if args.output != "" else configuration.Job["OutputDirectory"]
    if not os.path.exists(configuration.Job["OutputDirectory"]):
        os.makedirs(configuration.Job["OutputDirectory"])

    checkAnalysis(configuration, args.analysis)
    processingDict = buildProcessingDict(configuration, args.samples)

    if (args.parallel):
        configuration.Job["Batch"] = True
        jobs = [BuildJob(configuration.Job, processName, fileLocation) for processName, fileLocation in processingDict.items()]
        jobs = SortJobsBySize(jobs)
        pool = Pool(processes=args.nWorkers)              # start with n worker processes
        pool.map(RunJob, jobs, chunksize=1)

    else:
        for processName, fileLocation in processingDict.items():
            RunJob(BuildJob(configuration.Job, processName, fileLocation))      
  
#======================================================================   
if __name__ == "__main__":
    """
    Here the code should appear that is executed when running the plotter directly
    (and not import it in another python file via 'import Plotter')
    """
   
    main( sys.argv[1:] )

