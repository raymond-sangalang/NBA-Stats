''' KeyChain.py
for each player, they will contain their own individual (unique) key
    Key utilized for the join of tables in SQL
        - create key algorithm; condition if key already exists
        - search for key in output file with player names and key
'''


class KeyChain:
    """ start chaining with initial prime number mod and keep count, then
        increment probe """
    _STARTPROBE= 13 
    count= 0 
    
    def __init__(self):   
        """ Constructor- contains a dictionary with integer keys associated name values,
                         checkMap set holds names to evaluate one user (one-to-one functionality) """
        self._dictPlayer= {}
        self.checkMap= set()
        
    
    def addUniq(self, player_name):
        """ addUniq: function searches for a unique number for a given player; checks if already in set of names
                          and loops to until a number is unique in the dictionary keys"""
        checkKey= -1
        
        if player_name in self.getMap():
            return -1

        else:
            self.getMap().add(player_name)
            trial= 1
            _Done= False
            
            while not _Done:
                ''' loop and call createKey until value is unique in player dictionary'''
                checkKey= self.createKey(player_name, i= trial)
                
                # check if key is a positive and unique integer
                if checkKey not in self.getPlayers().keys() and checkKey > 0:
                    _Done = True
                    
                trial += 1   
        
        self.count= self.getCount() + 1
        self.getPlayers()[checkKey]= player_name
        
        if self.getCount() == self.getProbe()-3:
            self.setProbe()
        
        return checkKey      
    
    
    def createKey(self, player_name, i=0):
        """ createKey- adds all letters in players name by ascii values and adds multiple of
                            prime factors + number trial, then mod probe; this provides a 
                            limitation to a number separation in keys                        """
        
        asciName= sum( [ord(n) for n in player_name] )
        return ( (asciName + ( (2**i)*(3**i) ) + i ) % self.getProbe() )
    
    
    def getMap(self):                     
        """ return set checkMap; set of names """
        return self.checkMap
    
    def getPlayers(self):                 
        """ return dictionary _dictPlayer; key- int key and value- string names """
        return self._dictPlayer
    
    """ getters for count and probe """
    def getCount(self):  return self.count
    def getProbe(self):  return self._STARTPROBE
    
    def getKey(self, name):
        ''' search dictionary values for associated name and return key '''
        
        for key, val in self.getPlayers().items():
            if val == name:
                return key
            
    
    
    def setProbe(self): 
        """ setProbe- set value of probe increase number to have in unique keys """
        self._STARTPROBE *= 2
    
    
    def __len__(self):
        return len(self.getPlayers().keys())
    
    def __repr__(self):
        print(f"\tKeys{' '*3}Players\n\t----{' '*3}-------\n")
        for k, v in self.getPlayers():
            print(f"\t{k:5d}  ", v)
