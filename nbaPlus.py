from playerDB import nbaDatabase
from nameScrape import Name


class UI:

    def __init__(self):

        print("Starting NBA Plus...")

        self.playerBase = nbaDatabase()
        self.startup_scrape()
        self.show_top_players()

    def startup_scrape(self):

        searchWeb = True  # False when not needing to search
        teams = {}

        try:
            Name(searchWeb, self.playerBase, teamDict=teams)
            print("--> Data loaded successfully.")
        except Exception as e:
            print(f"ERROR: Scraping failed. Continuing without web data.\n{e}")
        


    def show_top_players(self):
      

        print("\nTop Players:")
        for player in self.playerBase.get_all_players()[:10]:
            name = f"{player[0]} {player[1]}"
            position = player[2]
            team = player[3]
            bpm = player[4]
            season = player[5]

            print(f"{name:30} {position:3} {team:3} BPM={bpm:5.2f} ({season})")


if __name__ == "__main__":
    app = UI()
