import re
import ast

NEWLINE              = '\n'
SPACE                = ' '    
CONTINUATION         = "\\"
TAB                  = '\t'
IMPORT_PREFIX        = "import "
FROM_PREFIX          = "from "
AS_KEYWORD           = "as"
MEMBER_DELIM = SUB_MOD_DELIM = "."
LIST_DELIM           = ","        
ALIAS_TEMPLATE       = "alias_%d"  
SET_ALIAS_TEMPLATE   = "%s as %s"
IMPORT_TEMPLATE      = "%simport %s"
FROM_TEMPLATE        = "%sfrom %s import %s"  
IDENTIFIER_REGEX     = r'\b{0}\b'
IDENTIFIER_DOT_REGEX = r'\b{0}\.\b'
CONTINUED_TEMPLATE   = "%s%s%s"
LONG_LINE_TEMPLATE   = "%s%s"
MAGIC_PREFFIX = MAGIC_SUFFIX = PRIVATE_PREFIX = "__"

# -----------------------------------------------------------------------------
obfuscatedModImports = set()
maskedIdentifiers    = set() 
__modAliases = {}
__mbrAliases = {} 

def injectAliases( fileContent, clearTextMods ):
    return __parseImports( fileContent, True, clearTextMods )

def analyzeImports( fileContent, clearTextMods=[] ):
    __parseImports( fileContent, False, clearTextMods )

# TODO: Rewrite using the ast module. See findPublicIdentifiers()...    
def __parseImports( fileContent, isMasking, clearTextMods=[] ):
    """
    This function has two modes of operation, switched between via
    the isMasking argument: 
    
    A) When isMasking is False: 
        Simply find imports and populate obfuscatedModImports and maskedIdentifiers 
        
    B) When isMasking is True: 
        Provide aliases for the non-obfuscated imports modules and objects 
        (i.e. clearTextMods). Those aliases then become obfuscated, 
        by Opy implicitly, thereby making the code a bit more 
        difficult to read... 
        (of course it's not too hard to de-obfuscate that!)        
    """

    global __modAliases, __mbrAliases                
    __modAliases = {} 
    __mbrAliases = {}

    def isImportLn( line ):
        # mulit-line strings/comments should have been isolated
        # from the fileContent before assignExternalAliases was called
        stripped = line.strip()
        isImportLine = stripped.startswith( IMPORT_PREFIX )
        isFromLine = stripped.startswith( FROM_PREFIX )
        isEither = (isImportLine or isFromLine) 
        return isEither, isImportLine, isFromLine
        
    def isClearTextMod( modName ):
        modSubs = modName.split( SUB_MOD_DELIM )
        subMod = ""
        for sub in modSubs:                
            subMod += sub if subMod == "" else (SUB_MOD_DELIM + sub)
            if subMod in clearTextMods: return True
        return False                        
    
    def processLine( line ):
        global obfuscatedModImports, maskedIdentifiers, __modAliases, __mbrAliases
        # determine if this is an import/from line
        stripped = line.strip()
        _, isImportLine, isFromLine = isImportLn( line )
        # If it is an import/from line, split off the items 
        # part of it, and remove any extra spaces in that. 
        # Skip to the next line if there are no import items 
        # to parse.
        if isImportLine :                           
            try: itemsPart = SPACE.join( stripped.split( SPACE )[1:] )     
            except: return line
        elif isFromLine:
            tokens = stripped.split( SPACE )                
            try:
                # on a from line, if the module name is not preserved 
                # anyway, skip the entire line 
                modName = tokens[1]     
                if not isClearTextMod( modName ):
                    obfuscatedModImports.add( modName ) 
                    return line                                                
                itemsPart = SPACE.join( tokens[3:] )     
            except: return line
        else: return line               
        # split & strip all the import items 
        items = itemsPart.split( LIST_DELIM )
        normList = [i.strip() for i in items]
        revisedImports=[]
        for item in normList :
            # tokenize the list item 
            tokens = item.split( SPACE )
            importName = tokens[0]
            # on an import line, if the module name is not preserved 
            # anyway, skip the item
            if isImportLine :
                modName = importName                
                if not isClearTextMod( modName ):
                    obfuscatedModImports.add( modName ) 
                    continue                    
            # determine if the import is aliased
            try   : isAliased = tokens[1]==AS_KEYWORD
            except: isAliased = False
            # give the import an alias if it doesn't have one
            if not isAliased:                             
                alias = ( ALIAS_TEMPLATE % 
                          (len(__modAliases) + len(__mbrAliases),) )
                item = SET_ALIAS_TEMPLATE % ( importName, alias )      
                if isImportLine : 
                    __modAliases[importName]=alias
                else: 
                    __mbrAliases[importName]=alias        
                maskedIdentifiers.add( importName )                                                
            revisedImports.append( item )                    
        # re-build the line                                                        
        leadSpaces = SPACE * (len(line) - len(line.lstrip(SPACE)))
        itemsPart = LIST_DELIM.join( revisedImports )    
        line = ( (IMPORT_TEMPLATE % (leadSpaces, itemsPart))
                 if isImportLine else
                 (FROM_TEMPLATE % 
                   (leadSpaces, modName, itemsPart)) )
        return line

    def applyAliases( lines ): 
        #TODO: trim this down. It functions, it's ugly...
        nakedAliasesRegEx={}
        dotAliasesRegEx={}        
        for name in maskedIdentifiers :
            nakedAliasesRegEx[name] = ( 
                re.compile( IDENTIFIER_REGEX.format( name ) ) ) 
        for name in maskedIdentifiers :
            dotAliasesRegEx[name] = ( 
                re.compile( IDENTIFIER_DOT_REGEX.format( name ) ) ) 
        revLines = []   
        for line in lines:
            if not isImportLn( line )[0]:
                for name, regEx in dotAliasesRegEx.iteritems():
                    modAlias = __modAliases.get(name)
                    mbrAlias = __mbrAliases.get(name)                    
                    if mbrAlias: line = regEx.sub( mbrAlias + MEMBER_DELIM, line )
                    elif modAlias: line = regEx.sub( modAlias + MEMBER_DELIM, line )                    
                for name, regEx in nakedAliasesRegEx.iteritems():
                    modAlias = __modAliases.get(name)
                    mbrAlias = __mbrAliases.get(name)                    
                    if mbrAlias: line = regEx.sub( mbrAlias, line )
                    elif modAlias: line = regEx.sub( modAlias, line )                    
            revLines.append( line )
        return revLines

    # split the fileContent into lines and
    # roll all lines broken via continuations
    # into long single lines, thus eliminating that
    # messy detail from any subsequent logic        
    lines = __toLines( fileContent, combineContinued=True )
    if isMasking :
        # find the imports and inject aliases         
        revLines = []                   
        for l in lines: revLines.append( processLine( l ) )          
        # apply the aliases to original import names
        # reassemble and return the revised lines                            
        revLines = applyAliases( revLines )
        return NEWLINE.join( revLines )
    else :
        # find the imports, but discard the masking revisions  
        for l in lines: processLine( l ) 

