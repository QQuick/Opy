aGlobalPublicString = "A"
__aGlobalPrivateString = "B"

def aGlobalPublicFunc():
    print aGlobalPublicString
    print __aGlobalPrivateString 

def __aGlobalPrivateFunc():
    print aGlobalPublicString
    print __aGlobalPrivateString 
            
class aPublicClass :
    def __init__(self):
        self.publicStringInPublicClass="C"
        self.__privateStringInPublicClass="D"

    def publicFuncInPublicClass(self):
        self.__privateFuncInPublicClass()

    def __privateFuncInPublicClass(self):
        print self.publicStringInPublicClass
        print self.__privateStringInPublicClass
        
class __aPrivateClass :
    def __init__(self):
        self.publicStringInPrivateClass="E"
        self.__privateStringInPrivateClass="F"

    def publicFuncInPrivateClass(self):
        self.__privateFuncInPrivateClass()

    def __privateFuncInPrivateClass(self):
        print self.publicStringInPrivateClass
        print self.__privateStringInPrivateClass      

if __name__ == '__main__':
    
    aGlobalPublicFunc()
    __aGlobalPrivateFunc()
    
    pub = aPublicClass()
    print pub.publicStringInPublicClass    
    pub.publicFuncInPublicClass()
        
    priv = __aPrivateClass()
    priv.publicFuncInPrivateClass()                
    print priv.publicStringInPrivateClass    
    
            