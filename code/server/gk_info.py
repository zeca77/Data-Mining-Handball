from models import GkInfo, GkInfoSchema, Game
from config import db
from flask import make_response, abort


# Create a handler for our read (GET) people
def read_all():
    """
    This function responds to a request for /api/games
    with the complete lists of games

    :return:        sorted list of games
    """
    # Create the list of people from our data
    # Create the list of people from our data
    gk_info_game = GkInfo.query.all()

    # Serialize the data for the response
    gk_info_schema = GkInfoSchema(many=True)
    return gk_info_schema.dump(gk_info_game)


def read_game(game_id, type):
    """
       This function responds to a request for /api/gk_info
       with stats from a single game

       :return:        single game
       """
    game = Game.query.filter(Game.pdf_number == game_id).one_or_none()
    if type == 0:
        team_name = game.home_team_name
    else:
        team_name = game.away_team_name

    gk_info_game = GkInfo.query.filter(GkInfo.game_id == game_id).filter(GkInfo.team_name == team_name)
    gk_info_schema = GkInfoSchema(many=True)
    return gk_info_schema.dump(gk_info_game)
