from opy import analyze, OpyConfig
import os, sys

thisDir   = os.path.dirname( os.path.realpath( sys.argv[0] ) )
parentDir = os.path.dirname( thisDir )
scrDir    = os.path.join( parentDir, "dog_walker" )
config = OpyConfig()

( obfuscatedWordList, skipWordList, 
  obfuscatedModImports, maskedIdentifiers ) = analyze( 
    sourceRootDirectory = scrDir
  , fileList = [ "poly_walker_test.py" ]  
  , configSettings=config  )

print( "--- ANALYSIS ---" )
print( "obfuscatedWordList" )
print( obfuscatedWordList )
#print( "skipWordList" )
#print( skipWordList )
print( "obfuscatedModImports" )
print( obfuscatedModImports )
print( "maskedIdentifiers" )
print( maskedIdentifiers )
