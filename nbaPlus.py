""" Raymond Sangalang
         - The program implements UI(user-interface) to communicate with user and retrieves data from
           the Names(back-end database) to compile data from a file and allow searching of data      """
from datetime import datetime as dt
from nameScrape import Name, savePage, loadPage
from playerDB import nbaDatabase
from trademanager import TradeManager
from nbaexception import checkInput, OptionNotInRangeError, NotAnIntegerError, ZeroOrLessError


class UI:
    """ UI(user-interface)- implements front-end app: constructor for file, and run method to utilize methods
                            from player Name and catches exceptions to acquire data validation.               """

    # WebScrape/Crawl into espn files
    __STARTFILE = "http://www.espn.com/nba/statistics/rpm/_/year/"
    _STARTYEAR = 2014

    OPTION_DICT = {1: "player's by last name", 2: "player overall years", 3: "player stats",
                   4: "player's rebounds", 5: "End Search"}

    def __init__(self):
        """ constructor: keep looping until file is able to be read in, then create Name object """

        self.playerBase = self.getDB()
        recentYear = dt.now().year + 1  # next year int to stop iteration

        """ Condition to check if serialized data exists and most current year within the data is up to date """
        if self.playerBase.connect_SQL() and ((recentYear - 1) == self.playerBase.getCurrentYearData()):
            return


        self.playerBase.createTables()
        teams = Name.getTeam()

        year_to_data, page_count = loadPage()
        loadStatus = True if year_to_data and page_count else False

        for num_year in range(year_to_data, recentYear):
            ''' Collecting data in years starting from 2014 to current year '''

            print(f"\n\n\t\tYEAR: {num_year - 1}-{num_year}\n\t\t{'-' * 15}\nProcessing Data...\n")

            # file pages differ, such that current year omits a string partition
            filetouse = self.__STARTFILE + str(num_year) if num_year <= recentYear else self.__STARTFILE[:-8]

            searchWeb = filetouse

            if loadStatus:
                loadStatus = False
            else:
                page_count = 1

            while True:
                ''' loops until valid file name is read, and if user just entered, then utilizes default file name '''

                _data = Name(searchWeb, self.playerBase, teamDict=teams)  # insert player names into data base
                page_count += 1  # increment to next page of data

                if len(_data) == 0:  # if Name has no data, break out of loop  --> save web page and year
                    break

                if page_count >= 2 and num_year == recentYear:
                    searchWeb = filetouse + f"/_/page/{page_count}"

                elif page_count >= 2:
                    searchWeb = filetouse + f"/page/{page_count}"
            savePage(num_year, page_count)


    def getData(self):
        return self.playerBase.getData()

    def getDB(self):
        self.playerBase = nbaDatabase()
        self.playerBase.connect_SQL()
        return self.playerBase

    def getMenu(self):
        return self.OPTION_DICT

    def getOption(self):

        print(f"\nSearch Engine\n{'-' * 27} ")
        [print(f"\t{index}. {values}") for index, values in self.getMenu().items()]
        option = input("\nEnter Choice: ")

        if not option.isdigit():
            raise NotAnIntegerError(option)

        return int(option)

    def goSearch(self):
        """ goSearch- function to obtain user input of type of search """

        self.playerBase.connect_SQL()

        db_dict = {1: self.playerBase.search_player, 2: self.playerBase.search_YearOfPlayer,
                   3: self.playerBase.search_StatsOfPlayer, 4: self.playerBase.search_RebOfPlayer}

        while True:
            """ User Selection of search engine """
            try:
                _option = self.getOption()

                if not 1 <= _option <= 5:
                    raise OptionNotInRangeError(_option)
                elif _option == 5:
                    break
                print(f"You chose {self.OPTION_DICT[_option]} database!")

                db_dict[_option]()

            except (OptionNotInRangeError, NotAnIntegerError) as e:
                print(e)

            except ValueError:
                print("\tINDEX ERROR: please select another option")
        print("\n\t\t ENDING SEARCH....")


    def createTeams(self):
        """ Creating Team """
        print(f"\n\tCreating Teams\n\t{'-' * 14}")
        while True:
            try:
                numPlayers = checkInput("players on each team")
                numTeams = checkInput("teams to create")

                break
            except (ZeroOrLessError, NotAnIntegerError) as err:
                print(err)
            except (ValueError, TypeError, KeyboardInterrupt) as err:
                print("ERROR:", err, "\nplease input integer values")

        teams, index = [], 0


        while index < numTeams:
            newTeam = TradeManager(numPlayers)
            newTeam.createUnit()
            teams.append(newTeam)
            index += 1

        for i in teams:
            i.printRoster()
            i.printAllStats()
            print("Least years for team:", i.getLeastYears())


if __name__ == "__main__":
    app = UI()
    app.goSearch()
    app.createTeams()
