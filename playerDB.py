""" Player database                              ---> DATABASE <--- 
------------------------------------------------------------------------------------------------------------------------------------"""
import sqlite3, os
import io, numpy as np
_DATABASE= '_nbaPlayer.db'


def connect_SQL():
    ''' Connect to SQL database into _nbaPlayer.db '''
    
    new_file= not os.path.exists(_DATABASE)                 # if database file doesn't exist, set as a new file
    
   
    try:
        return sqlite3.connect(_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)         # return successful connection and acquire registered 
                                                                                        #      data types, otherwise catch error 
    except sqlite3.Error as e:
        raise sqlite3.Error("ERROR:", str(e))
        
    if new_file:   
        print("Must Create Table for new file:", _DATABASE)    

        
def createTables(_conn):
    '''  Four tables created: 
              1- players years ==> same/new team, rank, and years(numpy array); linked year to table 3 ^ 4
              2- stats of player ==> games played, min/game, reb/game, wins, year, key
              3- rebs of players ==> off_rpg, def_rpg, total_rpg, year, key
              4 - player ==> first name, last name, position and key; linked primary key                      '''
    
    _cur= _conn.cursor()
    _cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Player' ''')
    
                      
    check_Tables(_cur)                              # condition: if tables exist recreate, else creating new tables
    createNewTable(_cur)
    if _cur.fetchone() != None: 
        print(f'\n\tCREATING NEW TABLES\n\t{"-"*19}\n')
        createNewTable(_cur)

    _conn.commit()                                  # save changes 

def createNewTable(_cur):
    
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
    sqlite3.register_adapter(np.ndarray, mutate_obj) 
    
    # responsible for restoring/transforming numpy array object
    sqlite3.register_converter("array", restore_obj)


def add_playersYear(_cur, team, rank, year, key):
    ''' insert function to SQL commands, inputting a players year(TABLE) by rank and team '''
    
    _cur.execute("""INSERT INTO YearOfPlayer (team, rank, year, key)
                    VALUES(?,?,?,?)""", (team, rank, year, key))
        
        
def add_stats(_cur, game_played, min_per_game, reb_per_game, wins, year, key):
    ''' Insert into inputting a players stat table by year: games played, mins/game, reb/game and wins by plus/minus scores,  '''
    
    _cur.execute("""INSERT INTO StatsOfPlayer (game_played, min_per_game, reb_per_game, wins, year, key)
            VALUES(?,?,?,?,?,?)""", (game_played, min_per_game, reb_per_game, wins, year, key))
   
   
def add_reb(_cur, off_reb_per_game, def_reb_per_game, reb_per_game, year, key):
    ''' add_reb- off_reb_per_game, def_reb_per_game, reb_per_game, year, key '''
    
    _cur.execute("""INSERT INTO RebOfPlayer (off_reb_per_game, def_reb_per_game, reb_per_game, year, key)
                VALUES(?,?,?,?,?)""", (off_reb_per_game, def_reb_per_game, reb_per_game, year, key))    
    
    
def add_Player(_conn, name, pos, key):
    ''' add_Player: inputting a new players(objects for data) with attributes by name and years played '''
    
    (first_name, last_name) = name.split(' ', 1)                                # split name for optional search values
    
    if key != -1:
        _cur= _conn.cursor()
        _cur.execute("""INSERT INTO Player (first_name, last_name, position, key)
                    VALUES(?,?,?,?)""", (first_name, last_name, pos, key))
        _conn.commit()
    
    
    
    
def add_to_tables(_conn, playerYear, player_stats, player_reb, playerObj, keyf):
    ''' add_to_tables: function taking 3 list arguments to insert into all three tables
                       as a function decorator'''
    
    _cur= _conn.cursor()
    name= playerObj[0]             # player name
    
    
    if (check_records(_cur, playerObj[0]) == None):
        """ check records to see if name(object/player) already exists in database 
                         return tuple of value or None""" 
        
        key= keyf.addUniq(name)
        add_Player(_conn, *playerObj, key)
        _conn.commit()
        
    else:
        key= keyf.getKey(name)             # get original key to use if object in records
            
            
    add_playersYear(_cur, *playerYear, key)
    _conn.commit()
    
    add_stats(_cur, *player_stats, key)
    _conn.commit()
    
    add_reb(_cur, *player_reb, key)                
    _conn.commit()
    
    
    
def check_Tables(_cur):
    ''' check_Tables- removes tables if they exists'''
    
    if _cur.fetchone()[0] != 0:                                        # check for value in table 
        _cur.execute("""DROP TABLE if exists YearOfPlayer """)   
        _cur.execute("""DROP TABLE if exists StatsOfPlayer """)  
        _cur.execute("""DROP TABLE if exists RebOfPlayer """) 
        _cur.execute("""DROP TABLE if exists Player """)     
        
        
def check_records(_cur, name):
    """ check_records- Select on query to see if specific name exists in database
                       will return bool value(values in/None) """
    
    (f_name, l_name) = name.split(' ', 1)
    
    _cur.execute("""Select last_name
                    FROM Player
                    WHERE first_name = ?  
                          AND last_name = ?""",(f_name, l_name))
    
    return _cur.fetchone()                                           # return values in or None from Select query
    
    
    
def mutate_obj(year=[]):
    """ mutate_obj- utilize io byte conversion and numpy functionality save, in order to mutate numpy array
                    object as an acceptable registered data type in the SQL database                        """
    
    outB= io.BytesIO()
    np.save(outB, year)
    outB.seek(0)
    return sqlite3.Binary(outB.read())

def restore_obj(char_year):
    """ restore_obj- utilize io byte conversion and numpy functionality load, in order to convert from mutated bytes
                     object to be loaded as a numpy array                                                            """    
    outArr= io.BytesIO()
    np.save(outArr, year)
    outArr.seek(0)
    return np.load(outArr)
