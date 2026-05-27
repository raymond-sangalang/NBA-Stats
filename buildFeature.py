

def build_features(db, home_team, away_team):

    home_bpm = db.get_team_avg_bpm(home_team)
    away_bpm = db.get_team_avg_bpm(away_team)

    return [
        home_bpm,
        away_bpm
    ]