import nba_utils as nu
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv3
import pandas as pd

SPURS = "SAS"

games = scoreboard.ScoreBoard()
games_dict = games.get_dict()



for game in games_dict["scoreboard"]["games"]:
    home = game["homeTeam"]["teamTricode"]
    away = game["awayTeam"]["teamTricode"]
    spursId = nu.get_team_id(SPURS)

    if SPURS in (home, away):
        game_id = game["gameId"]
        print("Spurs game found:", home, "at", away)
        print(game_id)

        box = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)
        players: pd.DataFrame = box.get_data_frames()[0] # 0 is player box score, 1 is starters vs bench, 2 is whole team
        df: pd.DataFrame = players.loc[players["teamId"] == spursId]
        nu.get_true_shooting_percentage(df)