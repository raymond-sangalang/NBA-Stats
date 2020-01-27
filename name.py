# Raymond Sangalang
# CIS41A-lab5 name.py
#             back end to application: reads and stores data from the file and allows searches for dat
import re

pattern = re.compile("(<td\s>(\w+))+")   # re pattern
class Name:
    ''' class Name- back-end process data, and search database for initials and popularity '''
    
    def __init__(self, _fileName):
        ''' Constructor: requests(interface) for file, findall boy and girls within <td >(boynames|girlnames)</td> and process 2 lists  '''
        
        self._boyNames, self._girlNames= [], []    # 2 list for girls and guys

        with open(_fileName) as fileIn:
            for k,i in enumerate(re.findall(pattern, fileIn.read())):     # k utilized for count of both list of girls and boys
                
                if k % 2 == 0: self._boyNames.append(i[1])              # boys first
                else:
                    self._girlNames.append(i[1])                        # girls second
                    
            self._numRankings=int((len(self._girlNames)+len(self._boyNames))/2)             # count of data values
            print(f'Found {self._numRankings} names of each gender in file {_fileName}')    # print number of rankings in file
                                           
    def getBoys(self): return self._boyNames         # getters for boys and girls list
    def getGirls(self): return self._girlNames
    def getCount(self): return self._numRankings     # getter for count in both list

    # make into one for loop
    def searchByInitial(self, *initials, gender):
        ''' searchByInitial: accepts gender and (packaged)initial string, looks for each character in initial string
                             for all names starting with that character.                               '''
        
        gen= self.getBoys() if gender[0] == 'm' else self.getGirls()
        for ch in initials:
            yield (_init for _init in gen if re.match(ch, _init, re.I))   

  
    def searchByPopularity(self, limit= 0): 
        ''' searchByPopularity: return generator for popularity of names by argument limit
                                zip for large packaging of data '''
        return  ((x,y) for x,y in zip(self.getBoys()[:limit],self.getGirls()[:limit])) 

        