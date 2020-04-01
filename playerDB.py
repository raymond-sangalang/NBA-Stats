"""Player database- """
import sqlite3
from sqlite3 import Error

def connect_SQL():
    ''' Connect to SQL database into _nbaPlayer.db '''
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
    
    if _cur.fetchone()[0] != 0:                    # condition: if tables exist return, else move on to creating them 
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


def add_playersYear(_cur, player_year, team, rank):
    ''' insert function to SQL commands, inputting a players year(TABLE) by rank and team '''
    
    _cur.execute("""INSERT INTO YearOfPlayer (player_year, team, rank)
                    VALUES(?,?,?)""", (player_year, team, rank))
    #_conn.commit() # save changes     
    
def add_stats(_cur, game_played, min_per_game, off_reb_per_game, def_reb_per_game, reb_per_game, wins):
    ''' Insert into inputting a players stat table: games played, mins/game, reb/game and wins by plus/minus scores '''
    
    _cur.execute("""INSERT INTO StatsOfPlayer (game_played, min_per_game, off_reb_per_game, 
                                               def_reb_per_game, reb_per_game, wins)
            VALUES(?,?,?,?,?,?)""", (game_played, min_per_game, off_reb_per_game, def_reb_per_game, reb_per_game, wins))
    #_conn.commit() # save changes 
    
def add_Player(_cur, name, year, key=0):
    ''' add_Player: inputting a new players(objects for data) with attributes by name and years played '''
    
    _cur.execute("""INSERT INTO Player (name, year, key)
                    VALUES(?,?,?)""", (name, year, key))
    #_conn.commit() # save changes
    
def add_to_tables(_conn, playerYear, player_stats, playerObj):
    
    ''' add_to_tables: function taking 3 list arguments to insert into all three tables
                       as a function decorator'''
    _cur= _conn.cursor()
    add_playersYear(_cur, *playerYear)
    add_stats(_cur, *player_stats)
    add_Player(_cur, *playerObj)         #still need to create key
    _conn.commit()
