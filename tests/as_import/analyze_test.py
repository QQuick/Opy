from opy import analyze, OpyConfig
import os, sys

thisDir   = os.path.dirname( os.path.realpath( sys.argv[0] ) )
parentDir = os.path.dirname( thisDir )
scrDir    = os.path.join( parentDir, "dog_walker" )
config = OpyConfig()

results = analyze( sourceRootDirectory = scrDir
                 , fileList = [ "poly_walker_test.py" ]  
                 , configSettings=config  )

print( "--- ANALYSIS ---" )
print( "obfuscatedFileDict" )
print( results.obfuscatedFileDict )
print( "obfuscatedWordList" )
print( results.obfuscatedWordList )
# skipWordList is too long for it to be desirable to print it... 
#print( "skipWordList" )
#print( skipWordList )
print( "obfuscatedModImports" )
print( results.obfuscatedModImports )
print( "maskedIdentifiers" )
print( results.maskedIdentifiers )
