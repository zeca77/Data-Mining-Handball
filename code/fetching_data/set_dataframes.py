import numpy as np
import pandas as pd


# this file has the files that return the team and goalkeeper dataframes plus auxiliary functions


# this returns the dataframe of goalkeepers

def set_gk_df(filename, season, club_id, gk_info, gk_columns, gk_cls):
    if gk_info.ndim == 1:
        gk_dataframe = pd.DataFrame(columns=gk_columns)
        gk_dataframe.loc[0] = np.where(gk_info == '', 0, gk_info)
        gk_dataframe.drop(['P&F', "%"], axis=1, inplace=True)
    else:
        gk_dataframe = pd.DataFrame(np.where(gk_info == '', 0, gk_info), columns=gk_columns).drop(['P&F', "%"], axis=1)
    try:
        while True:
            gk_cls.remove('Rem.')
    except ValueError:
        pass
    gk_dataframe.columns.values[2:] = gk_cls[1:]
    gk_dataframe[["saves", "shots"]] = dataframe_col(gk_dataframe, "Total")
    gk_dataframe[["saves_6M", "shots_6M"]] = dataframe_col(gk_dataframe, "6m")
    gk_dataframe[["saves_wing", "shots_wing"]] = dataframe_col(gk_dataframe, "Ponta")
    gk_dataframe[["saves_9M", "shots_9M"]] = dataframe_col(gk_dataframe, "9m")
    gk_dataframe[["saves_7M", "shots_7M"]] = dataframe_col(gk_dataframe, "7m")
    gk_dataframe[["saves_counter_attack", "shots_counter_attack"]] = dataframe_col(gk_dataframe, "Contra-Ataque")
    gk_dataframe.drop(["Total", "6m", 'Ponta', '9m', '7m', 'Contra-Ataque'], axis=1, inplace=True)
    gk_dataframe['Nº'] = gk_dataframe['Nº'].astype('int32')
    gk_dataframe.rename(columns={"Nº": "number",
                                 "Nome": "name"}, inplace=True)
    gk_dataframe['club_id'] = club_id
    gk_dataframe['game_id'] = filename
    gk_dataframe['season'] = season
    gk_dataframe['CIPA'] = 0

    return gk_dataframe[["game_id", "season",
                         "name",
                         "CIPA",
                         "club_id", "number",
                         "saves",
                         "shots",
                         "saves_6M", "shots_6M",
                         "saves_wing", "shots_wing",
                         "saves_9M", "shots_9M",
                         "saves_7M", "shots_7M",
                         "saves_counter_attack", "shots_counter_attack"
                         ]]


# this returns the dataframe of a team

def set_team_df(filename, season, club_id, team_info, team_cols):
    team_dataframe = pd.DataFrame(np.where(team_info == '', 0, team_info), columns=team_cols)

    team_dataframe[["goals", "shots"]] = dataframe_col(team_dataframe, "G/R")
    team_dataframe[["goals_6M", "shots_6M"]] = dataframe_col(team_dataframe, "6m")
    team_dataframe[["goals_wing", "shots_wing"]] = dataframe_col(team_dataframe, "Ponta")
    team_dataframe[["goals_9M", "shots_9M"]] = dataframe_col(team_dataframe, "9m")
    team_dataframe[["goals_7M", "shots_7M"]] = dataframe_col(team_dataframe, "7m")
    team_dataframe[["goals_counter_attack", "shots_counter_attack"]] = dataframe_col(team_dataframe, "CA")
    team_dataframe[["goals_empty_goal", "shots_empty_goal"]] = dataframe_col(team_dataframe, "BV")
    team_dataframe.drop(["%", "G/R", 'CA', "6m", 'Ponta', '9m', '7m', 'CA', 'BV'], axis=1, inplace=True)
    for col in team_dataframe.columns[team_dataframe.columns != 'Nome']:
        team_dataframe[col] = team_dataframe[col].astype(float)
    team_dataframe['Nº'] = team_dataframe['Nº'].astype('int32')
    team_dataframe['CIPA'] = 0
    team_dataframe['club_id'] = club_id
    team_dataframe['game_id'] = filename
    team_dataframe['season'] = season
    team_dataframe.rename(columns={"Nº": "number",
                                   "Nome": "name",
                                   "AS": "assists",
                                   "FT": "technical_foul",
                                   "RB": "steal",
                                   "BL": "block",
                                   "2'": "two_minutes",
                                   "CV": "red",
                                   "AM": "yellow",
                                   }, inplace=True)
    team_dataframe = team_dataframe[["game_id", "season",
                                     "name",
                                     "CIPA",
                                     "club_id",
                                     "number",
                                     "goals",
                                     "shots",
                                     "goals_6M", "shots_6M",
                                     "goals_wing", "shots_wing",
                                     "goals_9M", "shots_9M",
                                     "goals_7M", "shots_7M",
                                     "goals_counter_attack", "shots_counter_attack",
                                     "goals_empty_goal", "shots_empty_goal",
                                     "assists",
                                     "technical_foul",
                                     "steal",
                                     "block",
                                     "yellow",
                                     "two_minutes",
                                     "red",
                                     "blue",
                                     ]]
    return team_dataframe


# for a column that is divided by a "/" , this returns that column as a dataframe with 2 cols
def dataframe_col(dataframe, col):
    df = dataframe[col].str.split("/", expand=True).astype(
        float).fillna(0)
    if df.shape[1] == 1:
        df[1] = df[0]
    return df
