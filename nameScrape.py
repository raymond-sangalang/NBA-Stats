# CIS41A-lab5 name.py
# Raymond Sangalang
# back end to application: reads and stores data from the file and allows searches for dat

import re
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

pattern = re.compile("(^[>](.+)</a|/a>(.+)<|([a-zA-Z\s]+))")
class Name:

    
    def __init__(self, _fileName=''):
        ''' Constructor- requests(interface)  '''
        self.players = {}
        #if _fileName is None:
            #return
    
        content= requests.get(_fileName)                    # creates HTML page object from request
        content.raise_for_status()
        
        soup= BeautifulSoup(content.text,'html.parser')     # flexible HTML parser-BeautifulSoup-gets python byte string from request obj
        table= soup.find('table', {'class': 'tablehead'})

        for tr in table.find_all('tr', {'class': self.match_tag}):
            listOfStats= re.findall('\d+(?:\.\d+)?', str([td.text for td in tr.find_all('td')]))
            listOfNames= re.findall("[^\s,'][a-zA-Z\s]+", str([td.text for td in tr.find_all('td')]))
            self.players[listOfNames[0]]= tuple(listOfNames[1:]+listOfStats)

            print(f"{', '.join([str(i) for i in listOfNames]):30s} ==> {', '.join([str(i) for i in listOfStats])}\n")
        if len(self.players) == 0: return None
            
            
    def match_tag(self, _tag):
        return True if _tag and (_tag.startswith('oddrow') or _tag.startswith('evenrow')) else False
        



        





    
    

        
        
        
        
