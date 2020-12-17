""" Team will acquire a projection of players compared to another instantiated Team
     Note: number of players must meet to compare                                     """
from Player import Player


class Team:

    def __init__(self, numberOfSeats=0):

        self.numberOfSeats = numberOfSeats
        self.spots = []  # list of all players on team

    def getNumberOfSeats(self):
        return self.numberOfSeats

    def getRoster(self):
        return self.spots

    def addPlayer(self, player=None):
        """ addPlayer - fills spots on team and takes the shortest amount of years """
        self.getRoster().append(player)
        self.minimalYears()

    def removePlayer(self, delName):

        if len(self) == 0:
            print("There is no spots to remove off roster")
            return
        index = 0
        while index < len(self):
            if self.spots[index].toString() == delName:
                self.getRoster().pop(index)
                self.minimalYears()
                return
            index += 1

        print(f"Could Not Find {delName} on team ")

    def minimalYears(self):

        if len(self) <= 1:
            self.numberOfSeats = self.getRoster()[0].yearsInDB()
        else:
            self.numberOfSeats = min([seat.yearsInDB() for seat in self.getRoster()])



    def print(self):
        for spot in self.getRoster():
            spot.printStats()

    def printRoster(self):
        for i, name in enumerate(self.getRoster()):
            print(i+1, str(name))

    def __len__(self):
        return len(self.spots)


if __name__ == "__main__":

    """ check new classes to be robust into the system """

    playersName = "Stephen Curry"
    yearsPlayed = range(2014, 2021)
    minPerGamePlayed = [36.5, 32.7, 34.2, 33.4, 32.0, 33.8, 27.8]
    total_rpgPlayed = [6.53, 10.92, 11.37, 7.96, 6.2, 7.6, 4.72]
    winsPlayed = [18.76, 25.77, 27.01, 19.03, 9.4, 15.69, 0.73]

    player1 = Player(playersName, yearsPlayed, minPerGamePlayed, total_rpgPlayed, winsPlayed)

    playersName = "Klay Thompson"
    yearsPlayed = range(2014, 2020)
    minPerGamePlayed = [35.4, 31.9, 33.3, 34.0, 34.3, 34.0]
    total_rpgPlayed = [3.54, 4.13, 3.87, 3.98, 3.46, 2.39]
    winsPlayed = [12.75, 12.03, 11.92, 11.01, 9.01, 7.07]

    player2 = Player(playersName, yearsPlayed, minPerGamePlayed, total_rpgPlayed, winsPlayed)

    team1 = Team()
    team1.addPlayer(player1)
    team1.addPlayer(player2)

    team1.printRoster()
    print("The minimal number of years for all players:", team1.getNumberOfSeats())
