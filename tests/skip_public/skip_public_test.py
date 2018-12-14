from opy import obfuscate, OpyConfig
import os, sys

thisDir   = os.path.dirname( os.path.realpath( sys.argv[0] ) )
scrDir    = thisDir
trgDir    = os.path.join( thisDir, "obfuscated" )

config = OpyConfig()
config.subset_files = ["public_private.py"]
config.skip_public = True

obfuscate(   sourceRootDirectory = scrDir
           , targetRootDirectory = trgDir
           , configSettings=config )