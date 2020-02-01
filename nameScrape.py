# CIS41A-lab5 name.py
# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for data
import re, requests, sqlite3
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


''' creating a database through sqlite3 into file _nbaPlayer.db '''
'''
_link= sqlite3.connect('_nbaPlayer.db')
_cur= _link.cursor()

_cur.execute("""CREATE TABLE RECORDS()""")
_link.close()
'''
str_pattern= re.compile("[^\s\d,'/][a-zA-Z\.\-\s]+")

class Name:

    def __init__(self, _fileName=''):
        ''' Constructor- requests(interface)  '''
        
        
        self.players = {}
        self.listOfNames, self.listOfStats = [], []      # listOfNames --> player name, team, and position
                                                         # listOfStats --> rank, game played, min/game, off-reb/game, def-reb/game, reb/game, wins

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
        



        





    
    

        
        
        
        
