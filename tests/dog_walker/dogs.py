class Dog:                      # Define the dog species
    def __init__ (self, sound): # Constructor, named __init__, accepts provided sound
        self.sound = sound      # Stores accepted sound into self.sound field inside new dog

    def _bark (self):           # Define _bark method, not part of interface of dog
        print (self.sound)      # It prints the self.sound field stored inside this dog
        
    def escape (self):          # Define escape method
        print ('Hang head')     # The dog hangs his head
        self._bark ()           # It then calls upon its own _bark method
        self._bark ()           # And yet again
        
    def follow_me (self):       # Define escape method
        print ('Walk behind')   # The dog walks one step behind the boss
        self._bark ()           # It then calls upon its own _bark method
        self._bark ()           # And yet again