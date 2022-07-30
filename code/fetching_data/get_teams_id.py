from bs4 import BeautifulSoup
import requests


def get_teams_id(game):
    url = f"https://portal.fpa.pt/jogo/{game}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    club_ids = []
    for link in doc.find_all('a'):
        ref = link.get('href')
        if 'clube/id' in ref and ref not in club_ids:
            club_ids.append(ref)
    home_club_id = int(club_ids[0].rpartition('https://portal.fpa.pt/clube/id/')[2])
    away_club_id = int(club_ids[1].rpartition('https://portal.fpa.pt/clube/id/')[2])
    return home_club_id, away_club_id
