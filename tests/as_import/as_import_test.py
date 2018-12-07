from opy import obfuscate
import os, sys

thisDir   = os.path.dirname( os.path.realpath( sys.argv[0] ) )
parentDir = os.path.dirname( thisDir )
scrDir    = os.path.join( parentDir, "dog_walker" )
trgDir    = os.path.join( thisDir,   "obfuscated" )
cfgFile   = os.path.join( thisDir,   "test_config.txt" )

results = obfuscate( sourceRootDirectory = scrDir
                   , targetRootDirectory = trgDir
                   , configFilePath      = cfgFile )

print( "obfuscatedWordList" )
print( results.obfuscatedWordList )