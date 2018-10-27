"""
Library Interface for Opy Utility 
"""
import settings
from settings import ConfigSettings as OpyConfig

def obfuscate( printHelpAndExit    = False
             , sourceRootDirectory = None
             , targetRootDirectory = None
             , configFilePath      = None
             , configSettings      = None
             ):    
    settings.isLibraryInvoked    = True
    settings.printHelpAndExit    = printHelpAndExit
    settings.sourceRootDirectory = sourceRootDirectory
    settings.targetRootDirectory = targetRootDirectory
    settings.configSettings      = configSettings
    settings.configFilePath = ( 
        configFilePath if configSettings is None else False )        
    if not printHelpAndExit :
        print "Opy Settings"
        print "sourceRootDirectory: %s" % (sourceRootDirectory,)
        print "targetRootDirectory: %s" % (targetRootDirectory,)
        print "configFilePath: %s"      % (configFilePath,)
        print "configSettings: \n%s"    % (configSettings,)    
    import opy