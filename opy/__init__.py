"""
Library Interface for Opy Utility 
"""
import settings
 
def obfuscate( printHelpAndExit    = False
             , sourceRootDirectory = None
             , targetRootDirectory = None
             , configFilePath      = None
             ):    
    settings.isLibraryInvoked    = True
    settings.printHelpAndExit    = printHelpAndExit
    settings.sourceRootDirectory = sourceRootDirectory
    settings.targetRootDirectory = targetRootDirectory
    settings.configFilePath      = configFilePath    
    if not printHelpAndExit :
        print "Opy Settings"
        print "sourceRootDirectory: %s" % (sourceRootDirectory,)
        print "targetRootDirectory: %s" % (targetRootDirectory,)
        print "configFilePath: %s"      % (configFilePath,)    
    import opy