# nameScrape.py
import requests, os, time 
from bs4 import BeautifulSoup, Comment
from datetime import date


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Page headers for request 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.basketball-reference.com/",
    "Connection": "keep-alive",
}



class Name:

    def __init__(self, searchWeb, playerBase, teamDict=None, start_year=None, end_year=None):
        
        self.playerBase = playerBase
        self.teamDict = teamDict or {}

        if not searchWeb:
            print("--> Web scraping disabled.")
            return

        print("--> Scraping Basketball-Reference...")


        # Given a certain starting year to start from
        # to the most (or this) current year
        start_year = 2022 if not start_year else start_year
        end_year = date.today().year if not end_year else end_year

        for year in range(start_year, end_year + 1):

            if self.playerBase.season_exists(year):
                print(f"Skipping {year} (already scraped)")
                continue

            try:
                self.scrape_season(year)
                time.sleep(2)

            except Exception as e:
                print(f"WARNING: Failed season {year}: {e}")



  
    #
    # Scraping methods
    #


    def find_table(self, soup, table_id):

        table = soup.find("table", id=table_id)
        if table:
            return table

        comments = soup.find_all(string=lambda t: isinstance(t, Comment))
        for comment in comments:
            if table_id in comment:
                comment_soup = BeautifulSoup(c, "html.parser")
                table = comment_soup.find("table", id=table_id)
                if table:
                    return table
        return None



    def scrape_seasons(self, start, end):

        for year in range(start, end + 1):
            try:
                self.scrape_season(year)
                time.sleep(2) 
            except Exception as e:
                print(f"WARNING: Failed season {year}: {e}")




    # scrape_season - takes in the starting year of the web page to scrape
    #
    def scrape_season(self, year):


        # 
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"
        print(f"Fetching {url}")

        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        table = self.find_table(soup, "advanced")

        if table is None:
            raise RuntimeError("Advanced stats table not found")


        tbody = table.find("tbody")
        rows = tbody.find_all("tr")

        for row in rows:
            print(row.text)

            # finding player name with their corresponding team, postion, and bpm
            name_td = row.find("td", {"data-stat": "name_display"})
            if name_td is None:
                continue

            # Convert Scraped Data into desired values/types
            name = name_td.get_text(strip=True)
      
            team_td = row.find("td", {"data-stat": "team_name_abbr"})
            team = team_td.get_text(strip=True) if team_td else ""
       
            pos_td = row.find("td", {"data-stat": "pos"})
            pos = pos_td.get_text(strip=True) if pos_td else ""

            bpm_td = row.find("td", {"data-stat": "bpm"})
            try:
                bpm = float(bpm_td.get_text(strip=True)) if bpm_td else 0.0
            except ValueError:
                bpm = 0.0

            if not name or not team:
                continue

            print(f"Adding new row: {name:30s} | {team:4s} | {pos:3s} | BPM={bpm:5.2f} | {year:5d}")

            self.playerBase.insert_player(
                name=name,
                team=team,
                position=pos,
                bpm=bpm,
                season=year
            )