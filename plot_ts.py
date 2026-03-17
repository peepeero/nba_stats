#!/usr/bin/python3
import subprocess
import time
from nba_api.stats.endpoints import teamgamelog
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.endpoints import playergamelogs
import typing
import nba_utils as nu
import pandas as pd
import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def createGraphTSToPoints(df: pd.DataFrame, lookback: int):
    df["PPG"] = df["Points"] / df["Games"]
    df_filtered = df[df["PPG"] > 5]
    plt.scatter(df_filtered["PPG"], df_filtered["TS%"])
    plt.xlabel("PPG")
    plt.ylabel("True Shooting Pct")
    plt.title("PPG vs True Shooting Percentage")
    for i, row in df_filtered.iterrows():
        plt.text(row["PPG"], row["TS%"], row["Names"].split()[0])
    plt.savefig("scatter.png")
    subprocess.run(["explorer.exe", "scatter.png"])
    return

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

    tsDf: pd.DataFrame = nu.get_true_shooting_percentage(totals)
    createGraphTSToPoints(tsDf, lookback)
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("run with ./team_game.py number_of_games, short_team_name")
        sys.exit(1)
    elif len(sys.argv) == 2:
        get_ts_for_games(int(sys.argv[1]))
    else:
        get_ts_for_games(int(sys.argv[1]), sys.argv[2])
