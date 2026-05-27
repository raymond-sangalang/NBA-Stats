import requests
from bs4 import BeautifulSoup


class GameScraper:

    def __init__(self, db):
        self.db = db

    def scrape_season_games(self, year):

        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", id="schedule")
        rows = table.find("tbody").find_all("tr")

        for row in rows:

            date_td = row.find("th", {"data-stat": "date_game"})
            print(f"date_td: {date_td}")

            away_td = row.find("td", {"data-stat": "visitor_team_name"})
            home_td = row.find("td", {"data-stat": "home_team_name"})

            away_pts_td = row.find("td", {"data-stat": "visitor_pts"})
            home_pts_td = row.find("td", {"data-stat": "home_pts"})


            if not all([date_td, away_td, home_td, away_pts_td, home_pts_td]):
                continue


            game_date = date_td.text.strip()

            away_team = away_td.text.strip()
            home_team = home_td.text.strip()

            away_score = int(away_pts_td.text.strip())
            home_score = int(home_pts_td.text.strip())


            self.db.insert_game(
                game_date,
                year,
                home_team,
                away_team,
                home_score,
                away_score
            )

            print(
                f"{away_team} {away_score} @ "
                f"{home_team} {home_score}"
            )