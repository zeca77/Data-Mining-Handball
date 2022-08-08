import sqlalchemy
import sys

sys.path.append("..")
from fetching_data.get_lines import get_lines
from fetching_data.get_game_info import get_game_info
from fetching_data.get_club_info import get_club_info
from fetching_data.get_associate_info import get_associate_info
from config import db, connection
from models import Game, GkInfo, TeamInfo, Associate, Club


def get_keys():
    with open('../../keys.txt', "r") as my_file:
        return [s.rstrip() for s in my_file.readlines()]


def get_games_with_issues():
    with open('../../Games with issues.txt', "r") as my_file:
        return [s.rstrip() for s in my_file.readlines()]


keys = get_keys()
games_with_issues = get_games_with_issues()
curr_key = 0

api_key = keys[0]
answer = input("Drop Existing tables?: (Yes/No) ")
if answer.lower() == "yes":
    input('Are you sure?')
    if answer.lower() == "y":
        db.drop_all()

# Create the database

db.create_all()


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


def fill_clubs_table():
    print("Filling clubs table...")
    distinct_teams_result = connection.execute(
        sqlalchemy.select(TeamInfo.club_id).distinct().where(TeamInfo.club_id.notin_(sqlalchemy.select(Club.club_id))))
    for row in distinct_teams_result:
        club_id = row._mapping.get('club_id')
        db.session.add(get_club_info(club_id))
    db.session.commit()
    print("Clubs table Filled.")


def fill_associates_table():
    print("Filling associates table...")
    distinct_players_result = connection.execute(
        sqlalchemy.select(TeamInfo.CIPA).distinct().where(TeamInfo.CIPA.notin_(sqlalchemy.select(Associate.cipa))))
    for row in distinct_players_result:
        cipa = row._mapping.get('CIPA')
        db.session.add(get_associate_info(cipa))
    db.session.commit()
    print("Associates table Filled.")


def insert_dataframe_to_table(dataframe, table_name):
    try:
        dataframe.to_sql(con=db.engine, name=table_name, if_exists='append', index=False)
    except sqlalchemy.exc.IntegrityError:
        print('Duplicate Entry')


if answer.lower() == "y":
    for filename in range(228050, 228053):
        if filename % 10 == 0:
            db.session.commit()

        filename = str(filename)
        if filename not in games_with_issues:
            lines, code = get_lines(filename, api_key)
            check_key_validity()
            game_info = get_game_info(lines, filename)
            db.session.add(game_info.get('game'))
            insert_dataframe_to_table(dataframe=game_info.get('home_team_info'), table_name='team_info')
            insert_dataframe_to_table(dataframe=game_info.get('away_team_info'), table_name='team_info')
            insert_dataframe_to_table(dataframe=game_info.get('home_gk_info'), table_name='gk_info')
            insert_dataframe_to_table(dataframe=game_info.get('away_gk_info'), table_name='gk_info')
    db.session.commit()
    fill_clubs_table()
    fill_associates_table()
# my_dude= PlayerSeasonStats(202230,'2021/22',connection)
