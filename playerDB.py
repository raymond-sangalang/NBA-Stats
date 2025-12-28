import sqlite3, os, math
from collections import defaultdict


DB_FILE = "nba.db"


class nbaDatabase:
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cur = self.conn.cursor()
        self._create_schema()

    
    # creating table schema
    def _create_schema(self):
        
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                position TEXT,
                team TEXT,
                bpm REAL,
                season INTEGER
            )
        """)

        # Indexes 
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_season ON Player(season)")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_team ON Player(team)")
        self.cur.execute("CREATE INDEX IF NOT EXISTS idx_position ON Player(position)")
        self.conn.commit()


    # inserting player in Player table
    def insert_player(self, name, team, position, bpm, season):
        
        parts = name.split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""

        self.cur.execute("""
            INSERT INTO Player (first_name, last_name, position, team, bpm, season)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first, last, position, team, bpm, season))

        self.conn.commit()

 
    # Queries
    def get_all_players(self):
        
        self.cur.execute("""
            SELECT first_name, last_name, position, team, bpm, season
            FROM Player
            ORDER BY season DESC, bpm DESC
        """)
        return self.cur.fetchall()

    def get_players_by_team(self, team):
        
        self.cur.execute("""
            SELECT first_name, last_name, position, bpm, season
            FROM Player
            WHERE team = ?
            ORDER BY season DESC, bpm DESC
        """, (team,))
        return self.cur.fetchall()

    def get_players_by_season(self, season):
        
        self.cur.execute("""
            SELECT first_name, last_name, position, team, bpm
            FROM Player
            WHERE season = ?
            ORDER BY bpm DESC
        """, (season,))
        return self.cur.fetchall()


    # normalized bpm
    def get_normalized_bpm(self, season):
       
        self.cur.execute("""
            SELECT position, bpm
            FROM Player
            WHERE season = ? AND bpm IS NOT NULL
        """, (season,))
        rows = self.cur.fetchall()

        pos_vals = defaultdict(list)
        for pos, bpm in rows:
            pos_vals[pos].append(bpm)

        stats = {}
        for pos, vals in pos_vals.items():
            mean = sum(vals) / len(vals)
            std = math.sqrt(sum((v-mean)**2 for v in vals) / len(vals)) or 1.0
            stats[pos] = (mean, std)

        self.cur.execute("""
            SELECT first_name, last_name, position, team, bpm
            FROM Player
            WHERE season = ?
        """, (season,))

        normalized = []
        for fn, ln, pos, team, bpm in self.cur.fetchall():
            mean, std = stats.get(pos, (0, 1))
            z = (bpm - mean) / std
            normalized.append((fn, ln, pos, team, bpm, round(z, 3)))

        return normalized


    def close(self):
        self.conn.close()
