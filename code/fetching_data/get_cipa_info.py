import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_cipa_info(game_nr):
    url = f"http://si.fpa.pt/fap_sa/usrpck_print.print_boletim?p_sessao=1&P_ID_PROVA_JOGO={game_nr}&p_layout=P300632"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    def get_team_tables():
        tables = doc.find_all(class_="tabela")
        found_home = False
        found_away = False
        for x in tables:
            if "Equipa A" in x.text:
                home_table = x
                found_home = True
            elif 'Equipa B' in x.text and "::" in x.text:
                away_table = x
                found_away = True
                # stop the loop earlier
            if found_home and found_away:
                return home_table, away_table

    home_team_table, away_team_table = get_team_tables()

    def get_team_info(team_table):
        player_rows = []
        for row in team_table.find_all('tr'):
            if row.findChild().text.isdigit():
                player_rows.append(row)
        info_rows = []
        for pl_row in player_rows:
            player_info = pl_row.find_all('td')
            player_number = player_info[0].text.strip()
            player_cipa = player_info[1].text.strip()
            player_full_name = player_info[2].text.strip()
            info_rows.append([player_number, player_cipa, player_full_name])
        return np.array(info_rows)

    home_team_df = pd.DataFrame(get_team_info(home_team_table), columns=['number', 'CIPA', 'name'])
    away_team_df = pd.DataFrame(get_team_info(away_team_table), columns=['number', 'CIPA', 'name'])
    home_team_df[['number', 'CIPA']] = home_team_df[['number', 'CIPA']].astype(int)
    away_team_df[['number', 'CIPA']] = away_team_df[['number', 'CIPA']].astype(int)

    return home_team_df, away_team_df


home_team_info, away_team_info = get_cipa_info(
    game_nr='227900')
