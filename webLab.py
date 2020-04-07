# Raymond Sangalang
#         - The program implements UI(user-interface) to communicate with user and retrives data from the Names(back-end database) to
#           compile data from a file and allow searching of data
from nameScrape import Name, re, requests, _pDB


_conn= _pDB.connect_SQL()                           # connect a database through sqlite3 into file _nbaPlayer.db 
_pDB.createTables(_conn)                            # create table if do not exist

class UI:
    ''' UI(user-interface)- implements front-end app: constructor for file, and run method to utilize methods
                            from player Name and catches exceptions to acquire data validation.               '''


    # WebScrape/Crawl into espn files
    __STARTFILE= "http://www.espn.com/nba/statistics/rpm/_/year/" 
    


    def __init__(self):
        ''' constructor: keep looping until file is able to be read in, then create Name object '''
        
        for num_year in range(2014, 2021):
            ''' Collecting data in years starting from 2014 to 2020 '''
            
            print(f"\n\n\t\tYEAR: {num_year-1}-{num_year}\n\t\t{'-'*15}\nData obtained:\n")
            
            # file pages differ, such that current year omits a partition of string
            filetouse= self.__STARTFILE+str(num_year)  if num_year <= 2021  else self.__STARTFILE[:-8]
            
            searchWeb= filetouse
            page_count= 1                                        # start of page count
            
            while True: 
                ''' loops until valid file name is read, and if user just entered, then utilizes default file name'''
                
                print(searchWeb)
                
                _data= Name(searchWeb)
                page_count += 1                                   # increment to next page of data
                
                if len(_data) == 0: 
                    break                                         # if page has no data, break out of loop
                
                self._dataNames = _data                
                
                if page_count >= 2 and num_year == 2021:
                    searchWeb= filetouse + f"/_/page/{page_count}"
                    
                elif page_count >= 2: 
                    searchWeb= filetouse + f"/page/{page_count}"
                                                            


    def getData(self): return self._dataNames  # getter to Name class
    

    
    

if __name__ == "__main__":
    app= UI()





