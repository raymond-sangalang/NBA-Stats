# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for data
import re, requests
import subprocess
from bs4 import BeautifulSoup
from keychain import KeyChain, save_object, load_object

_TEAMFILE = "team_file.csv"
_SERIALIZABLEFILE = "nbaObj.pkl"
_webLocation = "currentWebPage.txt"
keyf = KeyChain()


class Name:

    def __init__(self, _fileName='', _pDB=None, teamDict={}):
        ''' Constructor- requests(interface)  '''

        curr_year = re.search("(20[\d]+)", _fileName)[0]  # current year
        self.players = {}
        self.teams = teamDict

        _pDB.connect_SQL()  # connect a database through sqlite3 into file _nbaPlayer.db

        content = requests.get(_fileName)  # creates HTML page object from request
        content.raise_for_status()

        soup = BeautifulSoup(content.text,
                             'html.parser')  # flexible HTML parser-BeautifulSoup-gets python byte string from request obj
        table = soup.find('table', {'class': 'tablehead'})

        key = load_object(_SERIALIZABLEFILE)
        self.keyHolder = keyf if key is None else key

        for tr in table.find_all('tr', {'class': self.match_tag}):
            """ get and list all subclasses, td, and string for searching - listOfStats --> rank, game played, 
                 min/game, off-reb/game, def-reb/game, reb/game, wins                                          """

            _string = str([td.text for td in tr.find_all('td')])
            listOfStats = re.findall('-?\d+(?:\.\d+)?', _string)

            newsoup = str(tr.find('a'))             # subclass 'a' (contains name, position, team and link to player)
            name = re.search("(?<=>)(.+)<", newsoup)

            if not name:
                break
            name = name.group(1)

            fname, lname = tuple(name.split(' ', 1))  # split into first and last name of player

            pos = re.search(', (\w{1,2})', _string).group(1)  # position
            team = self.teams[str(
                re.findall('[A-Z]{2,3}', _string)[-1])]  # get last team name played in year by search of team abbr key

            self.players[fname + ' ' + lname] = [pos, *listOfStats]


            ''' Set Values for tables'''
            # YearOfPlayer entities: name+year--team--ranking
            playerYear = [team, int(listOfStats[0]), curr_year]

            # StatsOfPlayer: games played, min/game, off rpg, def rpg, total reb/game, wins= game_played, min_per_game, reb_per_game, wins, year
            player_stats = [int(listOfStats[1]), float(listOfStats[2]), *[float(i) for i in listOfStats[5:]], curr_year]

            # RebOfPlayer: off_rpg, def_rpg, rpg
            player_reb = listOfStats[3:6] + [curr_year]

            # Player attributes/entities: name(first and last), basketball position, and unique Key
            playerObj = [fname + ' ' + lname, pos]

            '''  Inserting values into the tables- 1) playersYear  2) StatsOfPlayer  3) Player  '''
            _pDB.add_to_tables(playerYear, player_stats, player_reb, playerObj, self.keyHolder)
            
        save_object(self.keyHolder, _SERIALIZABLEFILE)
        _pDB.__disconnect__()  # close connection


    def match_tag(self, _tag):
        """ match_tag:  boolean return utilized for search in web parsing """
        return True if (_tag and (_tag.startswith('oddrow') or _tag.startswith('evenrow'))) else False


    def getKey(self, name):
        return keyf.getKey(name)


    def __len__(self):
        return len(self.players)

    @staticmethod
    def getTeam():

        _Done = False
        _teamIn = {}
        pattern = re.compile('(?P<Team>[A-Za-z0-9\s]+), (?P<abbrev>[A-Z]+)')

        try:
            with open(_TEAMFILE, "r") as infile:

                for line in infile:
                    match = re.search(pattern, line.rstrip())

                    if match is not None:
                        _teamIn[match.group("abbrev")] = match.group("Team")


        except FileNotFoundError:
            raise FileNotFoundError(
                f"Cant find {_TEAMFILE}")  # exceptions handle file search, IO streaming, incorrect
        except ValueError:
            print("File content invalid.")  # value/type and problem occurrences while running program

        return _teamIn


def savePage(arg1, arg2):
    """ save web page location (year(arg1), page(arg2)) """
    arg1, arg2 = str(arg1), str(arg2)
    if not arg1.isdigit() or not arg2.isdigit():
        print("Invalid arguments")
        return 1

    subprocess.call(['sh', './savePage.sh', _webLocation, arg1, arg2])


def loadPage():

    task = subprocess.Popen(["cut", "-f2", _webLocation], stdout=subprocess.PIPE)
    recent_web = tuple(int(line) for line in task.stdout)

    task.wait()
    return recent_web
