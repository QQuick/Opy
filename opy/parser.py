import re
import ast
import six 

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
__modReplace = {}
__modAliases = {}
__mbrAliases = {} 

__ANALIZE_MODE, __MASK_MODE, __REPLACE_MODE = tuple(range(3))

def analyzeImports( fileContent, clearTextMods=[] ):
    __parseImports( fileContent, __ANALIZE_MODE, clearTextMods )

def injectAliases( fileContent, clearTextMods ):
    return __parseImports( fileContent, __MASK_MODE, clearTextMods )

def replaceImports( fileContent, replacements={} ):
    return __parseImports( fileContent, __REPLACE_MODE, replacements=replacements )

# TODO: Rewrite using the ast module. See findPublicIdentifiers()...
def __parseImports( fileContent, mode, clearTextMods=[], replacements={} ):
    """
    This function has multiple modes of operation: 
    
    __ANALIZE_MODE 
        Simply find imports and populate obfuscatedModImports and maskedIdentifiers 
        
    __MASK_MODE 
        Provide aliases for the non-obfuscated imports modules and objects 
        (i.e. clearTextMods). Those aliases then become obfuscated, 
        by Opy implicitly, thereby making the code a bit more 
        difficult to read... 
        (of course it's not too hard to de-obfuscate that!)

    __REPLACE_MODE        
                
    """

    global __modAliases, __mbrAliases, __modReplace                
    __modAliases = {} 
    __mbrAliases = {}
    __modReplace = replacements

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

    def replaceModKey( modName ):
        modSubs = modName.split( SUB_MOD_DELIM )
        subMod = ""
        for sub in modSubs:                
            subMod += sub if subMod == "" else (SUB_MOD_DELIM + sub)
            if subMod in __modReplace: return subMod
        return None                        
    
    def processLine( line, mode ):
        global obfuscatedModImports, maskedIdentifiers, \
            __modAliases, __mbrAliases, __modReplace
        # determine if this is an import/from line
        stripped = line.strip()
        _, isImportLine, isFromLine = isImportLn( line )
        replaceKey = None
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
                # on a from line, if the module name is not 
                # being replaced or preserved, skip the entire line                 
                modName = tokens[1]                     
                if mode==__REPLACE_MODE:
                    replaceKey = replaceModKey( modName )
                    if replaceKey is None : return line
                    # replace the leading portions of the module name only
                    # preserving any sub module names which may follow                    
                    modName = modName.replace( replaceKey, 
                                               __modReplace[replaceKey] )        
                else:
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
            if isImportLine :
                modName = importName
                # on an import line, if the module name is not  
                # being replaced or preserved, skip the item                                   
                if mode==__REPLACE_MODE:
                    replaceKey = replaceModKey( modName )
                    isSkipped = replaceKey is None 
                else:
                    isSkipped = not isClearTextMod( modName )
                    if isSkipped : obfuscatedModImports.add( modName ) 
                if isSkipped :
                    revisedImports.append( item )
                    continue                           
            # determine if the import is aliased
            try   : isAliased = tokens[1]==AS_KEYWORD
            except: isAliased = False
            if mode==__REPLACE_MODE:
                if isImportLine :
                    # replace the leading portions of the module name only
                    # preserving any sub module names which may follow                    
                    replacement = importName.replace( replaceKey, 
                                                      __modReplace[replaceKey] )                    
                    # replace the module name and either preserve an 
                    # existing alias, or alias it be the original name 
                    # if it doesn't have one
                    if isAliased :                
                        try   : alias = tokens[2]
                        except: alias = ""
                    else : alias = importName
                    item = SET_ALIAS_TEMPLATE % ( replacement, alias )
            else :
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
                for name, regEx in six.iteritems( dotAliasesRegEx ):
                    modAlias = __modAliases.get(name)
                    mbrAlias = __mbrAliases.get(name)                    
                    if mbrAlias: line = regEx.sub( mbrAlias + MEMBER_DELIM, line )
                    elif modAlias: line = regEx.sub( modAlias + MEMBER_DELIM, line )                    
                for name, regEx in six.iteritems( nakedAliasesRegEx ):
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
    if (mode==__MASK_MODE) or (mode==__REPLACE_MODE):
        revLines = []
        # find all imports and apply replacements / inject aliases                                    
        for l in lines: revLines.append( processLine( l, mode ) )
        # in mask mode, apply the aliases to original import names
        if mode==__MASK_MODE : revLines = applyAliases( revLines )
        # reassemble and return the revised lines                   
        return NEWLINE.join( revLines )
    else : # find the imports, but discard revisions  
        for l in lines: processLine( l, mode ) 

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
