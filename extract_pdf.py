import requests
import base64
import time


def get_lines(filename):
    api_key = "cd99f6d65b237acf09e2233f54c260b7"
    file = f"https://estatistica.fpa.pt/jogos/{filename}.pdf"
    data = f'{{"apikey":"{api_key}","input":"url","file":"{file}","filename":"","outputformat":"txt","options":""}}'
    print("FETCHING DATA FROM WEBPAGE:")
    response = requests.post('https://api.convertio.co/convert', data=data)
    response_json = response.json()
    print(response_json['code'], ":", response_json['status'])
    id = response_json['data']["id"]
    time.sleep(1)
    file = requests.get(f'https://api.convertio.co/convert/{id}/dl')
    content = file.json()['data']['content']
    lines = base64.b64decode(content).decode('utf-8').splitlines()
    lines = list(filter(None, lines))
    lines = list(filter(filter_prov, lines))
    return lines


def filter_prov(string):
    if "Provisório" in string or 'Observado' in string:
        return False
    else:
        return True
