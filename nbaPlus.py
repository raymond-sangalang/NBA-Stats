''' Raymond Sangalang
         - The program implements UI(user-interface) to communicate with user and retrives data from 
           the Names(back-end database) to compile data from a file and allow searching of data      '''                                                                   
from nameScrape import Name, re, requests, keyf
import string, playerDB
from playerDB import nbaDatabase
from datetime import datetime as dt


try:
    import cPickle as pickle
    
except ModuleNotFoundError:
    import pickle

_SERIALIZABLEFILE = "nbaObj.pkl"


'''  ==> Note to self:  Create serial class in keychain <== '''
"""---------------------------------------------------------------------------------------------------------------------------------"""
"""
        ### to insert/update
pklData = pickle.dumps(nbaData, pickle.HIGHEST_PROTOCOL)  
curr.execute("insert into table (nbaData) values (:nbaData)", sqlite3.Binary(pklData))
        ### to retrieve data
curr.execute("Select nbaData from table limit 1")
for row in curr:
    data = pickle.loads(str(row['nbaData']))        """
"""---------------------------------------------------------------------------------------------------------------------------------""" 

def save_object(_obj, filename):
    ''' save_object: Overwrite any existing file in working directory with the filename, written
     in binary(wb) as a pickle file.                                            '''

    with open(filename, 'wb') as outFile:
        pickle.dump(_obj, outFile, pickle.HIGHEST_PROTOCOL)    

        
def load_object(filename):
    with open(filename, 'rb') as binFile:
        return pickle.load(binFile)
        
        
        
class UI:
    ''' UI(user-interface)- implements front-end app: constructor for file, and run method to utilize methods
                            from player Name and catches exceptions to acquire data validation.               '''

    # WebScrape/Crawl into espn files
    __STARTFILE= "http://www.espn.com/nba/statistics/rpm/_/year/" 
    

    def __init__(self):
        ''' constructor: keep looping until file is able to be read in, then create Name object '''
        
        self.playerBase = load_object(_SERIALIZABLEFILE)
        recentYear = dt.now().year + 1                                               # next year int to stop interation
        _conn= self.playerBase.connect_SQL()                                         # connect database through sqlite3 into .db file 
        
    
        """ Condition to check if serialized data exists and most current year within the data is up to date """
        if (self.playerBase is not None) and ( (recentYear-1) == self.playerBase.getCurrentYearData(_conn) ):
            return
        
        else:
            self.playerBase= nbaDatabase()        
                                                
        self.playerBase.createTables(_conn)                                           # create table if do not exist
        teams= Name.getTeam()
      
        for num_year in range(2014, recentYear):
            ''' Collecting data in years starting from 2014 to current year '''
            
            print(f"\n\n\t\tYEAR: {num_year-1}-{num_year}\n\t\t{'-'*15}\nProcessing Data...\n")
            
            # file pages differ, such that current year omits a string partition
            filetouse= self.__STARTFILE+str(num_year)  if num_year <= recentYear  else self.__STARTFILE[:-8]
            
            searchWeb= filetouse
            page_count= 1
            
            while True: 
                ''' loops until valid file name is read, and if user just entered, then utilizes default file name '''
                
                _data= Name( searchWeb, self.playerBase, teamDict= teams)             # insert player names into data base
                page_count += 1                                                       # increment to next page of data
                
                if len( _data ) == 0:                                                 # if Name has no data, break out of loop
                    break        
                
                print( '\t' , searchWeb )
                self._dataNames = _data                
                
                if page_count >= 2 and num_year == recentYear:
                    searchWeb= filetouse + f"/_/page/{ page_count }"
                    
                elif page_count >= 2: 
                    searchWeb= filetouse + f"/page/{ page_count }"
            
            save_object(self.getData(), _SERIALIZABLEFILE)
            


    def getData(self): return self.playerBase                              # getter to the database
    
    
    def goSearch(self):
        """ goSearch- function to obtain user input of type of search """
        
        _cur= self.playerBase.connect_SQL()  
        _option= 0
        
        search_dict= {1: "players", 2 : "years", 3 : "stats", 4 : "rebounds", 5 : "End Search"}
        
        db_dict= { 1 : self.playerBase.search_player, 2 : self.playerBase.search_YearOfPlayer, 
                   3 : self.playerBase.search_StatsOfPlayer, 4 : self.playerBase.search_RebOfPlayer }
    
        while _option != 5:
            try:
                
                while True:
                    """ User Selection of search engine """
                    
                    print(f"\nSearch Engine\n{'-'*19} ")  
                    [print(f"\t{index}. {values}") for index, values in search_dict.items()]  
                    
                    _option= int(input( "\nEnter Choice: " ))
                    
                    if _option == 5: break
                    else:
                        print(f"You chose {search_dict[_option]} database!")
            
                    db_dict[_option](_cur)
                
            except ValueError:
                print("Index error...")
                
            except KeyError:
                print("Invalid Option...")
            
        print("\n\t\t ending search....")
        return
    


if __name__ == "__main__":
    app= UI()
    app.goSearch()

    print("\n\nreturn 0")
