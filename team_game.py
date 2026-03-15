#!/usr/bin/python3
from nba_api.stats.endpoints import teamgamelog
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.endpoints import playergamelogs
import typing
import nba_utils as nu
import pandas as pd
import sys

def get_ts_for_games(lookback: int, team_abbreviation: str = "SAS"):
    team_id = nu.get_team_id(team_abbreviation)
    logs = playergamelogs.PlayerGameLogs(
        team_id_nullable=team_id,
        season_nullable="2025-26"
    )
    df = logs.get_data_frames()[0]
    last_games = (
        df.sort_values("GAME_DATE", ascending=False)
        .drop_duplicates("GAME_ID")
        .head(lookback)["GAME_ID"]
    )

    name_cols = ["PLAYER_NAME"]
    all_games = df[df["GAME_ID"].isin(last_games)]
    all_games = all_games[all_games["MIN"] != "00:00"]
    totals = (
        all_games
        .groupby(name_cols)
        .agg(
            games=("PTS", "count"),
            points=("PTS", "sum"),
            fieldGoalsAttempted=("FGA", "sum"),
            freeThrowsAttempted=("FTA", "sum"),
        )
        .reset_index()
        .sort_values("points", ascending=False)
    )

    nu.get_true_shooting_percentage(totals)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("run with ./team_game.py number_of_games, short_team_name")
        sys.exit(1)
    elif len(sys.argv) == 2:
        get_ts_for_games(int(sys.argv[1]))
    else:
        get_ts_for_games(int(sys.argv[1]), sys.argv[2])
