# gameScrape.py
import requests
from bs4 import BeautifulSoup


class GameScraper:
    """
    GameScraper - scrapes the NBA game schedules and results from the 
                  Basketball Reference and stored them in the database
    """

    def __init__(self, db):
        """
        Initialize the scraper with a database object.
        The database object will have a method to insert game data in the database

        """
        self.db = db

    def scrape_season_games(self, year):
        """
        Scrape all completed NBA regular season games for a given year.
        Retrieves the schedule and results page from the Basketball Reference
        resource. Extracts game information, and inserts each game into the database.
        """

        # Define the Basketball Reference URL for the season
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games.html"
        
        # Send request to retrieve the webpage
        r = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(r.text, "html.parser")

        # Locate the schedule table as well as all game rows
        table = soup.find("table", id="schedule")
        rows = table.find("tbody").find_all("tr")

        # Process each game row
        for row in rows:

            # Extract the game date
            date_td = row.find("th", {"data-stat": "date_game"})
            print(f"date_td: {date_td}")

            # Extract team names
            away_td = row.find("td", {"data-stat": "visitor_team_name"})
            home_td = row.find("td", {"data-stat": "home_team_name"})

            # Extract team scores
            away_pts_td = row.find("td", {"data-stat": "visitor_pts"})
            home_pts_td = row.find("td", {"data-stat": "home_pts"})

            # Check if the rows is missing desired data and skip if true
            if not all([date_td, away_td, home_td, away_pts_td, home_pts_td]):
                continue


            # Convert scraped data into desired values/types
            game_date = date_td.text.strip()

            away_team = away_td.text.strip()
            home_team = home_td.text.strip()

            away_score = int(away_pts_td.text.strip())
            home_score = int(home_pts_td.text.strip())


            # Store the game in the database
            self.db.insert_game(game_date, year, home_team, away_team, home_score, away_score)

            # Display insered game information
            print(f"{away_team} {away_score} @ {home_team} {home_score}")