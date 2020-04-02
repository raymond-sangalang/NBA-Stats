# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for data

import re, requests, playerDB
import playerDB as _pDB
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


_TEAMFILE= "team_file.csv"

class Name:

    def __init__(self, _fileName=''):
        ''' Constructor- requests(interface)  '''
        
        
        curr_year= re.search("(20[\d]+)",_fileName)[0]      #current year    
        self.players = {}
        self.listOfStats = []     # listOfStats --> rank, game played, min/game, off-reb/game, def-reb/game, reb/game, wins
        
        
        _conn= _pDB.connect_SQL() # connect a database through sqlite3 into file _nbaPlayer.db 
        _pDB.createTables(_conn)  # create table if do not exist

            
        content= requests.get(_fileName)                 # creates HTML page object from request
        content.raise_for_status()
        
        soup= BeautifulSoup(content.text,'html.parser')              # flexible HTML parser-BeautifulSoup-gets python byte string from request obj
        table= soup.find('table', {'class': 'tablehead'})

        
        for tr in table.find_all('tr', {'class': self.match_tag}):
            
            _string= str([td.text for td in tr.find_all('td')])              # get and list all subclasses, td, and string for searching
            self.listOfStats= re.findall('-?\d+(?:\.\d+)?', _string)
            
            newsoup= str( tr.find('a') )                                       # subclass 'a' contains name, position, team and link to player                       
            name=re.search( "(?<=>)(.+)<" , newsoup ).group(1)                 #
            fname, lname = tuple( name.split(' ', 1) )                         # split into first and last name of player
            
            pos = re.search(', (\w{1,2})', _string).group(1)     ## position
            team = re.findall('[A-Z]{2,3}',_string)[-1]              ## team
            
            self.players[fname+' '+lname] = [ pos, *self.listOfStats ]

            print(f"{f'{fname} {lname} {pos} {team}':30s} ==> {', '.join([str(i) for i in self.listOfStats])}\n")
            
            
            ''' Set Values for tables'''
            # YearOfPlayer entities: name+year--team--ranking
            playerYear= (f"{fname+' '+lname}{curr_year}", team, int(self.listOfStats[0]))
            
            # StatsOfPlayer: games played, min/game, off rpg, def rpg, total reb/game, wins
            player_stats= (int(self.listOfStats[1]),*[float(i) for i in self.listOfStats[2:]])
    
            
            # Player attributes/entities: name(first and last), basketball position, and unique Key
            ''' ****_come back to creating key class_****   ****_Split name_****might be useful in search '''
 
            playerObj= [fname+' '+lname, pos]                   
        
            '''  Inserting values into the tables- 1) playersYear  2) StatsOfPlayer  3) Player  '''
            _pDB.add_to_tables(_conn, playerYear, player_stats, playerObj)
   

        _conn.close() # close connection 
 
            
            

 
            
            
    def match_tag(self, _tag):
        '''match_tag:  boolean return utilized for search in web parsing'''
        return True if ( _tag and ( _tag.startswith('oddrow')  or  _tag.startswith('evenrow') ) ) else False
    
    
    def __len__(self): 
        ''' returned of contained value in object '''
        return len(self.players)



        





    
    

        
        
        
        
