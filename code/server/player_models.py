from config import db, ma
from marshmallow import fields
from models import TeamInfo
import sqlalchemy
import pandas as pd


class PlayerSeasonStats:
    def __init__(self, games, goals, shots, technical_fouls,
                 assists, blocks):
        self.games = games
        self.goals = goals
        self.shots = shots
        self.technical_fouls = technical_fouls
        self.assists = assists
        self.blocks = blocks


class PlayerSeasonStatsSchema(ma.Schema):
    games = fields.Integer()
    goals = fields.Integer()
    shots = fields.Integer()
    technical_fouls = fields.Integer()
    assists = fields.Integer()
    blocks = fields.Integer()


class GoalkeeperSeasonStats:
    def __init__(self, games, saves, shots_against, technical_fouls, shots_attempted, goals, assists):
        self.games = games
        self.saves = saves
        self.shots_against = shots_against
        self.technical_fouls = technical_fouls
        self.shots_attempted = shots_attempted
        self.goals = goals
        self.assists = assists


class GoalkeeperSeasonStatsSchema(ma.Schema):
    games = fields.Integer()
    saves = fields.Integer()
    shots_against = fields.Integer()
    technical_fouls = fields.Integer()
    shots_attempted = fields.Integer()
    goals = fields.Integer()
    assists = fields.Integer()
