"""
Library Interface for Opy Utility 
"""
import settings
from settings import ConfigSettings as OpyConfig

def obfuscate( sourceRootDirectory = None
             , targetRootDirectory = None
             , configFilePath      = None
             , configSettings      = None
             ):    
    settings.isLibraryInvoked    = True
    settings.printHelp           = False
    settings.sourceRootDirectory = sourceRootDirectory
    settings.targetRootDirectory = targetRootDirectory
    settings.configSettings      = configSettings
    settings.configFilePath = ( 
        configFilePath if configSettings is None else False )        
    print "Opy Settings"
    print "sourceRootDirectory: %s" % (sourceRootDirectory,)
    print "targetRootDirectory: %s" % (targetRootDirectory,)
    print "configFilePath: %s"      % (configFilePath,)
    print "configSettings: \n%s"    % (configSettings,)    
    import opy
    
def printHelp():    
    settings.isLibraryInvoked = True
    settings.printHelp        = True    
    import opy    