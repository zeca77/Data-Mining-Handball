from models import Associate, AssociateSchema
from config import db
from flask import make_response, abort


def read_all():
    """
    This function responds to a request for /api/associates
    with the complete list of associates

    :return:        sorted list of associates
    """

    associates = Associate.query.order_by(Associate.cipa).all()

    # Serialize the data for the response
    associate_schema = AssociateSchema(many=True)
    return associate_schema.dump(associates)


def read_one(cipa):
    """
       This function responds to a request for /api/associates
       with a single associates

       :return:        single associate
       """
    aassociate = Associate.query.filter(Associate.cipa == cipa).one_or_none()
    if aassociate is not None:

        # Serialize the data for the response
        associate_schema = AssociateSchema()
        return associate_schema.dump(aassociate)
    else:
        abort(
            404,
            "Associate not found for CIPA: {cipa}".format(cipa=cipa),
        )
