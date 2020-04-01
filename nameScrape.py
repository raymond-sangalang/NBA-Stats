# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for data

import re, requests, playerDB
import playerDB as _pDB
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

_TEAMFILE= "team_file.csv"
str_pattern= re.compile("[^\s\"\d,'/][a-zA-Z\.\-\s]+")


 
class Name:

    def __init__(self, _fileName=''):
        ''' Constructor- requests(interface)  '''
        
        
        curr_year= re.search("(20[\d]+)",_fileName)[0]      #current year    
        self.players = {}
        self.listOfNames, self.listOfStats = [], []      # listOfNames --> player name, team, and position
                                                         # listOfStats --> rank, game played, min/game, off-reb/game, def-reb/game, reb/game, wins        
        
        _conn= _pDB.connect_SQL() # connect a database through sqlite3 into file _nbaPlayer.db 
        _pDB.createTables(_conn)  # create table if do not exist
            
        content= requests.get(_fileName)                 # creates HTML page object from request
        content.raise_for_status()
        
        soup= BeautifulSoup(content.text,'html.parser')              # flexible HTML parser-BeautifulSoup-gets python byte string from request obj
        table= soup.find('table', {'class': 'tablehead'})

        for tr in table.find_all('tr', {'class': self.match_tag}):
            
            self.listOfStats= re.findall('\d+(?:\.\d+)?', str([td.text for td in tr.find_all('td')]))
            self.listOfNames= re.findall(str_pattern, str([td.text for td in tr.find_all('td')]))
            self.players[self.listOfNames[0]]= self.listOfNames[-1:]+self.listOfStats

            print(f"{', '.join([str(i) for i in self.listOfNames]):30s} ==> {', '.join([str(i) for i in self.listOfStats])}\n")
            
            
            ''' Set Values for tables'''
            # YearOfPlayer entities: name+year--team--ranking
            playerYear= (f'{self.listOfNames[0]}{curr_year}', self.listOfNames[-1], int(self.listOfStats[0]))
            
            # StatsOfPlayer: games played, min/game, off rpg, def rpg, total reb/game, wins
            player_stats= (int(self.listOfStats[1]),*[float(i) for i in self.listOfStats[2:]])
            
            # Player attributes/entities: name(first and last), basketball position, and unique Key
            ''' ****_come back to creating key class_****   ****_Split name_****might be useful in search '''
            playerObj= [self.listOfNames[0], self.listOfNames[-1]]                   #print(self.listOfNames[0].split())
            
            
            '''  Inserting values into the tables- 1) playersYear  2) StatsOfPlayer  3) Player  '''
            _pDB.add_to_tables(_conn, playerYear, player_stats, playerObj)




        _conn.close() # close connection
            
            

 
            
            
    def match_tag(self, _tag):
        
        return True if ( _tag and ( _tag.startswith('oddrow')  or  _tag.startswith('evenrow') ) ) else False
    
    
    def __len__(self): return len(self.listOfNames)
    



        





    
    

        
        
        
        
