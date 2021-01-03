from team import Team
from playerDB import nbaDatabase


class TradeManager:

    def __init__(self, rosterCount):

        self.unit = Team(name=str(input("\nEnter a team name: ")))
        self.db = nbaDatabase()
        self.rosterCount = rosterCount

    def getRoster(self):
        return self.unit.getRoster()

    def __iter__(self):
        return iter(self.unit)

    def __str__(self):
        return str(self.unit)

    def __repr__(self):
        return str(self.unit)

    def __eq__(self, other):
        if not isinstance(other, Team):
            return NotImplemented
        return tuple(self.getRoster()) == tuple(other.getRoster())

    def __hash__(self):
        return hash(tuple(self.getRoster()))


    def createUnit(self):
        print(f"\tCreate Team {self.unit.name}")
        self.db.connect_SQL()
        self.createTeams()
        self.db.__disconnect__()


    def createTeams(self):
        """ Creating Team """

        count = 0

        while count < self.rosterCount:
            print(f"\n-> Lookup player {count + 1}")
            playerData = self.db.getPlayerInfo()

            if self.unit.addPlayer(playerData):
                count += 1

    def getLeastYears(self):
        return self.unit.getNumberOfYears()


    def printAllStats(self):
        self.unit.print()

    def printRoster(self):
        self.unit.printRoster()





