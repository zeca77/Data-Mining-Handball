import numpy as np


def filter_prov(string):
    if "Provisório" in string or 'Observado' in string:
        return False
    else:
        return True


# this method returns the lines of a certain position inside a np array
def get_position_lines(player_lines):
    indexes = []
    columns = player_lines[0].split()
    local_line = player_lines[0]
    current_ix = 0
    for ix in columns:
        found = local_line.find(ix)
        current_ix += found
        local_line = local_line[found:]
        indexes.append(current_ix - 4)
    indexes[0] = 0
    indexes[1] = 4
    if "BV" in columns:
        indexes[10] += 1
    indexes.reverse()
    team_info = np.array([])
    for player in player_lines[1:]:
        player_info = []
        tmp = player.ljust(300)
        for index in indexes:
            lcl = tmp[index:]
            tmp = tmp[:index]
            index_info = lcl
            player_info.append(index_info.strip())
        player_info.reverse()
        player_info = np.array(player_info)
        if team_info.__len__() != 0:
            team_info = np.vstack((team_info, player_info))
        else:
            team_info = player_info
    return team_info
