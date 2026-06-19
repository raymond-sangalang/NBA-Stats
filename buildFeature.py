# buildFeature.py

def build_features(db, home_team, away_team):
    """
    Build the feature vector that will be used by the prediction model.
    Retrives the average Plus/Minus (BPM) for both teams and returns them
    as a list of features.

    Parameters:
        db: Database object
        home_team: Name of the home team.
        away_team: Name of the away team

    Returns:
        Feature vector as a list containing home teams average bpm
        and the away teams average bpm.
    """

    # Get the average BPM for the home team
    home_bpm = db.get_team_avg_bpm(home_team)

    # Get the average BPM for the away team
    away_bpm = db.get_team_avg_bpm(away_team)

    # Return the feature vector for model input
    return [home_bpm, away_bpm]