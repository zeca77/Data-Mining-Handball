from models import Club, ClubSchema
from config import db
from flask import make_response, abort


# Create a handler for our read (GET) people
def read_all():
    """
    This function responds to a request for /api/clubs
    with the complete lists of clubs

    :return:        sorted list of clubs
    """
    # Create the list of people from our data
    clubs = Club.query.order_by(Club.club_id).all()

    # Serialize the data for the response
    club_schema = ClubSchema(many=True)
    return club_schema.dump(clubs)


def read_one(club_id):
    """
       This function responds to a request for /api/people
       with a single game

       :return:        single game
       """
    club = Club.query.filter(Club.club_id == club_id).one_or_none()
    if club is not None:

        # Serialize the data for the response
        club_schema = ClubSchema()
        return club_schema.dump(club)
    else:
        abort(
            404,
            "Club not found for Club Id: {club_id}".format(club_id=club_id),
        )
