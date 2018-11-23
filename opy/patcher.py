class OpyFile:
    def __init__( self, path ):
        self.__path = path
        with open( self.__path, 'rb' ) as f: self.__lines = f.readlines()

    def lines( self, isNumbered=False ):
        if isNumbered: 
            return [ ((i+1), ln) for i, ln in enumerate( self.__lines ) ]
        return self.__lines

    def line( self, lineNo ): return self.__lines[ lineNo-1 ]
    
    def setLine( self, lineNo, line ): self.__lines[ lineNo-1 ] = line
    
    def replaceInLine( self, lineNo, old, new ): 
        self.setLine( lineNo, self.line( lineNo ).replace( old, new ) )
        
    def update( self ):    
        with open( self.__path, 'wb' ) as f: f.writelines( self.__lines ) 