def __toLines( fileContent, combineContinued=False ):
    lines = fileContent.split( NEWLINE )
    if combineContinued :
        revLines = []
        longLine = ""
        for l in lines:
            if l.strip().endswith( CONTINUATION ):
                longLine = ( CONTINUED_TEMPLATE % 
                    (longLine, l.rstrip()[:-1], SPACE ) )
            else :            
                longLine = LONG_LINE_TEMPLATE % (longLine, l)
                revLines.append( longLine )
                longLine = ""
        lines = revLines
    return lines 

# -----------------------------------------------------------------------------
def findPublicIdentifiers( fileContent ):
    publicIds=set()
    root = ast.parse( fileContent )    
    publicIds.update( __findAstPublicNameAssigns( root ) )
    publicIds.update( __findAstPublicFuncsClassesAttribs( root ) )
    return publicIds

# recursive
def __findAstPublicFuncsClassesAttribs( node ):
    publicNodes = set()    
    for child in ast.iter_child_nodes( node ):       
        if( isinstance( child, ast.FunctionDef ) or 
            isinstance( child, ast.ClassDef ) ):            
            if __isPrivatePrefix( child.name ) : continue                        
            publicNodes.add( child.name ) 
            publicNodes.update( __findAstPublicAttribAssigns( child ) )            
            publicNodes.update( __findAstPublicFuncsClassesAttribs( child ) )
    return publicNodes

def __findAstPublicAttribAssigns( node ):
    publicNodes = set()    
    for child in ast.iter_child_nodes( node ):
        if isinstance( child, ast.Assign ):
            for target in child.targets :
                if isinstance( target, ast.Attribute ) :        
                    if not __isPrivatePrefix( target.attr ):    
                        publicNodes.add( target.attr )
    return publicNodes

def __findAstPublicNameAssigns( node ):
    publicNodes = []    
    for child in ast.iter_child_nodes( node ):
        if isinstance( child, ast.Assign ):
            for target in child.targets :
                if isinstance( target, ast.Name ) :
                    if not __isPrivatePrefix( target.id ):    
                        publicNodes.append( target.id )
    return publicNodes

def __isPrivatePrefix( identifier ):
    return ( identifier.startswith( PRIVATE_PREFIX )
             and not identifier.endswith( MAGIC_SUFFIX ) )
