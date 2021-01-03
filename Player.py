""" Player.py - class obtains data of a player """


class Player:

    def __init__(self, name, years=None, minPerGame=None, total_rpg=None, wins=None):

        self.name = name
        self.years = years
        self.playerStats = dict()

        if not self.years:
            return

        for i, year in enumerate(self.years):
            self.playerStats[year] = [minPerGame[i], total_rpg[i], wins[i]]


    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name, self.years != other.name, other.years

    def __hash__(self):

        return hash((self.name, self.years))


    def getName(self):
        return self.name

    def getYears(self):
        return self.years

    def setYears(self, years):
        self.years = years

    def setStats(self, years, playerStats):
        self.years = years
        self.playerStats = playerStats

    def getYear_minPerGame(self, year):
        return self.playerStats[year][0]

    def getYear_totalRPG(self, year):
        return self.playerStats[year][1]

    def getYear_wins(self, year):
        return self.playerStats[year][2]

    def yearsInDB(self):
        return len(self.years)

    def getAverage(self, f, numYears):

        yearsToAvg = self.years[self.yearsInDB() - numYears:]
        return sum([f(_) for _ in yearsToAvg]) / numYears

    def avgChoice(self, numYears, choice=0):

        avgDict = {1: self.getYear_minPerGame, 2: self.getYear_totalRPG, 3: self.getYear_wins}
        fx = None

        try:
            while True:
                """ User Selection of search engine """
                if choice not in avgDict.keys():
                    print(f"\nSearch Average\n{'-' * 19} "
                          + "\n1) Minutes per game\n2) Total rebounds per game\n3) Wins per game")
                    choice = int(input("\nEnter Choice: "))

                fx = avgDict[choice]
                break

        except ValueError:
            print("Index error...")
        except KeyError:
            print("Invalid Option...")

        return self.getAverage(fx, numYears)

    def printStats(self):
        print(f"\n\t\t{self.name}\n\t\t{'-' * len(self.name)}")
        for year, stat in self.playerStats.items():
            print(f"{year}:\n\tMin Per Game: {stat[0]}\n\t" +
                  f"Total RPG: {stat[1]}\n\tWins-Loss ratio: {stat[2]}\n")

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(f'{self.name} played in ' + ' '.join(self.years))
