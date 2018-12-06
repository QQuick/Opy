"""
Library Interface for Opy Utility 
"""
from . import settings
from . settings import ConfigSettings as OpyConfig
from . patcher import OpyFile, patch, setLine, replaceInLine

def obfuscate( sourceRootDirectory = None
             , targetRootDirectory = None
             , configFilePath      = None
             , configSettings      = None
             ):    
    global opy
    settings.isLibraryInvoked    = True
    settings.printHelp           = False
    settings.sourceRootDirectory = sourceRootDirectory
    settings.targetRootDirectory = targetRootDirectory
    settings.configSettings      = configSettings
    settings.configFilePath = ( 
        configFilePath if configSettings is None else False )        
    print( "Opy Settings" )
    print( "sourceRootDirectory: %s" % (sourceRootDirectory,) )
    print( "targetRootDirectory: %s" % (targetRootDirectory,) )
    print( "configFilePath: %s"      % (configFilePath,) )
    print( "configSettings: \n%s"    % (configSettings,) )
    __runOpy()
    return ( opy.obfuscatedFileDict
           , opy.obfuscatedWordList  
           , opy.skipWordList        
           , opy.parser.obfuscatedModImports 
           , opy.parser.maskedIdentifiers     
    )    

def analyze( sourceRootDirectory = None
           , fileList            = []  
           , configSettings      = OpyConfig()
           ):    
    global opy
    settings.isLibraryInvoked    = True
    settings.printHelp           = False
    settings.sourceRootDirectory = sourceRootDirectory
    settings.targetRootDirectory = None
    settings.configSettings      = configSettings
    settings.configFilePath      = False

    init_subset_files = settings.configSettings.subset_files
    init_dry_run      = settings.configSettings.dry_run         
    settings.configSettings.subset_files  = fileList
    settings.configSettings.dry_run       = True
         
    print( "Analyze Opy Settings" )
    print( "sourceRootDirectory: %s" % (sourceRootDirectory,) )
    print( "configSettings: \n%s"    % (configSettings,) )
    __runOpy()

    settings.configSettings.subset_files = init_subset_files
    settings.configSettings.dry_run      = init_dry_run
    
    return ( opy.obfuscatedFileDict
           , opy.obfuscatedWordList  
           , opy.skipWordList        
           , opy.parser.obfuscatedModImports 
           , opy.parser.maskedIdentifiers     
    )
    
def printHelp():    
    settings.isLibraryInvoked = True
    settings.printHelp        = True
    __runOpy()
    
def __runOpy():        
    global opy    
    try :
        if settings.isPython2 : 
            reload( opy )
        else :
            try : # Python 3.0 to 3.3                
                import imp 
                imp.reload( opy )
            except : # Python 3.4+                    
                import importlib
                importlib.reload( opy ) # @UndefinedVariable
    except : from . import opy
    