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

def analyze( sourceRootDirectory = None
           , fileList            = []  
           , configSettings      = OpyConfig()
           ):    
    settings.isLibraryInvoked    = True
    settings.printHelp           = False
    settings.sourceRootDirectory = sourceRootDirectory
    settings.targetRootDirectory = None
    configSettings.subset_files  = fileList
    configSettings.dry_run       = True
    settings.configSettings      = configSettings
    settings.configFilePath      = False         
    print "Analyze Opy Settings"
    print "sourceRootDirectory: %s" % (sourceRootDirectory,)
    print "configSettings: \n%s"    % (configSettings,)    
    import opy
    return ( opy.obfuscatedWordList
           , opy.parser.obfuscatedModImports
           , opy.parser.maskedIdentifiers
    )
    
def printHelp():    
    settings.isLibraryInvoked = True
    settings.printHelp        = True    
    import opy    