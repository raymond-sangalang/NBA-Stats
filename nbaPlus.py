''' Raymond Sangalang
         - The program implements UI(user-interface) to communicate with user and retrives data from 
           the Names(back-end database) to compile data from a file and allow searching of data      '''                                                                   
from nameScrape import Name, re, requests, keyf
import string, playerDB

import nameScrape

class UI:
    ''' UI(user-interface)- implements front-end app: constructor for file, and run method to utilize methods
                            from player Name and catches exceptions to acquire data validation.               '''


    # WebScrape/Crawl into espn files
    __STARTFILE= "http://www.espn.com/nba/statistics/rpm/_/year/" 
    


    def __init__(self):
        ''' constructor: keep looping until file is able to be read in, then create Name object '''
        
        self.playerBase= playerDB
        _conn= self.playerBase.connect_SQL()                                          # connect database through sqlite3 into .db file 
        self.playerBase.createTables(_conn)                                           # create table if do not exist
        teams= Name.getTeam()
        
        for num_year in range(2014, 2021):
            ''' Collecting data in years starting from 2014 to 2020 '''
            
            print(f"\n\n\t\tYEAR: {num_year-1}-{num_year}\n\t\t{'-'*15}\nProcessing Data...\n")
            
            
            # file pages differ, such that current year omits a string partition
            filetouse= self.__STARTFILE+str(num_year)  if num_year <= 2021  else self.__STARTFILE[:-8]
            
            searchWeb= filetouse
            page_count= 1                                                             # start of page count
            
            while True: 
                ''' loops until valid file name is read, and if user just entered, then utilizes default file name '''
                
                _data= Name( searchWeb, self.playerBase, teamDict= teams)             # insert player names into data base
                page_count += 1                                                       # increment to next page of data
                
                if len( _data ) == 0:                                                 # if Name has no data, break out of loop
                    break        
                
                print( '\t' , searchWeb )
                self._dataNames = _data                
                
                if page_count >= 2 and num_year == 2021:
                    searchWeb= filetouse + f"/_/page/{ page_count }"
                    
                elif page_count >= 2: 
                    searchWeb= filetouse + f"/page/{ page_count }"
                         
            
        



    def getData(self): return self.playerBase  # getter to the database
    
    
    def goSearch(self):
        """ goSearch- function to obtain user input of type of search """
        
        _cur= self.playerBase.connect_SQL()  
        
        search_dict= {1: "players", 2 : "years", 3 : "stats", 4 : "rebounds"}
        
        db_dict= { 1 : self.playerBase.search_player, 2 : self.playerBase.search_YearOfPlayer, 
                   3 : self.playerBase.search_StatsOfPlayer, 4 : self.playerBase.search_RebOfPlayer }
    
        try:
            
            while True:
                """ User Selection of search engine """
                
                print(f"\nSearch Engine\n{'-'*19} ")
                [print(f"\t{index}. {values}") for index, values in search_dict.items()]  
                
                _option= int(input( "\nEnter Choice: " ))
                print(f"You chose {search_dict[_option]} database!")
          
                db_dict[_option](_cur)
          
               
        except ValueError:
            print("index error")
            
        except KeyError:
            print("\n\t\t ending search....")
            
        return
    

    
    

if __name__ == "__main__":
    app= UI()
    app.goSearch()

    print("\n\nreturn 0")






