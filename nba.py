#!/usr/bin/python3
import typing
from nba_api.stats.endpoints import playercareerstats
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams

global_teams = dict()

nba_teams = teams.get_teams()
global_teams = {
    team['full_name']: team['id'] for team in teams.get_teams()
}
