import base64
import time

import requests

from fetching_data.aux_fun import filter_prov


def get_lines(filename, api_key):
    file_location = f"https://estatistica.fpa.pt/jogos/{filename}.pdf"
    data = f'{{"apikey":"{api_key}","input":"url","file":"{file_location}","filename":"","outputformat":"txt","options":""}}'
    print(f"FETCHING DATA FROM WEBPAGE: {filename}.pdf")
    response = requests.post('https://api.convertio.co/convert', data=data)
    response_json = response.json()
    print(response_json['code'], ":", response_json['status'])
    if response_json['code'] != 200:
        print(response_json['error'])
    try:
        time.sleep(2)
        id = response_json['data']["id"]
        file = requests.get(f'https://api.convertio.co/convert/{id}/dl')
        content = file.json()['data']['content']
    except KeyError:
        try:
            print("Key Error:Trying again:")
            time.sleep(3)
            id = response_json['data']["id"]

            file = requests.get(f'https://api.convertio.co/convert/{id}/dl')
            content = file.json()['data']['content']
        except KeyError:
            try:
                print("Key Error 2: Trying again:")
                time.sleep(5)
                id = response_json['data']["id"]

                file = requests.get(f'https://api.convertio.co/convert/{id}/dl')
                content = file.json()['data']['content']
            except KeyError:
                return [], response_json['error']  #
    lines = base64.b64decode(content).decode('utf-8')
    lines = lines.replace('\r\n\r\n', '\r\n').splitlines()
    lines = list(filter(None, lines))
    lines = list(filter(filter_prov, lines))

    return lines, response_json['code']
