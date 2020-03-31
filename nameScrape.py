# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for data
import re, requests, sqlite3
from sqlite3 import Error
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def connect_SQL():
    try:
        return sqlite3.connect('_nbaPlayer.db')
    except Error as e:
        print("ERROR:", str(e))

def createTables(_conn):
    '''  Three tables created: 
              1- players years ==> same/new team and rankings; linked years
              2- stats of player ==> games played, min/game, reb/game, wins
              3- players ==> first and last name, years played               '''
    
    _cur= _conn.cursor()
    _cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Player' ''')
    
    if _cur.fetchone()[0] != 0:
        return   
    
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
        
        _conn= connect_SQL() # connect a database through sqlite3 into file _nbaPlayer.db 
        createTables(_conn)  # create table if do not exist
        
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

            '''generators'''
            # YearOfPlayer: name+year--team--ranking
            playerYear_entities= (f'{self.listOfNames[0]}{curr_year}', self.listOfNames[-1], int(self.listOfStats[0]))
            
            # StatsOfPlayer: games played, min/game, off rpg, def rpg, total reb/game, wins
            player_stats= (int(self.listOfStats[1]),*[float(i) for i in self.listOfStats[2:]])
            print(*list(player_stats))
            
            _conn.close() # close connection
                  
            
    def match_tag(self, _tag):
        return True if _tag and (_tag.startswith('oddrow') or _tag.startswith('evenrow')) else False
    
    def __len__(self): return len(self.listOfNames)
        



        





    
    

        
        
        
        
