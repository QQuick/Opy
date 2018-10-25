import io

isLibraryInvoked    = False
printHelpAndExit    = False
sourceRootDirectory = None
targetRootDirectory = None
configFilePath      = None # None == default, False == use configSettings

class ConfigSettings :
    def __init__( self ) :    
        self.obfuscate_strings = True        
        self.obfuscated_name_tail = '_opy_'  
        self.plain_marker = '_opy_'          
        self.pep8_comments = False
        self.source_extensions = [ 'py', 'pyx' ]          
        self.skip_extensions = [ 
             'pyc'
            ,'txt'
            ,'project'      # Eclipse/PyDev IDE files/folders
            ,'pydevproject'
            ,'settings' 
        ] 
        self.skip_path_fragments = [ 
             'opy_config.txt'
            ,'opy_config.py' 
        ]
        self.external_modules = [
             're'
            ,'os'
            ,'sys'
            ,'errno'
            ,'keyword'
            ,'importlib'
            ,'random'
            ,'codecs'
            ,'shutil'
            ,'traceback'
            ,'ConfigParser'
        ]
        self.plain_files = []
        self.plain_names = []

    def __str__( self ):
        # TODO : rewrite this in a more clean/clever manner... 
        text = ( 
              "obfuscate_strings = %s\n" % str(self.obfuscate_strings)         
            + "obfuscated_name_tail = '%s'\n" % self.obfuscated_name_tail
            + "plain_marker = '%s'\n" % self.plain_marker
            + "pep8_comments = %s\n" % str(self.pep8_comments)
        )
        text += "source_extensions ='''\n"
        for item in self.source_extensions : text += "%s\n" % item
        text += "'''\n"
        text += "skip_extensions ='''\n"
        for item in self.skip_extensions : text += "%s\n" % item
        text += "'''\n"
        text += "skip_path_fragments ='''\n"
        for item in self.skip_path_fragments : text += "%s\n" % item
        text += "'''\n"
        text += "external_modules ='''\n"
        for item in self.external_modules : text += "%s\n" % item
        text += "'''\n"
        text += "plain_files ='''\n"
        for item in self.plain_files : text += "%s\n" % item
        text += "'''\n"
        text += "plain_names ='''\n"
        for item in self.plain_names : text += "%s\n" % item
        text += "'''\n"
        return text

    def toVirtualFile( self ): return io.StringIO( unicode(str(self)) )         
    
configSettings = ConfigSettings()
