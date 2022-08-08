from datetime import datetime
from config import db, ma


class Game(db.Model):
    __tablename__ = 'games'
    championship_name = db.Column(db.String(60))
    game_week = db.Column(db.Integer)
    season = db.Column(db.String(60))
    date = db.Column(db.String(60))
    time = db.Column(db.String(60))
    pdf_number = db.Column(db.Integer, primary_key=True)
    game_location = db.Column(db.String(60))
    home_team_id = db.Column(db.String(60))
    away_team_id = db.Column(db.String(60))
    home_team_score = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)
    home_team_score_first_half = db.Column(db.Integer)
    away_team_score_first_half = db.Column(db.Integer)
    home_team_score_second_half = db.Column(db.Integer)
    away_team_score_second_half = db.Column(db.Integer)
    referee1 = db.Column(db.String(60))
    referee2 = db.Column(db.String(60))


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True


class TeamInfo(db.Model):
    __tablename__ = 'team_info'
    game_id = db.Column(db.String(60), primary_key=True)
    season = db.Column(db.String(60))
    name = db.Column(db.String(60))
    CIPA = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    shots = db.Column(db.Integer)
    goals_6M = db.Column(db.Integer)
    shots_6M = db.Column(db.Integer)
    goals_wing = db.Column(db.Integer)
    shots_wing = db.Column(db.Integer)
    goals_9M = db.Column(db.Integer)
    shots_9M = db.Column(db.Integer)
    goals_7M = db.Column(db.Integer)
    shots_7M = db.Column(db.Integer)
    goals_counter_attack = db.Column(db.Integer)
    shots_counter_attack = db.Column(db.Integer)
    goals_empty_goal = db.Column(db.Integer)
    shots_empty_goal = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    technical_foul = db.Column(db.Integer)
    steal = db.Column(db.Integer)
    block = db.Column(db.Integer)
    yellow = db.Column(db.Integer)
    two_minutes = db.Column(db.Integer)
    red = db.Column(db.Integer)
    blue = db.Column(db.Integer)


class TeamInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TeamInfo
        load_instance = True


class GkInfo(db.Model):
    __tablename__ = 'gk_info'

    game_id = db.Column(db.String(60), primary_key=True)
    season = db.Column(db.String(60))
    name = db.Column(db.String(60))
    CIPA = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    shots = db.Column(db.Integer)
    saves_6M = db.Column(db.Integer)
    shots_6M = db.Column(db.Integer)
    saves_wing = db.Column(db.Integer)
    shots_wing = db.Column(db.Integer)

    saves_9M = db.Column(db.Integer)
    shots_9M = db.Column(db.Integer)
    saves_7M = db.Column(db.Integer)
    shots_7M = db.Column(db.Integer)
    saves_counter_attack = db.Column(db.Integer)
    shots_counter_attack = db.Column(db.Integer)


class GkInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GkInfo
        load_instance = True


class Club(db.Model):
    __tablename__ = 'clubs'
    club_id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(60))
    address = db.Column(db.String(100))
    home_ground = db.Column(db.String(60))
    image_url = db.Column(db.String(120))


class ClubSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Club
        load_instance = True


class Associate(db.Model):
    __tablename__ = 'associates'
    cipa = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    date_of_birth = db.Column(db.String(60))
    role = db.Column(db.String(60))
    picture_url = db.Column(db.String(60))


class AssociateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Associate
        load_instance = True
