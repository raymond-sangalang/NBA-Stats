# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for data
import re, requests, sqlite3
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

def createTables():
    '''  Three tables created: 
              1- players years ==> same/new team and rankings; linked years
              2- stats of player ==> games played, min/game, reb/game, wins
              3- players ==> first and last name, years played               '''
    
    _cur.execute("""CREATE TABLE YearOfPlayer
            (player_year text, team text, rank integer)""")
    _conn.commit() # save changes 
    
                                                    # rebound<related to def and off reb>
    _cur.execute("""CREATE TABLE StatsOfPlayer
            (game_played integer, min_per_game real,
            off_reb_per_game real, def_reb_per_game real,
            reb_per_game real, wins real)""")
    _conn.commit() # save changes 
                                                    # provided a creation of key for lookup
    _cur.execute("""CREATE TABLE Player
            (name text, year integer, key integer)""")
    _conn.commit() # save changes 


def add_playersYear(player_year, team, rank):
    ''' insert function to SQL commands, inputting a players year(TABLE) by rank and team '''
    
    _cur.execute("""INSERT INTO YearOfPlayer (player_year, team, rank)
                    VALUES(?,?,?)""", (player_year, team, rank))
    _conn.commit() # save changes     
    
def add_stats(game_played, min_per_game, off_reb_per_game, def_reb_per_game, reb_per_game, wins):
    ''' Insert into inputting a players stat table: games played, mins/game, reb/game and wins by plus/minus scores '''
    
    _cur.execute("""INSERT INTO StatsOfPlayer (game_played, min_per_game, off_reb_per_game, 
                                               def_reb_per_game, reb_per_game, wins)
            VALUES(?,?,?,?,?)""", (game_played, min_per_game, off_reb_per_game, def_reb_per_game, reb_per_game, wins))
    _conn.commit() # save changes 
    
def add_Player(name, year, key):
    ''' add_Player: inputting a new players(objects for data) with attributes by name and years played '''
    
    _cur.execute("""INSERT INTO Player (name, year, key)
                    VALUES(?,?,?)""", (name, year, key))
    _conn.commit() # save changes     
    

str_pattern= re.compile("[^\s\"\d,'/][a-zA-Z\.\-\s]+")      # regex pattern to obtain values of name, position and team.

class Name:

    def __init__(self, _fileName=''):
        ''' Constructor- requests(interface)  '''
        
        curr_year= re.search("(20[\d]+)",_fileName)[0]      #current year    
        self.players = {}
        self.listOfNames, self.listOfStats = [], []      # listOfNames --> player name, team, and position
                                                         # listOfStats --> rank, game played, min/game, off-reb/game, def-reb/game, reb/game, wins        
        
        _conn= sqlite3.connect('_nbaPlayer.db') # connect a database through sqlite3 into file _nbaPlayer.db 
        _cur= _conn.cursor()  
        
        _cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Player' ''')
        if _cur.fetchone()[0] == 0:
            createTables()
            
        content= requests.get(_fileName)                 # creates HTML page object from request
        content.raise_for_status()
        
        soup= BeautifulSoup(content.text,'html.parser')              # flexible HTML parser-BeautifulSoup-gets python byte string from request obj
        table= soup.find('table', {'class': 'tablehead'})

        for tr in table.find_all('tr', {'class': self.match_tag}):
            self.listOfStats= re.findall('\d+(?:\.\d+)?', str([td.text for td in tr.find_all('td')]))
            self.listOfNames= re.findall(str_pattern, str([td.text for td in tr.find_all('td')]))
            self.players[self.listOfNames[0]]= self.listOfNames[1:]+self.listOfStats

            print(f"{', '.join([str(i) for i in self.listOfNames]):30s} ==> {', '.join([str(i) for i in self.listOfStats])}\n")
            
        '''print(f"Name {' '*25} Stats")
        for k, v in self.players.items():
            print(f"{k:30s} {', '.join(list(v))}")'''
        '''
        if len(self.listOfNames) != 0:
            print(_fileName)
            for _init, _stat in zip(self.listOfNames, self.listOfStats):
                print(f"{', '.join(_init.split()):30s} ==> {', '.join([str(_s) for _s in _stat])}")
            #print(f"{', '.join([str(i) for i in self.listOfNames]):30s} ==> {', '.join([str(i) for i in self.listOfStats])}\n")'''
 
            
            
    def match_tag(self, _tag):
        return True if _tag and (_tag.startswith('oddrow') or _tag.startswith('evenrow')) else False
    
    def __len__(self): return len(self.listOfNames)
        



        





    
    

        
        
        
        
