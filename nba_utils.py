#!/usr/bin/python3
import pandas as pd
import typing

from nba_api.stats.static import teams

TEAM_IDS = { nba_team['abbreviation']: nba_team['id'] for nba_team in teams.get_teams()}

def get_team_id(abbrev: str):
    return TEAM_IDS[abbrev]

def get_true_shooting_percentage(df: pd.DataFrame):
    rows = []
    columns = ["Names", "Games", "Points", "FGA", "FTA", "TS%"]
    for ix, row in df.iterrows():
        if "firstName" in row:
            name = f"{row['firstName']} {row['familyName']}"
        else:
            name = row["PLAYER_NAME"]
        points = row['points']
        attempts = row['fieldGoalsAttempted']
        free_throw_attempts = row['freeThrowsAttempted']
        games = row['games']
        denominator = 2 * (attempts + (0.44 * free_throw_attempts))
        if denominator > 0:
            tspct = (100 *points) / denominator
        else:
            tspct = 0

        rows.append([name, games, points, attempts, free_throw_attempts, tspct])
    stats_df = pd.DataFrame(rows, columns=columns)
    return stats_df

def get_teams():
    print(TEAM_IDS)

    
if __name__ == "__main__":
    get_teams()
