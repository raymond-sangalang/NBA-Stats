# Create KeyChain
'''
for each player, they will contain their own individual (unique) key
    Key utilized for the join of tables in SQL
        - create key algorithm; condition if key already exists
        - search for key in output file with player names and key
        - 
'''
import re
_DEFAULTFILE= "playerKey.txt"

class KeyChain:
    """ start chaining with initial prime number mod and keep count, then
        increment probe """
    
    _STARTPROBE= 13 
    count= 0
    
    def __init__(self, player_name):
        self._dictPlayer= {}
        _Done= False
        checkKey= -1
        
        
    
    def createKey(self, player_name, i= 0):
        
        newKey= None
        uniqVal= False

        nameVal= ( ( sum( [ord(i) for i in player_name] ) + ( (2**i)*(3**i) ) ) % self._STARTPROBE )
            
        return newKey
    
    def addUniq(self, player_name, findKey):
        
        if player_name not in _dictPlayer.values():
            trial= 1
            while not Done:
                checkKey= self.createKey(player_name, i= trial)
                if checkKey not in _dictPlayer.keys():
                    _Done = True
                trial += 1   
        
        if self.count == self._STARTPROBE:
            self._STARTPROBE *= 2
        _dictPlayer[checkKey]= player_name
               
        
        return checkKey  
        
        
    
    def searchKey(self):
        pass
    
    def getKey(self, player_name):
        ''' search key given player name'''
        pass
    
    def __len__(self):
        return len(self._dictPlayer.keys())
