# nbaPlus.py
from playerDB import nbaDatabase
from nameScrape import Name
from gameScrape import GameScraper
from datetime import datetime


"""
start scrape first and separate from user interface - independence
- scrape
- UI
- multiple users (processes)

"""
class UI:

    def __init__(self):

        print("Starting NBA Plus...")
        self.playerBase = nbaDatabase()
        self.startup_scrape()

        isRunning = True
        while isRunning:
            self.show_operation_menu()
            try:
                op = int(input("Enter operation: "))
                match op:
                    case 1:
                        print("Showing top 10 players")
                        self.show_top_players()
                    case 2:
                        #
                        self.show_top_bpm_players()
                    case 3:
                        self.show_top_scoring_players
                    case 4:
                        print("Exiting program")
                        isRunning = False

                    case _: 
                        print("Unknown Entry")
            except ValueError as e:
                print(f"Error: Incorrect operation value")

 
            





    def startup_scrape(self):

        searchWeb = True    # set searching to ON
        teams = {}

        # Current database range
        initial_year_db = self.playerBase.get_start_year()
        final_year_db = self.playerBase.get_end_year()

        
        EARLIEST_WEB_YEAR = 1951                            # The earliest season available on the scraped website
        CURRENT_YEAR = datetime.now().year                  # The current year

        try:

            start_yr = int(input("Enter the start year to start scraping: "))
            end_yr = int(input("Enter the end year to stop scraping: "))


            # input validation
            if start_yr > end_yr:
                raise ValueError("Start year cannot be greater than end year.")

            # website bounds
            if start_yr < EARLIEST_WEB_YEAR:
                raise ValueError(f"Start year must be at least {EARLIEST_WEB_YEAR}.")

            # website boundary and latest year possible
            if end_yr > CURRENT_YEAR:
                raise ValueError(f"End year cannot be greater than {CURRENT_YEAR}.")


            # Now check the given years against boundaries already within the database
            if initial_year_db is not None and final_year_db is not None:

                # Entire range already exists, therefore no need to scrape
                if start_yr >= initial_year_db and end_yr <= final_year_db:
                    raise ValueError(f"Data for {start_yr}-{end_yr} already exists in the database.")

                # Potential overlap may exist, where current year may have more data 
                if start_yr <= final_year_db and end_yr >= initial_year_db:
                    print(f"Boundaries may overlap with the existing database data ({initial_year_db}-{final_year_db}).")


            Name(searchWeb, self.playerBase, teamDict= teams, start_year=start_yr, end_year=end_yr) 
            game_scraper = GameScraper(self.playerBase)
            game_scraper.scrape_season_games(2025)

            print("--> Data loaded successfully.")

        except ValueError as e:
            print(f"INPUT ERROR: {e}")

        except Exception as e:
            print(f"ERROR: Failed to scrape data... Continuing the application.\n {e}")
        



    def show_top_bpm_players(self):
        
        print("\nTop BPM Players:")
        players = sorted(
            list(dict.fromkeys(self.playerBase.get_normalized_bpm(2026))),
            key= lambda player: player[4],   
            reverse= True                   
        )

        for index, player in enumerate(players[:10], start= 1):
            name = f"{player[0]} {player[1]}"
            position = player[2]
            team = player[3]
            bpm = player[4]
            season = player[5]

            print(f"{index}. {name:30} {position:3} {team:3} BPM={bpm:5.2f} ({season})")



    def show_top_scoring_players(self):
        # still need to implement
        
        print("\nTop Scoring Players:")
        for player in list(self.playerBase.get_all_players())[:10]:
            print(type(player))



    def show_top_players(self):
      

        print("\nTop Players:")
        
        # for player in list(dict.fromkeys(self.playerBase.get_all_players()))[:10]:
        for player in list(dict.fromkeys(self.playerBase.get_normalized_bpm(2026)))[:10]:
            name = f"{player[0]} {player[1]}"
            position = player[2]
            team = player[3]
            bpm = player[4]
            season = player[5]

            print(f"{name:30} {position:3} {team:3} BPM={bpm:5.2f} ({season})")


    def show_operation_menu(self):
        print(f"\n\t  Menu of Operations\n\t{'_' * 22}")
        print(f"\t1. Show Top 10 Players\n\t2. Show Top 10 BPM Players\n\t3. Show Top Scoring Players\n\t4. Exit Program")



if __name__ == "__main__":
    app = UI()
