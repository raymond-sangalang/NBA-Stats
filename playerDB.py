"""Player database- """
import sqlite3, os
from sqlite3 import Error

_DATABASE= '_nbaPlayer.db'


def connect_SQL():
    ''' Connect to SQL database into _nbaPlayer.db '''
    
    new_file= not os.path.exists(_DATABASE)
    
    try:
        
        return sqlite3.connect(_DATABASE)
    
    except Error as e:
        print("ERROR:", str(e))
    
    if new_file:
        print("Must Create Table for new file:", new_file)
        
def createTables(_conn):
    '''  Three tables created: 
              1- players years ==> same/new team and rankings; linked years
              2- stats of player ==> games played, min/game, reb/game, wins
              3- players ==> first and last name, years played               '''
    
    
    _cur= _conn.cursor()
    _cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Player' ''')
    
                      
    check_Tables(_cur)                              # condition: if tables exist recreate, else creating new tables
        
        
    _cur.execute("""CREATE TABLE YearOfPlayer
            (player_year text, team text, rank integer)""")
    
                                                    # rebound<related to def and off reb>
    _cur.execute("""CREATE TABLE StatsOfPlayer
            (game_played integer, min_per_game real,
            off_reb_per_game real, def_reb_per_game real,
            reb_per_game real, wins real)""")

                                                    # provided a creation of key for lookup
    _cur.execute("""CREATE TABLE Player
                (f_name text, l_name, year integer, key integer primary key not null)""")    
    _conn.commit() # save changes 


def add_playersYear(_cur, player_year, team, rank):
    ''' insert function to SQL commands, inputting a players year(TABLE) by rank and team '''
    
    _cur.execute("""INSERT INTO YearOfPlayer (player_year, team, rank)
                    VALUES(?,?,?)""", (player_year, team, rank))
        
    
def add_stats(_cur, game_played, min_per_game, off_reb_per_game, def_reb_per_game, reb_per_game, wins):
    ''' Insert into inputting a players stat table: games played, mins/game, reb/game and wins by plus/minus scores '''
    
    _cur.execute("""INSERT INTO StatsOfPlayer (game_played, min_per_game, off_reb_per_game, 
                                               def_reb_per_game, reb_per_game, wins)
            VALUES(?,?,?,?,?,?)""", (game_played, min_per_game, off_reb_per_game, def_reb_per_game, reb_per_game, wins))
   

    
def add_Player(_cur, name, year, keyf):
    ''' add_Player: inputting a new players(objects for data) with attributes by name and years played '''
    
    (f_name, l_name) = name.split(' ', 1)                                # split name for optional search values
    
    key = keyf.addUniq(name)
    print(f'{key:4d}: {name}')
    

    if key != -1:
        _cur.execute("""INSERT INTO Player (f_name, l_name, year, key)
                    VALUES(?,?,?,?)""", (f_name, l_name, year, key))
    else:
        update_Player(_cur, list_vals=[f_name, l_name, year])
   
    
def add_to_tables(_conn, playerYear, player_stats, playerObj, keyf):
    ''' add_to_tables: function taking 3 list arguments to insert into all three tables
                       as a function decorator'''
    
    _cur= _conn.cursor()
    
    add_playersYear(_cur, *playerYear)
    add_stats(_cur, *player_stats)
    add_Player(_cur, *playerObj, keyf)         
    
    print('\nLength of Dictionary:', len(keyf))
    ##_conn.commit()
    
    
    
def check_Tables(_cur):
    ''' check_Tables- removes tables if they exists'''
    
    if _cur.fetchone()[0] != 0:                                        # check for value in table 
        _cur.execute("""DROP TABLE if exists YearOfPlayer """)   
        _cur.execute("""DROP TABLE if exists StatsOfPlayer """)   
        _cur.execute("""DROP TABLE if exists Player """)     
    
    
    
def update_Player(_cur, list_vals= []):
    ''' update_Player: param: sql connection, tuple of first name, last name, and year'''
    
    update_p= ''' UPDATE Player
                  SET year = ? , 
                      key = ? 
                  WHERE f_name = ? , 
                        l_name = ?   '''
                                 
    key = keyf.addUniq(f"{list_vals[0]} {list_vals[1]}")
    if key != -1:
        _cur.execute( update_p, tuple( list_vals.append(key) ) ) 
