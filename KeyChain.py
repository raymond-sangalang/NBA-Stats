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
        
        if self.getCount() == self.getProbe()-1:
            self.setProbe()
        
        return checkKey      
    
    
    def createKey(self, player_name, i):
            
        return ( ( sum( [ord(n) for n in player_name] ) + ( (2**i)*(3**i) ) ) % self.getProbe() )
    
    
    def getMap(self):                     
        """ return set checkMap; set of names """
        return self.checkMap
    
    def getPlayers(self):                 
        """ return dictionary _dictPlayer; key- int key and value- string names """
        return self._dictPlayer
    
    """ getters for count and probe """
    def getCount(self):  return self.count
    def getProbe(self):  return self._STARTPROBE
    
    
    def setProbe(self): 
        """ setProbe- set value of probe increase number to have in unique keys """
        self._STARTPROBE *= 2
    
    
    def __len__(self):
        return len(self.getPlayers().keys())
    
    def __repr__(self):
        print(f"\tKeys{' '*3}Players\n\t----{' '*3}-------\n")
        for k, v in self.getPlayers():
            print(f"\t{k:5d}  ", v)
    
    
    
    
"""
if __name__ == "__main__":
    
    keyf= KeyChain()
    stringArr= ['LeBron James', 'Chris Paul', 'Stephen Curry', 'Kevin Durant', 'Anthony Davis',
                'James Harden', 'Giannis Antetokounmpo', 'Joel Embiid', 'Russell Westbrook',
                'Ryan Arcidiacono', 'Kris Dunn', 'Zach Lavine', 'Draymond Green', 'Klay Thompson',
                'Chris Paul', 'Andre Iguodala', 'Dirk Nowitzki', 'Nick Collison', 'Manu Ginobili',
                'Tim Duncan', 'LaMarcus Aldridge', 'Channing Frye', 'Kevin Love', 'Dwight Howard']
    
    for i in stringArr:
        print(keyf.addUniq(i),': ', i)
"""

