import random   # One of Python's many standard modules

import bosses
import dogs

# Create a list of random bosses
humanBeings = []                # Create an emptpy list
for index in range (10):        # Repeat the following 10 times, index running from 0 to 9
    humanBeings.append (        # Append a random HumanBeing to the list by
        random.choice ((bosses.NatureLover, bosses.CouchPotato)) () # randomly selecting its class
    )                                                               # and calling its contructor

# Let them all walk a new dog with an random sound
for humanBeing in humanBeings:  # Repeat the following for every humanBeing in the list
    humanBeing.walk (           # Call implementation of walk method for that type of humanBeing
        dogs.Dog (              # Construct a new dog as parameter to the walk method
            random.choice (     # Pick a random sound
                ('Wraff', 'Wooff', 'Howl', 'Kaii', 'Shreek') # fom this tuple of sounds
            )
        )
    )