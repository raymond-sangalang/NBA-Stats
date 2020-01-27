# Raymond Sangalang
# CIS 41A - lab5.py
#         - The program implements UI(user-interface) to communicate with user and retrives data from the Names(back-end database) to
#           compile data from a file and allow searching of data by initials and limit of popularity; utillize generator via less memory
#           from unknown amount of data.
from name import Name, re                   

class UI:
        ''' UI(user-interface)- implements front-end app: constructor for file, and run method to utilize methods
                                from Name and catches exceptions to acquire data validation.                     '''
        __DEFAULTFILE= "lab5_1990s.txt"
        
        def __init__(self):
                ''' constructor: keep looping until file is able to be read in, then create Name object'''
                while True:   
                        ''' loops until valid file name is read, and if user just entered, then utilizes default file name'''
                        try:
                                searchWeb= str(input(f"\n\tSearching Data\n\t{'-'*14}\nEnter a file <Enter key for default>: "))
                                
                                if searchWeb == "" : self._dataNames= Name(self.__DEFAULTFILE)
                                elif searchWeb: self._dataNames= Name(searchWeb)
                                
                                break    
                        except FileNotFoundError: print("ERROR: opening input file")
                        
        def getData(self): return self._dataNames  # getter to Name class
                
        def searchPop(self):
                ''' searchPop: checks for correct input; within range of list'''
                
                while True:
                        try:
                                _numPopularity= input("Enter top number of names or press Enter for all names:")
                                if not _numPopularity :                                 # if enter, then user selects all names
                                        _numPopularity= self.getData().getCount() 
                                        
                                elif self.getData().getCount() < int(_numPopularity) : 
                                        _numPopularity= self.getData().getCount()
                                        
                                elif not 0 < int(_numPopularity) :            # check range not within list (ex to this case: 1 to 200)
                                        raise ValueError(f"Data is in range <0 - {self.getData().getCount()}>")   # raise ValueError to tell user
                                
                                break
                        except ValueError as e: print("ERROR: ", str(e))                                  # print correct error
                gen= self.getData().searchByPopularity(int(_numPopularity))                    # input local generator
                
                sp, again, count= ' '*4 , "" , 1                       # sp for spaces, again to allow user to keep entering for data, count increments ranking
                print(f"\n\nRank{sp}Boys{sp*3}Girls\n----{sp+'-'*12}{sp+'-'*12}")
                
                while again == "":
                        try:
                                for v in range(5):
                                        (n1,n2) = next(gen)                          # iterate generator of tuples
                                        print(f"{v+count:3d} {sp}{n1:12s}{sp+n2:10s}")   # print 5 with rank
                                again= input("Enter for next 5 names: ")                # ask user for more values
                                count+=5
                                        
                        except StopIteration:                 # if values end in list
                                print("End of list of names")
                                break
                        
        def searchInit(self):        
                ''' searchInit: obtains gender and initial, then utilizes searchInitial in Name class '''
                
                _initialPattern= re.compile("(\w\w)|([,]{2})|([^a-zA-Z,])", re.IGNORECASE)          # checks format for comma-separated initials
                while True:
                        ''' Loops and validates exceptions on gender'''
                        try:
                                _gender=re.sub("\s", "", str(input("Enter gender: "))).lower()      # split spaces to check fullmatch      

                                if not re.fullmatch("(m|f|male|female)",_gender,re.I):      # must be in either m, f, male, or female
                                        raise ValueError("gender must be male(m) or female(f)!")    #raise exception if incorrect match
                                else: print(_gender)
                                break
                        except ValueError as e:
                                print("ERROR:", str(e))
                
                ''' keep prompting user for a comma-separated list of initials, until you get a valid list. A valid list:
                1 or more initials, and if more than one initials, must separated by a comma; initials must be a single lower or uppercase letter '''                        
                while True:        
                        try:
                                _initials= re.sub("\s", "", str(input("Enter a comma separated list of initials: "))).lower()
                                
                                if _initialPattern.search(_initials) or re.match(',',_initials):    # raise if starts with ',' or incorrect pattern found in compile 
                                        raise ValueError("must start with letter and comma separated if more than 1 letter")
                                
                                else: 
                                        _initials = sorted(re.sub(',','',_initials))               # sorting the validated list of initials for search
                                break   
                        except ValueError as e: print("Invalid:", str(e))
                        
                _listInitials= self.getData().searchByInitial(*_initials, gender=_gender)          # pack list of initials and return generator
                
                for count,i in enumerate(_listInitials):                           # print searched list of initials in generator
                        print(f'{_initials[count].upper()}:', ', '.join(sorted(list(i))))

        
        def run(self):       
                ''' run: loop to print menu and ask the user for one of 3 choices, until there is a valid choice. '''
                choice= {'i': self.searchInit, 'p': self.searchPop}
                _getChoice= None
                while _getChoice not in ('q', 'Q'):
                        try:
                                _getChoice = input(f"\n\tSearch Database\n\t{'-'*15}\ni. Search by initials\np. Search by popularity\nq. Quit\n\tYour choice: ")
                                _getChoice = choice[re.sub("\s", "", _getChoice).lower()]()
                                
                        except KeyError: 
                                print("Quiting Search")
                        
if __name__ == "__main__":
        
        app= UI()
        app.run()
