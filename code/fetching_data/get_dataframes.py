import pandas as pd

from fetching_data.aux_fun import get_position_lines
from fetching_data.set_dataframes import set_gk_df, set_team_df


# this method returns the info of a given page
# it returns a dataframe with the field player statistics,
# one with the goalkeeper statistics,
# and a string with name of the team

def get_page_info(page_lines, filename, cipa_info, club_id):
    season = page_lines[1].split()[2]
    final_team_index = page_lines.index([i for i in page_lines if 'Banco / Equipa' in i][0])
    team_lines = page_lines[11:final_team_index]
    team_columns = page_lines[11].split()
    team_columns[-1] = 'blue'
    team_info = get_position_lines(team_lines)
    team_dataframe = set_team_df(filename, season, club_id, team_info, team_columns)
    team_dataframe['name'] = cipa_info['name']
    team_dataframe['CIPA'] = cipa_info['CIPA']
    first_gk_index = final_team_index + 3
    final_gk_index = page_lines.index([i for i in page_lines if 'Totais' in i][1])
    gk_lines = page_lines[first_gk_index:final_gk_index]
    gk_columns = page_lines[first_gk_index].split()
    gk_info = get_position_lines(gk_lines)
    gk_dataframe = set_gk_df(filename, season, club_id, gk_info, gk_columns,
                             page_lines[final_team_index + 2].split()).drop('name', axis=1).drop('CIPA', axis=1)
    gk_dataframe = pd.merge(cipa_info, gk_dataframe, how='inner', on='number')

    return team_dataframe, gk_dataframe
