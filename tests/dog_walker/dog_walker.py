import bosses
import dogs
       
your_dog = dogs.Dog ('Wraff')      # Instantiate dog, provide sound "Wraff" to constructor
his_dog = dogs.Dog ('Howl')        # Instantiate dog, provide sound "Howl" to constructor
        
you = bosses.NatureLover ()         # Create yourself
your_friend = bosses.CouchPotato () # Create your friend

you.walk (your_dog)                 # Interface: walk dog, implementation: going out together
your_friend.walk (his_dog)    	    # Interface: walk dog, implementation: sending dog out