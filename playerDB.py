""" Player database                              ---> DATABASE <--- 
------------------------------------------------------------------------------------------------------------------------------------"""
import sqlite3, os
import string, io, re, numpy as np

_DATABASE= '_nbaPlayer.db'

class nbaDatabase:
    def init(self):
        print("NBA PLUS-MINUS SCORES")
    
    def connect_SQL(self):
        ''' Connect to SQL database into _nbaPlayer.db '''
        
        new_file= not os.path.exists(_DATABASE)                 # if database file doesn't exist, set as a new file
        
        try:
            return sqlite3.connect(_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)         # return successful connection and acquire registered 
                                                                                            #      data types, otherwise catch error 
        except sqlite3.Error as e:
            raise sqlite3.Error("ERROR:", str(e))
            
        if new_file:   
            print("Must Create Table for new file:", _DATABASE)    
    
            
    def createTables(self, _conn):
        '''  Four tables created: 
                  1- players years ==> same/new team, rank, and years(numpy array); linked year to table 3 ^ 4
                  2- stats of player ==> games played, min/game, reb/game, wins, year, key
                  3- rebs of players ==> off_rpg, def_rpg, total_rpg, year, key
                  4- player ==> first name, last name, position and key; linked primary key                      '''
        
        _cur= _conn.cursor()
        _cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Player' ''')
           
        self.check_Tables(_cur)                                  # condition: if tables exist recreate, else creating new tables
        self.createNewTable(_cur)
            
        if _cur.fetchone() != None: 
            print(f'\n\tCREATING NEW TABLES\n\t{"-"*19}\n')
            self.createNewTable(_cur)
    
        _conn.commit()                                       # save changes 
    
    
    def createNewTable(self, _cur):
        
        _cur.execute("""CREATE TABLE YearOfPlayer
                (team text, rank integer, year array, key integer not null)""")
                                                            
        _cur.execute("""CREATE TABLE StatsOfPlayer
                (game_played integer, min_per_game real, reb_per_game real, 
                 wins real, year, key integer not null)""")                   
        
        _cur.execute("""CREATE TABLE RebOfPlayer
                (off_reb_per_game real, def_reb_per_game real, reb_per_game real, 
                 year, key integer not null)""")                                        # reb/game(off ^ def) --- sort by key ^ year    
    
        _cur.execute("""CREATE TABLE Player
                    (first_name text, last_name text, position text, key integer primary key not null)""")    
        
    
        # responsible for serializing data of (array / numpy array) --> storing as bytes for sql compatibility
        sqlite3.register_adapter(np.ndarray, self.mutate_obj) 
        
        # responsible for restoring/transforming numpy array object
        sqlite3.register_converter("array", self.restore_obj)
    
    
    def add_playersYear(self, _cur, team, rank, year, key):
        ''' insert function to SQL commands, inputting a players year(TABLE) by rank and team '''
        
        _cur.execute("""INSERT INTO YearOfPlayer (team, rank, year, key)
                        VALUES(?,?,?,?)""", (team, rank, year, key))
            
            
    def add_stats(self, _cur, game_played, min_per_game, reb_per_game, wins, year, key):
        ''' Insert into inputting a players stat table by year: games played, mins/game, reb/game and wins by plus/minus scores,  '''
        
        _cur.execute("""INSERT INTO StatsOfPlayer (game_played, min_per_game, reb_per_game, wins, year, key)
                VALUES(?,?,?,?,?,?)""", (game_played, min_per_game, reb_per_game, wins, year, key))
       
       
    def add_reb(self, _cur, off_reb_per_game, def_reb_per_game, reb_per_game, year, key):
        ''' add_reb- off_reb_per_game, def_reb_per_game, reb_per_game, year, key '''
        
        _cur.execute("""INSERT INTO RebOfPlayer (off_reb_per_game, def_reb_per_game, reb_per_game, year, key)
                    VALUES(?,?,?,?,?)""", (off_reb_per_game, def_reb_per_game, reb_per_game, year, key))    
        
        
    def add_Player(self, _conn, name, pos, key):
        ''' add_Player: inputting a new players(objects for data) with attributes by name and years played '''
        
        (first_name, last_name) = name.split(' ', 1)                                # split name for optional search values
        
        if key != -1:
            _cur= _conn.cursor()
            _cur.execute("""INSERT INTO Player (first_name, last_name, position, key)
                        VALUES(?,?,?,?)""", (first_name, last_name, pos, key))
            _conn.commit()
        
        
        
        
    def add_to_tables(self, _conn, playerYear, player_stats, player_reb, playerObj, keyf):
        ''' add_to_tables: function taking 3 list arguments to insert into all three tables
                           as a function decorator'''
        
        _cur= _conn.cursor()
        name= playerObj[0]             # player name
        
        
        if (self.check_records(_cur, playerObj[0]) == None):
            """ check records to see if name(object/player) already exists in database 
                             return tuple of value or None""" 
            
            key= keyf.addUniq(name)
            self.add_Player(_conn, *playerObj, key)
            _conn.commit()
            
        else:
            key= keyf.getKey(name)             # get original key to use if object in records
                
                
        self.add_playersYear(_cur, *playerYear, key)
        _conn.commit()
        
        self.add_stats(_cur, *player_stats, key)
        _conn.commit()
        
        self.add_reb(_cur, *player_reb, key)                
        _conn.commit()
        
        
        
    def check_Tables(self, _cur):
        ''' check_Tables- removes tables if they exists'''
        
        if _cur.fetchone()[0] != 0:                                        # check for value in table 
            _cur.execute("""DROP TABLE if exists YearOfPlayer """)   
            _cur.execute("""DROP TABLE if exists StatsOfPlayer """)  
            _cur.execute("""DROP TABLE if exists RebOfPlayer """) 
            _cur.execute("""DROP TABLE if exists Player """)     
            
            
    def check_records(self, _cur, name):
        """ check_records- Select on query to see if specific name exists in database
                           will return bool value(values in/None) """
        
        (f_name, l_name) = name.split(' ', 1)
        
        _cur.execute("""Select last_name
                        FROM Player
                        WHERE first_name = ? COLLATE NOCASE
                              AND last_name = ? COLLATE NOCASE""",(f_name, l_name))
        
        return _cur.fetchone()                                           # return values in or None from Select query
        
        
        
    def mutate_obj(self, year=[]):
        """ mutate_obj- utilize io byte conversion and numpy functionality save, in order to mutate numpy array
                        object as an acceptable registered data type in the SQL database                        """
        
        outB= io.BytesIO()
        np.save(outB, year)
        outB.seek(0)
        return sqlite3.Binary(outB.read())
    
    
    def restore_obj(self, char_year):
        """ restore_obj- utilize io byte conversion and numpy functionality load, in order to convert from mutated bytes
                         object to be loaded as a numpy array                                                            """    
        
        outArr= io.BytesIO()
        np.save(outArr, char_year)
        outArr.seek(0)
        return np.load(outArr)
    
    
    
    """ ----------------------------------------------------------------------------------------------------------------
        Player (first_name text, last_name text, position text, key integer primary key not null)
        YearOfPlayer (team text, rank integer, year array, key integer not null) 
        StatsOfPlayer (game_played integer, min_per_game real, reb_per_game real, wins real, year, key integer not null)
        RebOfPlayer (off_reb_per_game real, def_reb_per_game real, reb_per_game real, year, key integer not null)        
        ---------------------------------------------------------------------------------------------------------------- """
    
    
    def search_player(self, _conn): 
        """ Player (first_name text, last_name text, position text, key integer primary key not null)                        """   
        
        _cur= _conn.cursor()
    
        l_name= input("Enter Last Name of player: ").replace(" ", '')
        
        _cur.execute("""Select * FROM Player
                         WHERE last_name = ?""",(string.capwords(l_name),))   
        player_info= _cur.fetchall()
        
        if ( player_info == None ):
            print("Sorry, couldn't find a match")  
            
        else:
            print("\n\nPlayers Found:\n")
            for row in player_info:
                print(f'\t{" ".join(row[:2])}, {row[-2]}')
                
        return
    
    
    def search_YearOfPlayer(self, _conn):
        """ YearOfPlayer (team text, rank integer, year array, key integer not null)  """
    
        _cur= _conn.cursor()
        name = self.getName().split()
        
        if not self.check_records(_cur, ' '.join(name)):
            print("player does not exist")
            
        else:
            
            _cur.execute("""Select * FROM Player
                             WHERE last_name = ? COLLATE NOCASE AND first_name = ? COLLATE NOCASE""",(name[-1],name[0],))   
            player_info= _cur.fetchone()        
            
            _cur.execute("""Select * FROM YearOfPlayer
                             WHERE key = ?""",(player_info[-1],))    
            player_year= _cur.fetchall()
            
            
            
            print( f"\n\t{' '.join(name)}'s overall years:\n" )
            print( 'Year:\t', f"{'Team:':<24}Rank:" )   
            
            for played in player_year:
                year=int(re.sub("[^0-9]", "",str(self.restore_obj(played[-2]))))
                print(f'{year}\t', ' '.join([f"{str(i):<23}" for i in list(played[:-2])]))   
    
        return
        
        
    def search_StatsOfPlayer(self, _conn):
        """ StatsOfPlayer (game_played integer, min_per_game real, reb_per_game real, wins real, year, key integer not null)  """
        
        _cur= _conn.cursor()
        name = self.getName().split()
        
        if not self.check_records(_cur, ' '.join(name)):
            print("player does not exist")
            
        else:
            _cur.execute("""Select * FROM Player
                             WHERE last_name = ? COLLATE NOCASE AND first_name = ? COLLATE NOCASE""",(name[-1],name[0],))   
            player_info= _cur.fetchone()        
           
            _cur.execute("""Select * FROM StatsOfPlayer
                             WHERE key = ?""",(player_info[-1],))    
            player_stats=_cur.fetchall()
           
            sp, da = ' ', '-'
            print(f"\n\t{' '.join(name)}'s overall plus-minus stats per year:\n" +
                     f'Year{sp*8}GP  MPG   RPG   WINS\n{da*4+sp*8+da*2+sp*2+da*4+sp+da*5+sp+da*5}' )   
            
            for stats in player_stats:
                print(f'{stats[-2]}\t', ' '.join([f"{str(i):>5}" for i in list(stats[:-2])]))    
     
        return
    
    
    
    def search_RebOfPlayer(self, _conn):
        """ RebOfPlayer (off_reb_per_game real, def_reb_per_game real, reb_per_game real, year, key integer not null)  """
       
        _cur= _conn.cursor()
        name = self.getName().split()
        
        if not self.check_records(_cur, ' '.join(name)):
            print("player does not exist")
            
        else:
            dash= "-"*5
            
            _cur.execute("""Select * FROM Player
                             WHERE last_name = ? COLLATE NOCASE AND first_name = ? COLLATE NOCASE""",(name[-1],name[0],))    
            player_info= _cur.fetchone()[-1]        
           
            _cur.execute("""Select * FROM RebOfPlayer
                             WHERE key = ?""",(player_info,))    
            player_reb=_cur.fetchall()
            
            print(f"\n\t{' '.join(name)}'s overall plus-minus rebs per year:\n" + 
                          f'Year \t', f'OFF{" "*3}DEF\n{dash}\t {dash+" "+dash}')
            for reb in player_reb:
                print(f'{reb[-2]}:\t', ' '.join([f"{str(i):>5}" for i in list(reb[:-3])]))    
    
        return
    
    
    
    
    
    def getName(self):
        
        f_name= input("Enter First Name of player: ").replace(" ", '')
        l_name= input("Enter Last Name of player: ").replace(" ", '')
        return string.capwords(f_name + ' ' + l_name)
    
    
    def getYearsOfPlayer(self, _conn):
        _cur= _conn.cursor()
        name = self.getName().split()
        
        if not check_records(_cur, ' '.join(name)):
            print("player does not exist")
            
        else:
            
            _cur.execute("""Select * FROM YearOfPlayer
                             WHERE last_name = ? COLLATE NOCASE AND first_name = ? COLLATE NOCASE""",(name[-1],name[0],))    
            player_year= _cur.fetchall()
    
            print ( player_year )
        
        return [int(re.sub( "[^0-9]", "", str( self.restore_obj(played[-2]) ) )) for played in player_year]  
    
    
    
    
      
    def update_Player(self, _cur, tup_vals= ()):
        ''' update_Player: param: sql connection, tuple of first name, last name, and position'''
    
        update_p= f''' UPDATE Player
                      SET position = ? , 
                          key = ? 
                      WHERE first_name = {tup_vals[0]} , 
                            last_name = {tup_vals[1]}   '''
        key = tup_vals[-1]                            
    
        while key != -1:
            key = keyf.addUniq(f"{tup_vals[0]} {tup_vals[1]}")
            
        tup_vals= list(tup_vals[0:3]).append(key)                         # add new key with first 3 values: f_name, l_name, year
        _cur.execute(update_p,tuple(tup_vals))                            # pass list as tuple for update

