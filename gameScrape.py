# gameScrape.py
import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import random


class GameScraper:
    """
    GameScraper - scrapes NBA game schedules and results from
                  Basketball Reference and stores them in the database.
    """

    # Months used by Basketball Reference schedule pages
    MONTHS = [  "october", "november", "december",
                "january", "february", "march",
                "april", "may", "june" ]


    def __init__(self, db, start_year=None, end_year=None):
        """
        Initialize the scraper with a database object.
        Parameters:
            db         : Database object used to store game data.
            start_year : First NBA season year to scrape.
            end_year   : Last NBA season year to scrape.
        """

        self.db = db

        # Reuse a single HTTP session for all requests
        self.session = requests.Session()

        # Provide a browser-like User-Agent to reduce blocking
        self.session.headers.update({
            "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
        })

        print("--> Scraping Basketball-Reference...")

        # Given a certain starting year to start from
        # to the most current year
        start_year = 2022 if not start_year else start_year
        end_year = date.today().year if not end_year else end_year

        # Iterate through each season
        for year in range(start_year, end_year + 1):

            # Skip seasons already stored in database
            if self.db.season_games_exists(year):
                print(f"Skipping {year} (already scraped)")
                continue

            try:
                self.scrape_season_games(year)

                # Delay between seasons to avoid rate limiting
                delay = random.uniform(3, 5)
                print(f"Waiting {delay:.1f} seconds.")
                time.sleep(delay)

            except Exception as e:
                print(f"WARNING: Failed season {year}: {e}")

    def scrape_season_games(self, year):
        """
        Scrape all completed NBA games for a given season.

        Basketball Reference stores schedules in separate monthly pages.
        Example:
            NBA_2024_games-october.html
            NBA_2024_games-november.html
            ...
        """

        print(f"\n--- Scraping {year} Season ---")

        # Iterate through all possible schedule months
        for month in self.MONTHS:

            url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
            

            try:

                # Random delay before each request
                delay = random.uniform(3, 5)
                print(f"Waiting {delay:.1f} seconds before requesting {month}.")
                time.sleep(delay)

                # Send request to retrieve webpage
                r = self.session.get(url, timeout=30)

                # Month page does not exist
                if r.status_code == 404:
                    continue

                # Rate limited by website
                if r.status_code == 429:
                    raise Exception("Rate limited (429). Wait a while before trying again.")

                # Raise exception for other HTTP errors
                r.raise_for_status()

                print(f"Processing {month.capitalize()} {year}")

                # Parse the HTML content
                soup = BeautifulSoup(r.text, "html.parser")

                # Locate the schedule table
                table = soup.find("table", id="schedule")

                if not table:
                    continue

                # Locate all game rows
                rows = table.find("tbody").find_all("tr")

                # Process each game row
                for row in rows:

                    # Extract the game date
                    date_td = row.find("th", {"data-stat": "date_game"})

                    # Extract team names
                    away_td = row.find("td", {"data-stat": "visitor_team_name"})
                    home_td = row.find("td", {"data-stat": "home_team_name"})

                    # Extract team scores
                    away_pts_td = row.find("td", {"data-stat": "visitor_pts"})
                    home_pts_td = row.find("td", {"data-stat": "home_pts"})

                    # Skip rows missing desired data
                    if not all([date_td, away_td, home_td, away_pts_td, home_pts_td]):
                        continue

                    # Skip games that have not yet been played
                    if (not away_pts_td.text.strip() or not home_pts_td.text.strip()):
                        continue

                    # Convert scraped data into desired values/types
                    game_date = date_td.text.strip()

                    away_team = away_td.text.strip()
                    home_team = home_td.text.strip()

                    away_score = int(away_pts_td.text.strip())
                    home_score = int(home_pts_td.text.strip())

                    # Store the game in the database
                    self.db.insert_game(
                        game_date,
                        year,
                        home_team,
                        away_team,
                        home_score,
                        away_score
                    )

                    # Display inserted game information
                    print(f"{game_date}: {away_team} {away_score} @ {home_team} {home_score}")

            except Exception as e:
                print(f"WARNING: Failed {month} {year}: {e}")