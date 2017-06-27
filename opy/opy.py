#! /usr/bin/python

license = (
'''_opy_Copyright 2014, 2015, 2016, 2017 Jacques de Hooge, GEATEC engineering, www.geatec.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''
)

import re
import os
import sys
import errno
import keyword
import importlib
import random
import codecs
import shutil

# =========== Initialize constants

programName = 'opy'
programVersion = '1.1.25'

if __name__ == '__main__':
    print ('{} (TM) Configurable Multi Module Python Obfuscator Version {}'.format (programName.capitalize (), programVersion))
    print ('Copyright (C) Geatec Engineering. License: Apache 2.0 at  http://www.apache.org/licenses/LICENSE-2.0\n')

    random.seed ()

    isPython2 = sys.version_info [0] == 2
    charBase = 2048         # Choose high to prevent string recoding from generating special chars like ', " and \
    stringNr = charBase
    charModulus = 7

    # =========== Utilities

    def createFilePath (filePath, open = False):
        try:
            os.makedirs (filePath.rsplit ('/', 1) [0])
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
                
        if open:
            return codecs.open (filePath, encoding = 'utf-8', mode = 'w')
            
    def getObfuscatedName (obfuscationIndex, name):
        return '{0}{1}{2}'.format (
            '__' if name.startswith ('__') else '_' if name.startswith ('_') else 'l',
            bin (obfuscationIndex) [2:] .replace ('0', 'l'),
            obfuscatedNameTail
        )
        
    def scramble (stringLiteral):
        global stringNr
        
        if isPython2:
            recodedStringLiteral = unicode () .join ([unichr (charBase + ord (char) + (charIndex + stringNr) % charModulus) for charIndex, char in enumerate (stringLiteral)])
            stringKey = unichr (stringNr)
        else:
            recodedStringLiteral = str () .join ([chr (charBase + ord (char) + (charIndex + stringNr) % charModulus) for charIndex, char in enumerate (stringLiteral)])
            stringKey = chr (stringNr)
            
        rotationDistance = stringNr % len (stringLiteral)
        rotatedStringLiteral = recodedStringLiteral [:-rotationDistance] + recodedStringLiteral [-rotationDistance:]
        keyedStringLiteral = rotatedStringLiteral + stringKey
        
        stringNr += 1
        return 'u"' + keyedStringLiteral + '"'      
        
    def getUnScrambler (stringBase):
        return '''
import sys

isPython2{0} = sys.version_info [0] == 2
charBase{0} = {1}
charModulus{0} = {2}

def unScramble{0} (keyedStringLiteral):
    global stringNr{0}
    
    stringNr = ord (keyedStringLiteral [-1])
    rotatedStringLiteral = keyedStringLiteral [:-1]
    
    rotationDistance = stringNr % len (rotatedStringLiteral)
    recodedStringLiteral = rotatedStringLiteral [:rotationDistance] + rotatedStringLiteral [rotationDistance:]
        
    if isPython2{0}:
        stringLiteral = unicode () .join ([unichr (ord (char) - charBase{0} - (charIndex + stringNr) % charModulus{0}) for charIndex, char in enumerate (recodedStringLiteral)])
    else:
        stringLiteral = str () .join ([chr (ord (char) - charBase{0} - (charIndex + stringNr) % charModulus{0}) for charIndex, char in enumerate (recodedStringLiteral)])
        
    return eval (stringLiteral)
    '''.format (plainMarker, charBase, charModulus) 
            
    def printHelpAndExit (errorLevel):
        print (r'''

*******************************************************************************
{0} will obfuscate your extensive, real world, multi module Python source code for free!
And YOU choose per project what to obfuscate and what not, by editting the config file.

BACKUP YOUR CODE AND VALUABLE DATA TO AN OFF-LINE MEDIUM FIRST TO PREVENT ACCIDENTAL LOSS OF WORK!!!

Then copy the default config file to the source top directory <topdir> and run {0} from there.
It will generate an obfuscation directory <topdir>/../<topdir>_{1}

At first some identifiers may be obfuscated that shouldn't be, e.g. some of those imported from external modules.   
Adapt your config file to avoid this, e.g. by adding external module names that will be recursively scanned for identifiers.
You may also exclude certain words or files in your project from obfuscation explicitly.
Source directory, obfuscation directory and config file path can also be supplied as command line parameters in that order.
Comments and string literals can be marked as plain, bypassing obfuscation

Known limitations:

A comment after a string literal should be preceded by whitespace
A ' or " inside a string literal should be escaped with \ rather then doubled
If the pep8_comments option is False (the default), a {2} in a string literal can only be used at the start, so use 'p''{2}''r' rather than 'p{2}r'
If the pep8_comments option is set to True, however, only a <blank><blank>{2}<blank> cannot be used in the middle or at the end of a string literal
Obfuscation of string literals is unsuitable for sensitive information since it can be trivially broken
No renaming backdoor support for methods starting with __ (non-overridable methods, also known as private methods)

Licence:
{3}
*******************************************************************************
        '''.format (programName.capitalize (), programName, r'#', license))
        exit (errorLevel)
        
    # ============ Assign directories ============

    if len (sys.argv) > 1:
        if '?' in sys.argv [1]:
            printHelpAndExit (0)
        sourceRootDirectory = sys.argv [1]
    else:
        sourceRootDirectory = os.getcwd () .replace ('\\', '/')

    if len (sys.argv) > 2:
        targetRootDirectory = sys.argv [2]
    else:
        targetRootDirectory = '{0}/{1}_{2}'.format (* (sourceRootDirectory.rsplit ('/', 1) + [programName]))

    if len (sys.argv) > 3:
        configFilePath = sys.argv [3]
    else:
        configFilePath = '{0}/{1}_config.txt'.format (sourceRootDirectory, programName)

    # =========== Read config file

    # Default values for config items to preserve backward compatibility if items are added
    obfuscate_strings = False
    obfuscated_name_tail = '_{}_'.format (programName)
    plain_marker = '_{}_'.format (programName)
    source_extensions = ''
    skip_extensions = ''
    external_modules = ''
    plain_files = ''
    plain_names = ''
        
    try:
        configFile = open (configFilePath)
    except Exception as exception:
        print (exception)
        printHelpAndExit (1)
        
    exec (configFile.read ())
    configFile.close ()

    try:
        obfuscateStrings = obfuscate_strings
    except:
        obfuscateStrings = False
        
    try:
        asciiStrings = ascii_strings
    except:
        asciiStrings = False
        
    try:
        obfuscatedNameTail = obfuscated_name_tail
    except:
        obfuscatedNameTail = ''
        
    try:
        plainMarker = plain_marker
    except:
        plainMarker = '_{0}_'.format (programName)
        
    try:
        pep8Comments = pep8_comments
    except:
        pep8Comments = False
        
    sourceFileNameExtensionList = source_extensions.split ()
    skipFileNameExtensionList = skip_extensions.split ()
    externalModuleNameList = external_modules.split ()
    plainFileRelPathList = plain_files.split ()
    extraPlainWordList = plain_names.split ()

    # ============ Gather source file names

    sourceFilePathList = [
        '{0}/{1}'.format (directory.replace ('\\', '/'), fileName)
        for directory, subDirectories, fileNames in os.walk (sourceRootDirectory)
        for fileName in fileNames
    ]

    # =========== Define comment swapping tools
            
    shebangCommentRegEx = re.compile (r'^{0}!'.format (r'#'))
    codingCommentRegEx = re.compile ('coding[:=]\s*([-\w.]+)')
    keepCommentRegEx = re.compile ('.*{0}.*'.format (plainMarker), re.DOTALL)
        
    def getCommentPlaceholderAndRegister (matchObject):
        comment = matchObject.group (0)
        if keepCommentRegEx.search (comment):   # Rare, so no need for speed
            replacedComments.append (comment.replace (plainMarker, ''))
            return commentPlaceholder
        else:
            return ''
        
    def getComment (matchObject):
        global commentIndex
        commentIndex += 1
        return replacedComments [commentIndex]
        
    commentRegEx = (
            re.compile (r'{0}{1}{2}.*?$'.format (
                r"(?<!')",
                r'(?<!")',
                r'  # '  # Acording to PEP8 an inline comment should start like this.
            ), re.MULTILINE)
        if pep8_comments else
            re.compile (r'{0}{1}{2}.*?$'.format (
                r"(?<!')",
                r'(?<!")',
                r'#'    # Acording to PEP8 an inline comment should start like this.
            ), re.MULTILINE)
    )
    commentPlaceholder = '_{0}_c_'.format (programName)
    commentPlaceholderRegEx = re.compile (r'{0}'.format (commentPlaceholder))

    # ============ Define string swapping tools

    keepStringRegEx = re.compile (r'.*{0}.*'.format (plainMarker))
        
    def getDecodedStringPlaceholderAndRegister (matchObject):
        string = matchObject.group (0)
        if obfuscateStrings:
            if keepStringRegEx.search (string): # Rare, so no need for speed
                replacedStrings.append (string.replace (plainMarker, ''))
                return stringPlaceholder    # Store original string minus plainMarker, no need to unscramble
            else:
                replacedStrings.append (scramble (string))
                return 'unScramble{0} ({1})'.format (plainMarker, stringPlaceholder)    # Store unScramble (<scrambledString>)
        else:
            replacedStrings.append (string)
            return stringPlaceholder
        
    def getString (matchObject):
        global stringIndex
        stringIndex += 1
        return replacedStrings [stringIndex]

    stringRegEx = re.compile (r'([ru]|ru|ur)?(({0})|({1})|({2})|({3}))'.format (
        r"'''.*?(?<![^\\]\\)(?<![^\\]\')'''",
        r'""".*?(?<![^\\]\\)(?<![^\\]\")"""',
        r"'.*?(?<![^\\]\\)'",
        r'".*?(?<![^\\]\\)"'
    ), re.MULTILINE | re.DOTALL | re.VERBOSE)

    stringPlaceholder = '_{0}_s_'.format (programName)
    stringPlaceholderRegEx = re.compile (r'{0}'.format (stringPlaceholder))

    # ============ Define 'from future' moving tools

    def moveFromFuture (matchObject):
        fromFuture = matchObject.group (0)

        if fromFuture:
            global nrOfSpecialLines
            contentList [nrOfSpecialLines:nrOfSpecialLines] = [fromFuture]  # Move 'from __future__' line after other special lines
            nrOfSpecialLines += 1
        return ''
        
    fromFutureRegEx = re.compile ('from\s*__future__\s*import\s*\w+.*$', re.MULTILINE)

    # ============ Define identifier recognition tools

    identifierRegEx = re.compile (r'''
        \b          # Delimeted
        (?!{0})     # Not starting with commentPlaceholder
        (?!{1})     # Not starting with stringPlaceholder
        [^\d\W]     # De Morgan: Not (decimal or nonalphanumerical) = not decimal and alphanumerical
        \w*         # Alphanumerical
        (?<!__)     # Not ending with __
        (?<!{0})    # Not ending with commentPlaceholder
        (?<!{1})    # Not ending with stringPlaceHolder
        \b          # Delimited
    '''.format (commentPlaceholder, stringPlaceholder), re.VERBOSE) # De Morgan

    chrRegEx = re.compile (r'\bchr\b')

    # =========== Generate skip list

    skipWordSet = set (keyword.kwlist + ['__init__'] + extraPlainWordList)  # __init__ should be in, since __init__.py is special

    plainFilePathList = ['{0}/{1}'.format (sourceRootDirectory, plainFileRelPath) for plainFileRelPath in plainFileRelPathList]
    for plainFilePath in plainFilePathList:
        plainFile = open (plainFilePath)
        content = plainFile.read ()
        plainFile.close ()
        
        # Throw away comment-like line tails
        
        content = commentRegEx.sub ('', content)
        
        # Throw away strings
        
        content = stringRegEx.sub ('', content)
        
        # Put identifiers in skip word set
        
        skipWordSet.update (re.findall (identifierRegEx, content))
        
    class ExternalModules:
        def __init__ (self):
            for externalModuleName in externalModuleNameList:
                attributeName = externalModuleName.replace ('.', plainMarker)   # Replace . in module name by placeholder to get attribute name
                
                try:
                    exec (
                        '''
import {0} as currentModule
                        '''.format (externalModuleName),
                        globals ()
                    )
                    setattr (self, attributeName, currentModule)    
                except Exception as exception:
                    print (exception)
                    setattr (self, attributeName, None) # So at least the attribute name will be available
                    print ('Warning: could not inspect external module {0}'.format (externalModuleName))
                
    externalModules = ExternalModules ()
    externalObjects = set ()
                
    def addExternalNames (anObject):
        if anObject in externalObjects:
            return
        else:
            externalObjects.update ([anObject])

        try:
            attributeNameList = list (anObject.__dict__)
        except:
            attributeNameList = []
        
        try:
            if isPython2:
                parameterNameList = list (anObject.func_code.co_varnames)
            else:
                parameterNameList = list (anObject.__code__.co_varnames)
        except:     
            parameterNameList = []
            
        attributeList = [getattr (anObject, attributeName) for attributeName in attributeNameList]
        attributeSkipWordList = (plainMarker.join (attributeNameList)) .split (plainMarker) # Split module name chunks that were joined by placeholder
        
        updateSet = set ([entry for entry in (parameterNameList + attributeSkipWordList) if not (entry.startswith ('__') and entry.endswith ('__'))])
        # Entries both starting and ending with __ are skipped anyhow by the identifier regex, not including them here saves time
        
        skipWordSet.update (updateSet)
        
        for attribute in attributeList: 
            try:
                addExternalNames (attribute)
            except:
                pass

    addExternalNames (__builtins__)
    addExternalNames (externalModules)

    skipWordList = list (skipWordSet)
    skipWordList.sort (key = lambda s: s.lower ())

    # ============ Generate obfuscated files

    obfuscatedWordList = []
    obfuscatedRegExList = []

    for sourceFilePath in sourceFilePathList:
        if sourceFilePath == configFilePath:    # Don't copy the config file to the target directory
            continue

        sourceDirectory, sourceFileName = sourceFilePath.rsplit ('/', 1)
        sourceFilePreName, sourceFileNameExtension = (sourceFileName.rsplit ('.', 1) + ['']) [ : 2]
        targetRelSubDirectory =  sourceFilePath [len (sourceRootDirectory) : ]
        
        # Read plain source

        if sourceFileNameExtension in sourceFileNameExtensionList and not sourceFilePath in plainFilePathList:
            stringBase = random.randrange (64)
        
            sourceFile = codecs.open (sourceFilePath, encoding = 'utf-8')
            content = sourceFile.read ()
            sourceFile.close ()
            
            replacedComments = []
            contentList = content.split ('\n', 2)
                
            nrOfSpecialLines = 0
            insertCodingComment = True
            
            if len (contentList) > 0:
                if shebangCommentRegEx.search (contentList [0]):                                # If the original code starts with a shebang line
                    nrOfSpecialLines += 1                                                       #   Account for that
                    if len (contentList) > 1 and codingCommentRegEx.search (contentList [1]):   #   If after the shebang a coding comment follows
                        nrOfSpecialLines += 1                                                   #       Account for that
                        insertCodingComment = False                                             #       Don't insert, it's already there
                elif codingCommentRegEx.search (contentList [0]):                               # Else if the original code starts with a coding comment
                    nrOfSpecialLines += 1                                                       #   Account for that
                    insertCodingComment = False                                                 #   Don't insert, it's already there
                
            if obfuscateStrings and insertCodingComment:                                        # Obfuscated strings are always converted to unicode
                contentList [nrOfSpecialLines:nrOfSpecialLines] = ['# coding: UTF-8']           # Insert the coding line if it wasn't there
                nrOfSpecialLines += 1                                                           # And remember it's there
                                                                                                # Nothing has to happen with an eventual shebang line
            if obfuscateStrings:
                normalContent = '\n'.join ([getUnScrambler (stringBase)] + contentList [nrOfSpecialLines:])
            else:
                normalContent = '\n'.join (contentList [nrOfSpecialLines:])
                
            # At this point normalContent does not contain the special lines
            # They are in contentList
            
            normalContent = commentRegEx.sub (getCommentPlaceholderAndRegister, normalContent)
             
            # Replace strings by string placeholders
            
            replacedStrings = []
            normalContent = stringRegEx.sub (getDecodedStringPlaceholderAndRegister, normalContent)
            
            # Take eventual out 'from __future__ import ... ' line and add it to contentlist
            # Content list is prepended to normalContent later
            
            normalContent = fromFutureRegEx.sub (moveFromFuture, normalContent)
                
            # Obfuscate content without strings
            
            # All source words and module name
            sourceWordSet = set (re.findall (identifierRegEx, normalContent) + [sourceFilePreName])

            # Add source words that are not yet obfuscated and shouldn't be skipped to global list of obfuscated words, preserve order of what's already there
            strippedSourceWordSet = sourceWordSet.difference (obfuscatedWordList).difference (skipWordSet)  # Leave out what is already or shouldn't be obfuscated
            strippedSourceWordList = list (strippedSourceWordSet)
            strippedSourceRegExList = [re.compile (r'\b{0}\b'.format (sourceWord)) for sourceWord in strippedSourceWordList]    # Regex used to replace obfuscated words
            obfuscatedWordList += strippedSourceWordList            
            obfuscatedRegExList += strippedSourceRegExList
            
            # Replace words to be obfuscated by obfuscated ones
            for obfuscationIndex, obfuscatedRegEx in enumerate (obfuscatedRegExList):
                normalContent = obfuscatedRegEx.sub (
                    getObfuscatedName (obfuscationIndex, obfuscatedWordList [obfuscationIndex]),
                    normalContent
                )   # Use regex to prevent replacing word parts
                
            # Replace string placeholders by strings
            
            stringIndex = -1
            normalContent = stringPlaceholderRegEx.sub (getString, normalContent)
        
            # Replace nonempty comment placeholders by comments
            
            commentIndex = -1
            normalContent = commentPlaceholderRegEx.sub (getComment, normalContent)
            
            content = '\n'.join (contentList [:nrOfSpecialLines] + [normalContent])
            
            # Remove empty lines
            
            content = '\n'.join ([line for line in [line.rstrip () for line in content.split ('\n')] if line])
            
            # Write target 
            
            # Obfuscate module name
            try:
                targetFilePreName = getObfuscatedName (obfuscatedWordList.index (sourceFilePreName), sourceFilePreName)
            except: # Not in list, e.g. toplevel module name
                targetFilePreName = sourceFilePreName
            
            # Obfuscate module subdir names, but only above the project root!
            targetChunks = targetRelSubDirectory.split ('/')
            for index in range (len (targetChunks)):
                try:
                    targetChunks [index] = getObfuscatedName (obfuscatedWordList.index (targetChunks [index]), targetChunks [index])
                except: # Not in list
                    pass
            targetRelSubDirectory = '/'.join (targetChunks)
            targetSubDirectory = '{0}{1}'.format (targetRootDirectory, targetRelSubDirectory) .rsplit ('/', 1) [0]

            # Create target path and write file
            targetFile = createFilePath ('{0}/{1}.{2}'.format (targetSubDirectory, targetFilePreName, sourceFileNameExtension), open = True)
            targetFile.write (content)
            targetFile.close ()
        elif not sourceFileNameExtension in skipFileNameExtensionList:
            targetSubDirectory = '{0}{1}'.format (targetRootDirectory, targetRelSubDirectory) .rsplit ('/', 1) [0]
            
            # Create target path and copy file
            targetFilePath = '{0}/{1}'.format (targetSubDirectory, sourceFileName)
            createFilePath (targetFilePath)
            shutil.copyfile (sourceFilePath, targetFilePath)
            
    print ('Obfuscated words: {0}'.format (len (obfuscatedWordList)))
    
    # Opyfying something twice can and is allowed to fail.
    # The obfuscation for e.g. variable 1 in round 1 can be the same as the obfuscation for e.g. variable 2 in round 2.
    # If in round 2 variable 2 is replaced first, the obfuscation from round 1 for variable 1 will be replaced by the same thing.
    