from opy import obfuscate, OpyConfig
import os, sys

thisDir   = os.path.dirname( os.path.realpath( sys.argv[0] ) )
scrDir    = thisDir
trgDir    = os.path.join( thisDir,   "obfuscated" )

config    = OpyConfig()
config.skip_path_fragments = [ os.path.relpath( sys.argv[0] ) ]

obfuscate(   sourceRootDirectory = scrDir
           , targetRootDirectory = trgDir
           , configSettings      = config )