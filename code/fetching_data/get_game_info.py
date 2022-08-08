from fetching_data.get_cipa_info import get_cipa_info
from fetching_data.get_dataframes import get_page_info
from fetching_data.get_teams_id import get_teams_id
from models import Game


# returns a dictionary with the info of the game
def get_game_info(lines, filename):
    find_string = lines[0].strip()
    page_indexes = []
    for i in range(len(lines)):
        if find_string in lines[i]:
            page_indexes.append(i)
    line6_list = lines[6].replace('(', '').replace(')', '').split()
    page_2_index = page_indexes[1]
    page_1_lines = lines[:page_2_index - 1]
    page_2_lines = lines[page_2_index:]
    home_cipa_info, away_cipa_info, game_week = get_cipa_info(filename)
    home_team_id, away_team_id = get_teams_id(filename)
    home_team_info, home_gk_info = get_page_info(page_lines=page_1_lines,
                                                 filename=filename,
                                                 cipa_info=home_cipa_info,
                                                 club_id=home_team_id)
    away_team_info, away_gk_info = get_page_info(page_lines=page_2_lines,
                                                 filename=filename,
                                                 cipa_info=away_cipa_info,
                                                 club_id=away_team_id)
    game = Game(championship_name=lines[0].strip(),
                game_week=int(game_week),
                season=lines[1].split()[2],
                date=lines[2].strip(),
                time=lines[3].split()[2],
                pdf_number=filename,
                game_location=" ".join(lines[4].split()[3:]),
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                home_team_score=int(lines[5].split()[0]),
                away_team_score=int(lines[5].split()[2]),
                home_team_score_first_half=int(line6_list[0]),
                away_team_score_first_half=int(line6_list[2]),
                home_team_score_second_half=int(line6_list[3]),
                away_team_score_second_half=int(line6_list[5]),
                referee1=lines[7].strip(),
                referee2=lines[8].strip()
                )
    arg_dictionary = {
        "game": game,
        "home_team_info": home_team_info,
        "away_team_info": away_team_info,
        "home_gk_info": home_gk_info,
        "away_gk_info": away_gk_info
    }
    return arg_dictionary
