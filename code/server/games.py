from models import Game, GameSchema
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
    games = Game.query.order_by(Game.pdf_number).all()

    # Serialize the data for the response
    game_schema = GameSchema(many=True)
    return game_schema.dump(games)


def read_one(game_id):
    """
       This function responds to a request for /api/people
       with a single game

       :return:        single game
       """
    game = Game.query.filter(Game.pdf_number == game_id).one_or_none()
    if game is not None:

        # Serialize the data for the response
        game_schema = GameSchema()
        return game_schema.dump(game)
    else:
        abort(
            404,
            "Game not found for Id: {game_id}".format(game_id=game_id),
        )
