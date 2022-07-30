from models import TeamInfo, TeamInfoSchema, Game
from config import db
from flask import make_response, abort


# Create a handler for our read (GET) people
def read_all():
    """
    This function responds to a request for /api/team_info
    with the complete lists of games

    :return:        sorted list of games
    """
    # Create the list of people from our data
    # Create the list of people from our data
    team_info = TeamInfo.query.all()

    # Serialize the data for the response
    team_info_schema = TeamInfoSchema(many=True)
    return team_info_schema.dump(team_info)


def read_game(game_id, type):
    """
       This function responds to a request for /api/team_info
       with stats from a single game

       :return:        single game
       """
    game = Game.query.filter(Game.pdf_number == game_id).one_or_none()
    if type == 0:
        team_name = game.home_team_name
    else:
        team_name = game.away_team_name
    team_info_game = TeamInfo.query.filter(TeamInfo.game_id == game_id).filter(TeamInfo.team_name == team_name)
    team_info_schema = TeamInfoSchema(many=True)
    return team_info_schema.dump(team_info_game)
