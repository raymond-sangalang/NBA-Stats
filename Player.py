""" Player.py - class obtains data of a player """


class Player:

    def __init__(self, name="", years=None, minPerGame=None, total_rpg=None, wins=None):

        self.name = name
        self.years = years
        self.playerStats = dict()

        for i, year in enumerate(self.years):
            self.playerStats[year] = [minPerGame[i], total_rpg[i], wins[i]]

    def getName(self):
        return self.name

    def getYears(self):
        return self.years

    def getYear_minPerGame(self, year):
        return self.playerStats[year][0]

    def getYear_totalRPG(self, year):
        return self.playerStats[year][1]

    def getYear_wins(self, year):
        return self.playerStats[year][2]

    def yearsInDB(self):
        return len(self.years)

    def printStats(self):
        print("\n\t\t", self.name)
        for year, stat in self.playerStats.items():
            print(f"{year}:\n\tMin Per Game: {stat[0]}\n\t" +
                  f"Total RPG: {stat[1]}\n\tWins-Loss ratio: {stat[2]}\n")

    def __str__(self):
        return self.name
