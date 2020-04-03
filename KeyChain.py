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
        _dictPlayer= {}
        _Done= False
        checkKey= -1
        
        if player_name not in _dictPlayer.values():
            trial= 1
            while not Done:
                checkKey= self.createKey(player_name, i= trial)
                if checkKey not in _dictPlayer.keys():
                    _Done = True
                trial += 1

            
        
        '''
        try:
            
            with open(_DEFAULTFILE,"r") as f_parser:
                # open file to read if value is already taken and same name doesnt occur 
                
                lines= f_parser.readlines().rstrip('\n')
                while not _Done:
                    
                    checkKey= self.createKey(player_name)
                    for line in lines:
                        
                        if re.search( str(checkKey), line):
                            break
                        elif re.search(player_name, line):
                            break
                    if line == "":
                        _Done= True
                        findKey= checkKey               # set new value to add to file
                        self.count += 1                 # increment counter
                          
                        
        except FileNotFoundError: 
            raise FileNotFoundError(f"Can't Find {_DEFAULTFILE}")
        except ValueError:
            print("File content invalid")
        except RuntimeError as e:
            print("ERROR:", str(e))
        '''
        
            
        if self.count == self._STARTPROBE:
            self._STARTPROBE *= 2
        _dictPlayer[checkKey]= player_name
        return checkKey
        
    
    def createKey(self, player_name, i= 0):
        
        newKey= None
        uniqVal= False

        nameVal= ( ( sum( [ord(i) for i in player_name] ) + ( (2**i)*(3**i) ) ) % self._STARTPROBE )
            
        return newKey
    
    def addUniq(self, player_name, findKey):
        
        
        with open(_DEFAULTFILE) as f_parser:
            lines= [line.split('\s')  for line in f_parser]
            
        outFile= open(_DEFAULTFILE, 'w')
        for line in sorted(lines, key=itemgetter(3)):
            outFile.write()
            
        
        
    
    def searchKey(self):
        pass
    
    def getKey(self, player_name):
        ''' search key given player name'''
        pass