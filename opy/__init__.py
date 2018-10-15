"""
Library Interface for Opy Utility 
"""
from opymaster import programName, programVersion
import opymaster
 
def obfuscate( printHelpAndExit    = False
             , sourceRootDirectory = None
             , targetRootDirectory = None
             , configFilePath      = None
             ):    
    opymaster.isLibrary           = True
    opymaster.printHelpAndExit    = printHelpAndExit
    opymaster.sourceRootDirectory = sourceRootDirectory
    opymaster.targetRootDirectory = targetRootDirectory
    opymaster.configFilePath      = configFilePath    
    if not printHelpAndExit :
        print "sourceRootDirectory: %s" % (sourceRootDirectory,)
        print "targetRootDirectory: %s" % (targetRootDirectory,)
        print "configFilePath: %s"      % (configFilePath,)    
    import opy