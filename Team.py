""" Team will acquire a projection of players compared to another instantiated Team
     Note: number of players must meet to compare                                     """
from player import Player


class Team:

    def __init__(self, name, numberOfYears=0, spots=None):
        self.name = name
        self.numberOfYears = numberOfYears               # lowest years played for all players on roster
        if spots is None:
            self.spots = []  # list of all players on team
        else:
            self.spots = list(spots)

    def getNumberOfYears(self):
        return self.numberOfYears

    def setNumberOfYears(self, numberOfYears):
        self.numberOfYears = numberOfYears

    def getFront(self):
        return self.spots[0]


    def getRoster(self):
        return self.spots

    def addPlayer(self, player=None):
        """ addPlayer - fills spots on team and takes the shortest amount of years """

        if not isinstance(player, Player) or any(i for i in self.spots if i == player):
            print("Invalid Entry: Must hold player object not in team")
            return False

        self.getRoster().append(player)
        self.minimalYears()
        return True


    def removePlayer(self, delName):

        if len(self) == 0:
            print("There is no spots to remove off roster")
        else:

            index = 0
            while index < len(self):

                if self.spots[index].toString() == delName:
                    self.getRoster().pop(index)
                    self.minimalYears()
                    return
                index += 1

            print(f"Could Not Find {delName} on team ")

    def minimalYears(self):

        if len(self) > 1:
            lowestYears = min([seat.yearsInDB() for seat in self.getRoster()])
        else:
            lowestYears = self.getFront().yearsInDB()

        self.setNumberOfYears(lowestYears)

    def getAverage(self, choice=0):

        if choice not in (1, 2, 3):
            print("ERROR: INVALID CHOICE!!!")

        else:
            print("\nAVERAGE WINS")
            for i in self.getRoster():
                print(f"\t{i.getName}: {i.avgChoice(self.getNumberOfYears(), choice):.2f}")


    def print(self):
        for sp in self.getRoster():
            sp.printStats()


    def printRoster(self):
        print(f"{self.name}'s Lineup\n")
        for index, name in enumerate(self.getRoster()):
            print("\t", index + 1, str(name))


    def __str__(self):
        ls = [f"\nTeam name: {self.name}", "Players:"]
        ls.extend("\t" + str(player) for player in self)
        return "\n".join(ls)


    def __len__(self):
        return len(self.spots)

    def __iter__(self):
        return iter(self.spots)

