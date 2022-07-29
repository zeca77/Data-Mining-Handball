import pandas as pd
import numpy as np
import mysql.connector
from pandas.io import sql
from extract_pdf import get_lines
from sqlalchemy import create_engine
import requests
import base64
import time


def get_team_info(page_lines):
    game_number = page_lines[4].split()[2]
    team_name = page_lines[9].strip()
    columns = page_lines[11].split()
    final_team_index = page_lines.index([i for i in page_lines if 'Banco / Equipa' in i][0]) - 1
    team_lines = page_lines[12:final_team_index]
    indexes = []
    local_line = page_lines[11]
    current_ix = 0
    columns[-1] = 'blue'
    for ix in columns:
        found = local_line.find(ix)
        current_ix += found
        local_line = local_line[found:]
        indexes.append(current_ix)
    indexes.reverse()
    team_info = np.array([])
    for player in team_lines:
        player_info = []
        tmp = player.ljust(300)
        for index in indexes:
            lcl = tmp[index:]
            tmp = tmp[:index]
            index_info = lcl
            player_info.append(index_info.strip())
        player_info.reverse()
        np.array(player_info)
        if team_info.__len__() != 0:
            team_info = np.vstack((team_info, np.array(player_info)))
        else:
            team_info = player_info
    team_dataframe = pd.DataFrame(np.where(team_info == '', 0, team_info), columns=columns)
    team_dataframe[["goals", "shots"]] = dataframe_col(team_dataframe, "G/R")
    team_dataframe[["goals_6M", "shots_6M"]] = dataframe_col(team_dataframe, "6m")
    team_dataframe[["goals_wing", "shots_wing"]] = dataframe_col(team_dataframe, "Ponta")
    team_dataframe[["goals_9M", "shots_9M"]] = dataframe_col(team_dataframe, "9m")
    team_dataframe[["goals_7M", "shots_7M"]] = dataframe_col(team_dataframe, "7m")
    team_dataframe[["goals_counter-attack", "shots_counter-attack"]] = dataframe_col(team_dataframe, "CA")
    team_dataframe[["goals_empty_goal", "shots_empty_goal"]] = dataframe_col(team_dataframe, "BV")
    team_dataframe.drop(["%", "G/R", 'CA', "6m", 'Ponta', '9m', '7m', 'CA', 'BV'], axis=1, inplace=True)
    for col in team_dataframe.columns[team_dataframe.columns != 'Nome']:
        team_dataframe[col] = team_dataframe[col].astype(float)
    team_dataframe['Nº'] = team_dataframe['Nº'].astype('int32')
    team_dataframe['team_name'] = team_name
    team_dataframe['game_id'] = game_number
    team_dataframe.rename(columns={"Nº": "number",
                                   "Nome": "name",
                                   "AS": "assists",
                                   "FT": "technical_foul",
                                   "RB": "steal",
                                   "BL": "block",
                                   "2'": "2_minutes",
                                   "CV": "red",
                                   "AM": "yellow",
                                   }, inplace=True)

    return team_dataframe[["game_id",
                           "name",
                           "team_name",
                           "number",
                           "goals",
                           "shots",
                           "goals_6M", "shots_6M",
                           "goals_wing", "shots_wing",
                           "goals_9M", "shots_9M",
                           "goals_7M", "shots_7M",
                           "goals_counter-attack", "shots_counter-attack",
                           "goals_empty_goal", "shots_empty_goal",
                           "assists",
                           "technical_foul",
                           "steal",
                           "block",
                           "yellow",
                           "2_minutes",
                           "red",
                           "blue",
                           ]]


def dataframe_col(team_dataframe, col):
    df = team_dataframe[col].str.split("/", expand=True).astype(
        float).fillna(0)
    if df.columns.size == 1:
        df[1] = df[0]
    return df


filename = "227903"

lines = get_lines(filename)

find_string = lines[0].strip()
page_indexes = []

for i in range(len(lines)):
    if find_string in lines[i]:
        page_indexes.append(i)

line6_list = lines[6].replace('(', '').replace(')', '').split()
page_2_index = page_indexes[1]
page_3_index = page_indexes[2]

arg_dictionary = {
    "championship_name": lines[0].strip(),
    "game_week": int(lines[1].split()[0][-2:]),
    "season": lines[1].split()[2],
    "date": lines[2].strip(),
    "time": lines[3].split()[2],
    "game_number": int(lines[4].split()[2]),
    "game_location": " ".join(lines[4].split()[3:]),
    "home_team_score": int(lines[5].split()[0]),
    "away_team_score": int(lines[5].split()[2]),
    "home_team_score_first_half": int(line6_list[0]),
    "away_team_score_first_half": int(line6_list[2]),
    "home_team_score_second_half": int(line6_list[3]),
    "away_team_score_second_half": int(line6_list[5]),
    "referee1": lines[7].strip(),
    "referee2": lines[8].strip(),
    "home_team_info": get_team_info(lines[:page_2_index - 1]),
    "away_team_info": get_team_info(lines[page_2_index:page_3_index - 1])
}


class Game:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


game = Game(arg_dictionary)

db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="testdatabase")
my_cursor = db.cursor()
answer = input("Drop Existing tables?: (Y/N) ")
if answer == "Y":
    my_cursor.execute("DROP TABLE games")
    my_cursor.execute("DROP TABLE team_info")
    # Create the table
    my_cursor.execute(
        """
        CREATE TABLE games(
        championship_name VARCHAR(30) NOT NULL,
        game_week TINYINT NOT NULL,
        season VARCHAR(30) NOT NULL,
        date VARCHAR(30) NOT NULL,
        time VARCHAR(30) NOT NULL,
        game_number TINYINT NOT NULL PRIMARY KEY,
        game_location VARCHAR(30) NOT NULL,
        home_team_score TINYINT NOT NULL,
        away_team_score TINYINT NOT NULL,
        home_team_score_first_half TINYINT NOT NULL,
        away_team_score_first_half TINYINT NOT NULL,
        home_team_score_second_half TINYINT NOT NULL,
        away_team_score_second_half TINYINT NOT NULL,
        referee1 VARCHAR(30) NOT NULL,
        referee2 VARCHAR(30) NOT NULL
        )
        """
    )

sql_order = """INSERT INTO games VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s,%s ,%s ,%s ,%s ,%s ,%s)"""
val = (
    game.championship_name, game.game_week, game.season, game.date, game.time, game.game_number,
    game.game_location, game.home_team_score, game.away_team_score,
    game.home_team_score_first_half, game.away_team_score_first_half,
    game.home_team_score_second_half, game.away_team_score_second_half,
    game.referee1,
    game.referee2)
my_cursor.execute(sql_order, val)
db.commit()
my_conn = create_engine("mysql://root:root@localhost/testdatabase")
game.home_team_info.to_sql(con=my_conn, name='team_info', if_exists='append', index=False)
game.away_team_info.to_sql(con=my_conn, name='team_info', if_exists='append', index=False)
