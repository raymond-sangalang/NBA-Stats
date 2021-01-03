""" Player database                              ---> DATABASE <--- 
---------------------------------------------------------------------------------------"""
import sqlite3, os
import string, io, re, numpy as np
from sqlite3 import Error
from player import Player
from team import Team


def restore_obj(char_year):
    """ restore_obj- utilize io byte conversion and numpy functionality load, in order to convert from
                        mutated bytes object loaded as a numpy array.                                  """

    outArr = io.BytesIO()
    np.save(outArr, char_year)
    outArr.seek(0)
    return np.load(outArr)


def mutate_obj(year=[]):
    """ mutate_obj- utilize io byte conversion and numpy functionality save, in order to mutate numpy array
                    object as an acceptable registered data type in the SQL database                        """

    outB = io.BytesIO()
    np.save(outB, year)
    outB.seek(0)
    return sqlite3.Binary(outB.read())


class nbaDatabase:
    __DBFILE = '_nbaPlayer.db'
    _TABLES = ["YearOfPlayer", "StatsOfPlayer", "RebOfPlayer", "Player"]

    def __init__(self, dbFile="", sqlConn=""):

        self.dbDict = {tab: [] for tab in self._TABLES}
        dbFile = dbFile if (not dbFile) else self.__DBFILE

        self.__db_connect = sqlite3.connect(dbFile, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.__db_connect.cursor()

    def getData(self):
        self.connect_SQL()
        result = self.selectAll()
        self.__disconnect__()
        return result

    def createTeams(self, rosterCount=0):
        """ Creating Team """

        newTeam = Team()
        count = 0

        while count < rosterCount:

            playerData = self.getPlayerInfo()

            if not playerData:
                print("Invalid Entry")
            else:
                newTeam.addPlayer(playerData)
                count += 1

        self.__disconnect__()
        return newTeam


    def getPlayerInfo(self):
        """ Player (first_name text, last_name text, position text, key integer primary key not null) """

        name = self.getName.split()

        if not self.check_records(' '.join(name)):
            return None

        player_info = list(self.selectByName(name))
        stats = {}

        self.cur.execute("""Select key FROM Player
                         WHERE last_name = ? COLLATE NOCASE AND first_name = ? COLLATE NOCASE""",
                         (name[-1], name[0],))
        searchKey = self.cur.fetchone()

        years = self.restoreYears(player_info)

        self.cur.execute("""Select min_per_game, reb_per_game, wins 
                        FROM StatsOfPlayer
                        WHERE key = ?""", searchKey)      # for i in yearsList
        statList = self.cur.fetchall()



        for year, stat in zip(years, statList):
            stats[year] = list(stat)

        newplayer = Player(' '.join(player_info[:2]))
        newplayer.setStats(years, stats)
        return newplayer


    """             Context Manager to close cursor and connection (handle cursor instance variable)                 """
    ####################################################################################################################
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Allows execution on (with object)"""
        self.cur.close()
        if isinstance(exc_val, Exception):
            self.__db_connect.rollback()
        else:
            self.__db_connect.commit()
        self.__db_connect.close()

    def __del__(self):
        self.__db_connect.close()

    def __disconnect__(self):
        self.__db_connect.close()

    def commit(self):
        self.__db_connect.commit()

    def connect_SQL(self):
        """ Connect to SQL database into _nbaPlayer.db, returning successful connection and
            acquire registered data types. Check existence of file, otherwise set new file """

        try:
            self.__db_connect = sqlite3.connect(self.__DBFILE, detect_types=sqlite3.PARSE_DECLTYPES)
            self.cur = self.__db_connect.cursor()


        except Error as e:
            raise Error("ERROR:", str(e))


    def check_Tables(self):
        """ check_Tables- removes tables if they exists"""
        return False if not self.cur.fetchone() else True




    def selectAll(self):
        if not self.cur.fetchone():
            return

        return [f"{i}\n"+self.cur.execute("Select * FROM " + i) for i in self._TABLES]

    def check_records(self, name):
        """ check_records- Select on query to see if specific name exists in database
                           will return bool value(values in/None) """

        (f_name, l_name) = name.split(' ', 1)

        self.cur.execute("""Select * FROM Player WHERE first_name = ? COLLATE NOCASE
                              AND last_name = ? COLLATE NOCASE""", (f_name, l_name))

        return self.cur.fetchone()  # return values in or None from Select query

    def createTables(self):
        """  Four tables created:
                  1- players years ==> same/new team, rank, and years(numpy array); linked year to table 3 ^ 4
                  2- stats of player ==> games played, min/game, reb/game, wins, year, key
                  3- rebs of players ==> off_rpg, def_rpg, total_rpg, year, key
                  4- player ==> first name, last name, position and key; linked primary key                      """

        self.connect_SQL()
        self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Player' ''')

        if not self.check_Tables():
            print(f'\n\tCREATING NEW TABLES\n\t{"-" * 19}\n')
            self.createNewTable()
            self.commit()

        self.__disconnect__()

    def createNewTable(self):


        self.cur.execute("""CREATE TABLE IF NOT EXISTS YearOfPlayer
                (team text, rank integer, year array, key integer not null)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS StatsOfPlayer
                (game_played integer, min_per_game real, reb_per_game real, 
                 wins real, year, key integer not null)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS RebOfPlayer
                (off_reb_per_game real, def_reb_per_game real, reb_per_game real, 
                 year, key integer not null)""")  # reb/game(off ^ def) --- sort by key ^ year

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Player
                    (first_name text, last_name text, position text, key integer primary key not null)""")


        # responsible for serializing data of (array / numpy array) --> storing as bytes for sql compatibility
        sqlite3.register_adapter(np.ndarray, mutate_obj)

        # responsible for restoring/transforming numpy array object
        sqlite3.register_converter("array", restore_obj)


    """                                          nameScrape                                                          """
    ####################################################################################################################
    def add_to_tables(self, playerYear, player_stats, player_reb, playerObj, keyf):
        """ add_to_tables: function taking 3 list arguments to insert into all three tables
                           as a function decorator"""

        name = playerObj[0]

        if not self.check_records(playerObj[0]):
            """ check records if exists in database and return tuple of value or None"""

            key = keyf.addUniq(name)
            self.add_Player(*playerObj, key)
            self.commit()

        else:
            key = keyf.getKey(name)  # get original key to use if object in records

        self.add_playersYear(*playerYear, key)
        self.commit()

        self.add_stats(*player_stats, key)
        self.commit()

        self.add_reb(*player_reb, key)
        self.commit()

    def add_playersYear(self, team, rank, year, key):
        """ insert function to SQL commands, inputting a players year(TABLE) by rank and team """
        if key == -1:
            return
        self.cur.execute("INSERT INTO YearOfPlayer (team, rank, year, key) VALUES(?,?,?,?)", (team, rank, year, key))


    def add_stats(self, game_played, min_per_game, reb_per_game, wins, year, key):
        """ Insert into inputting a players stat table by year: games played, mins/game, reb/game and wins by
            plus/minus scores """

        self.cur.execute("""INSERT INTO StatsOfPlayer (game_played, min_per_game, reb_per_game, wins, year, key)
                VALUES(?,?,?,?,?,?)""", (game_played, min_per_game, reb_per_game, wins, year, key))

    def add_reb(self, off_reb_per_game, def_reb_per_game, reb_per_game, year, key):
        """ add_reb- off_reb_per_game, def_reb_per_game, reb_per_game, year, key """

        self.cur.execute("""INSERT INTO RebOfPlayer (off_reb_per_game, def_reb_per_game, reb_per_game, year, key)
                    VALUES(?,?,?,?,?)""", (off_reb_per_game, def_reb_per_game, reb_per_game, year, key))

    def add_Player(self, name, pos, key):
        """ add_Player: inputting a new players(objects for data) with attributes by name and years played """

        if key == -1:
            return

        (first_name, last_name) = name.split(' ', 1)  # split name for optional search values

        self.cur.execute("""INSERT INTO Player (first_name, last_name, position, key)
                        VALUES(?,?,?,?)""", (first_name, last_name, pos, key))
        self.commit()


    """                                       nbaPlus                                                              """
    ##################################################################################################################
    def search_player(self):
        """ Player (first_name text, last_name text, position text, key integer primary key not null) """

        l_name = input("Enter Last Name of player: ").replace(" ", '')

        self.cur.execute("""Select * FROM Player
                         WHERE last_name = ?""", (string.capwords(l_name),))
        player_info = self.cur.fetchall()

        if player_info:
            print("\n\nPlayers Found:\n")
            for row in player_info:
                print(f'\t{" ".join(row[:2])}, {row[-2]}')

        else:
            print("Sorry, couldn't find a match")


    def search_YearOfPlayer(self):
        """ YearOfPlayer (team text, rank integer, year array, key integer not null)  """

        name = self.getName.split()

        if not self.check_records(' '.join(name)):
            print("player does not exist")

        else:

            player_info = self.selectByName(name)

            self.cur.execute("""Select * FROM YearOfPlayer
                             WHERE key = ?""", (player_info[-1],))
            player_year = self.cur.fetchall()

            print(f"\n\t{' '.join(name)}'s overall years:\n\nYear:\t {'Team:':<24}Rank:")

            for played in player_year:
                year = int(re.sub("[^0-9]", "", str(restore_obj(played[-2]))))
                print(f'{year}\t', ' '.join([f"{str(i):<23}" for i in list(played[:-2])]))

    def restoreYears(self, player_info):

        self.cur.execute("""Select * FROM YearOfPlayer 
                         WHERE key = ?""", (player_info[-1],))

        return [int(re.sub("[^0-9]", "", str(restore_obj(year[-2])))) for year in self.cur.fetchall()]

    def selectByName(self, name):

        self.cur.execute(
            """Select * FROM Player WHERE last_name = ? COLLATE NOCASE AND first_name = ? COLLATE NOCASE""",
            (name[-1], name[0],))
        return self.cur.fetchone()


    def search_StatsOfPlayer(self):
        """ StatsOfPlayer (game_played integer, min_per_game real, reb_per_game real, wins real, year, key integer not null)  """

        name = self.getName.split()

        if not self.check_records(' '.join(name)):
            print("player does not exist")

        else:
            player_info = self.selectByName(name)

            self.cur.execute("""Select * FROM StatsOfPlayer
                             WHERE key = ?""", (player_info[-1],))
            player_stats = self.cur.fetchall()

            sp, da = ' ', '-'
            print(f"\n\t{' '.join(name)}'s overall plus-minus stats per year:\n" +
                  f'Year{sp * 8}GP  MPG   RPG   WINS\n{da * 4 + sp * 8 + da * 2 + sp * 2 + da * 4 + sp + da * 5 + sp + da * 5}')

            for stats in player_stats:
                print(f'{stats[-2]}\t', ' '.join([f"{str(i):>5}" for i in list(stats[:-2])]))

    def search_RebOfPlayer(self):
        """ RebOfPlayer (off_reb_per_game real, def_reb_per_game real, reb_per_game real, year, key integer not null)  """

        _cur = self.cur  # _conn.cursor()
        name = self.getName.split()

        if not self.check_records(' '.join(name)):
            print("player does not exist")

        else:
            dash = "-" * 5

            player_info = self.selectByName(name)

            self.cur.execute("""Select * FROM RebOfPlayer
                             WHERE key = ?""", (player_info[-1],))
            player_reb = self.cur.fetchall()

            print(f"\n\t{' '.join(name)}'s overall plus-minus rebs per year:\n" +
                  f'Year \t', f'OFF{" " * 3}DEF\n{dash}\t {dash + " " + dash}')
            for reb in player_reb:
                print(f'{reb[-2]}:\t', ' '.join([f"{str(i):>5}" for i in list(reb[:-3])]))

    @property
    def getName(self):
        """ getName: """
        f_name = input("Enter First Name of player: ").replace(" ", '')
        l_name = input("Enter Last Name of player: ").replace(" ", '')
        return string.capwords(f_name + ' ' + l_name)

