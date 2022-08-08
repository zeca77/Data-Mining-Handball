from player_models import PlayerSeasonStats, PlayerSeasonStatsSchema, GoalkeeperSeasonStatsSchema, GoalkeeperSeasonStats
from models import TeamInfo, GkInfo
import sqlalchemy
import pandas as pd
from config import db, connection
from flask import make_response, abort


# Create a handler for our read (GET) people
def get_player_season_stats(cipa, season):
    """
    TODO
    This function responds to a request for /api/games
    with the complete lists of games

    :return:        sorted list of games
    """

    # Create the list of people from our data
    season_games = (pd.DataFrame(connection.execute(sqlalchemy.select(TeamInfo).where(
        (TeamInfo.CIPA == cipa) & (TeamInfo.season == season.replace('-', '/')))).all())
                    )

    # Serialize the data for the response

    return PlayerSeasonStatsSchema().dump(
        PlayerSeasonStats(games=len(season_games.index),
                          goals=season_games.goals.sum(),
                          shots=season_games.shots.sum(),
                          technical_fouls=season_games.technical_foul.sum(),
                          assists=season_games.assists.sum(),
                          blocks=season_games.block.sum()
                          ))


def get_goalkeeper_season_stats(cipa, season):
    """
    TODO
    This function responds to a request for /api/games
    with the complete lists of games

    :return:        sorted list of games
    """

    # Create the list of people from our data
    season_gk_games = (pd.DataFrame(connection.execute(sqlalchemy.select(GkInfo).where(
        (GkInfo.CIPA == cipa) & (GkInfo.season == season.replace('-', '/')))).all())
                       )
    season_games = (pd.DataFrame(connection.execute(sqlalchemy.select(TeamInfo).where(
        (TeamInfo.CIPA == cipa) & (TeamInfo.season == season.replace('-', '/')))).all())
                    )
    # Serialize the data for the response

    return GoalkeeperSeasonStatsSchema().dump(
        GoalkeeperSeasonStats(games=len(season_gk_games.index),
                              saves=season_gk_games.saves.sum(),
                              shots_against=season_gk_games.shots.sum(),
                              technical_fouls=season_games.technical_foul.sum(),
                              shots_attempted=season_games.shots.sum(),
                              goals=season_games.goals.sum(),
                              assists=season_games.assists.sum()
                              ))
