import sqlalchemy
import sys

sys.path.append("..")

from fetching_data.get_lines import get_lines
from fetching_data.get_game_info import get_game_info
from fetching_data.get_club_info import get_club_info
from fetching_data.get_associate_info import get_associate_info
from config import db
from models import Game, GkInfo, TeamInfo


def get_keys():
    with open('../../keys.txt', "r") as my_file:
        return [s.rstrip() for s in my_file.readlines()]


keys = get_keys()
curr_key = 0

api_key = keys[0]
answer = input("Drop Existing tables?: (Yes/No) ")
if answer.lower() == "yes":
    db.drop_all()

# Create the database
db.create_all()
connection = db.engine.connect()


def check_key_validity():
    global api_key, lines, code, curr_key
    if code != 200:
        if "404" in code:
            print("Skipping to next")

        else:
            while curr_key < keys.__len__() and code != 200 and "404" not in code:
                print("Key is over, skipping to next")
                curr_key += 1
                api_key = keys[curr_key]
                lines, code = get_lines(filename, api_key)


answer = input("Build Database?: (Y/N) ")
if answer.lower() == "y":
    for filename in range(222155, 222156):
        filename = str(filename)
        lines, code = get_lines(filename, api_key)
        check_key_validity()
        game_info = get_game_info(lines, filename)
        db.session.add(game_info.get('game'))
        game_info.get('home_team_info').to_sql(con=db.engine, name='team_info', if_exists='append', index=False)
        game_info.get('away_team_info').to_sql(con=db.engine, name='team_info', if_exists='append', index=False)
        game_info.get('home_gk_info').to_sql(con=db.engine, name='gk_info', if_exists='append', index=False)
        game_info.get('away_gk_info').to_sql(con=db.engine, name='gk_info', if_exists='append', index=False)

    db.session.commit()
    distinct_teams_result = connection.execute(sqlalchemy.select(TeamInfo.club_id).distinct())

    for row in distinct_teams_result:
        club_id = row._mapping.get('club_id')
        db.session.add(get_club_info(club_id))
    db.session.commit()

    distinct_players_result = connection.execute(sqlalchemy.select(TeamInfo.CIPA).distinct())
    for row in distinct_players_result:
        cipa = row._mapping.get('CIPA')
        db.session.add(get_associate_info(cipa))
    db.session.commit()
