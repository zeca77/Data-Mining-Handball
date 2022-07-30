from bs4 import BeautifulSoup
import requests
from models import Associate


def get_associate_info(cipa):
    url = f"https://portal.fpa.pt/associado/{cipa}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    details = doc.find('body').find('div', class_="association-detail")
    name = details.find('h3').get_text()
    info_table = details.find_all('td')
    date_of_birth = info_table[3].get_text()
    role = info_table[5].get_text()
    picture_url = details.find('img')['src']

    return Associate(cipa=cipa,
                     name=name,
                     date_of_birth=date_of_birth,
                     role=role,
                     picture_url=picture_url)
