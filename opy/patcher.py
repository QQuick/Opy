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

# -----------------------------------------------------------------------------
# High-level / Convenience functions 

def patch( path, patches=[] ):
    f = OpyFile( path )
    for p in patches :
        if len(p)==2:
            lineNo, line = p
            f.setLine( lineNo, line ) 
        elif len(p)==3:
            lineNo, old, new = p
            f.replaceInLine( lineNo, old, new )     
    f.update()

def setLine( path, lineNo, line ):
    f = OpyFile( path )
    f.setLine(lineNo, line) 
    f.update()

def replaceInLine( path, lineNo, old, new ):
    f = OpyFile( path )
    f.replaceInLine( lineNo, old, new  ) 
    f.update()
            