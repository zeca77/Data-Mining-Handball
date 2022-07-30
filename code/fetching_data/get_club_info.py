from bs4 import BeautifulSoup
import requests
from models import Club


def get_club_info(club_id):
    url = f'https://portal.fpa.pt/clube/id/{club_id}'

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    club_details = doc.find('div', class_="club-detail__content")

    club_name = club_details.find('h3').get_text()

    rows = club_details.find_all('tr')

    address = ' '.join(rows[0].find_all('td')[1].get_text().split())

    phone_number = rows[1].find_all('td')[1].get_text()

    home_ground = rows[-1].find_all('td')[1].get_text()
    image_url = doc.find('meta', attrs={'name': "twitter:image"})['content']

    return Club(club_id=club_id,
                club_name=club_name,
                address=address,
                phone_number=phone_number,
                home_ground=home_ground,
                image_url=image_url)
