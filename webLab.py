# Raymond Sangalang
#         - The program implements UI(user-interface) to communicate with user and retrives data from the Names(back-end database) to
#           compile data from a file and allow searching of data
from nameScrape import Name, re, requests
import os


class UI:
    ''' UI(user-interface)- implements front-end app: constructor for file, and run method to utilize methods
                            from Name and catches exceptions to acquire data validation.                     '''

    curr_year= "http://www.espn.com/nba/statistics/rpm"
    __STARTFILE= "http://www.espn.com/nba/statistics/rpm/_/year/"

    def __init__(self):
        ''' constructor: keep looping until file is able to be read in, then create Name object'''
        for num_year in range(2014, 2021):
            print(f"\n\n\t\tYEAR: {num_year-1}-{num_year}\n\t\t{'-'*15}\n")
            filetouse= self.__STARTFILE+str(num_year) if num_year != 2021 else self.curr_year
            searchWeb= filetouse
            
            page_count=1
            status = True
            while status: 
                print(searchWeb)
                ''' loops until valid file name is read, and if user just entered, then utilizes default file name'''
                #try:   #searchWeb= str(input(f"\n\tSearching Data\n\t{'-'*14}\nEnter a file <Enter key for default>: "))

                        
                    
                #searchWeb= __filetouse
                _data= Name(searchWeb)
                page_count+=1 
                if page_count >= 2 and num_year == 2021:
                    searchWeb= filetouse + f"/_/page/{page_count}"
                elif page_count >= 2: 
                    searchWeb= filetouse + f"/page/{page_count}"
                
    
                #if searchWeb == "" : self._dataNames= Name(self.__DEFAULTFILE)
                #elif searchWeb: self._dataNames= Name(searchWeb)
                if _data == None: status = False
                else:
                    self._dataNames = _data
                
                                                                  # increment to next page of data
    
                #break    
                '''
                except FileNotFoundError: print("ERROR: opening input file")
                except requests.exceptions.HTTPError as ht: print("HTTP ERROR:", ht)
                except requests.exceptions.ConnectionError as ct: print("Connection ERROR:", ct)
                '''
                #break

    def getData(self): return self._dataNames  # getter to Name class




if __name__ == "__main__":

    app= UI()
    app.run()
