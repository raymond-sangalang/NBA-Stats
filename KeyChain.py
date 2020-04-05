# Create KeyChain
'''
for each player, they will contain their own individual (unique) key
    Key utilized for the join of tables in SQL
        - create key algorithm; condition if key already exists
        - search for key in output file with player names and key
        - 
'''

_DEFAULTFILE= "playerKey.txt"

class KeyChain:
    """ start chaining with initial prime number mod and keep count, then
        increment probe """
    _STARTPROBE= 13 
    count= 0    
    
    def __init__(self):   
        self._dictPlayer= {}

        
    def addUniq(self, player_name):
        
        _Done= False
        checkKey= -1        
        
        if player_name not in self._dictPlayer.values():
            trial= 1
            
            while not _Done:
                checkKey= self.createKey(player_name, i= trial)
                
                if checkKey not in self._dictPlayer.keys() and checkKey > 0:
                    _Done = True
                    
                trial += 1   
        
        if self.count == (self._STARTPROBE - 3):
            self._STARTPROBE *= 2
            
        self._dictPlayer[checkKey]= player_name
        self.count += 1
        return checkKey      
    
    
    def createKey(self, player_name, i):
            
        return ( ( sum( [ord(n) for n in player_name] ) + ( (2**i)*(3**i) ) ) % self._STARTPROBE )
    
    """    
    def searchKey(self): pass
    
    def getKey(self, player_name):
        ''' search key given player name'''
        pass
    """
    
    def __len__(self):
        return len(self._dictPlayer.keys())
    
    

if __name__ == "__main__":
    
    keyf= KeyChain()
    stringArr= ['LeBron James', 'Chris Paul', 'Stephen Curry', 'Kevin Durant', 'Anthony Davis',
                'James Harden', 'Giannis Antetokounmpo', 'Joel Embiid', 'Russell Westbrook',
                'Ryan Arcidiacono', 'Kris Dunn', 'Zach Lavine', 'Draymond Green', 'Klay Thompson',
                'Chris Paul', 'Andre Iguodala', 'Dirk Nowitzki', 'Nick Collison', 'Manu Ginobili',
                'Tim Duncan', 'LaMarcus Aldridge', 'Channing Frye', 'Kevin Love', 'Dwight Howard']
    
    for i in stringArr:
        print(keyf.addUniq(i),': ', i)

