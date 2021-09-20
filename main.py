# -*- coding: utf8 -*-
import requests
import json
from bs4 import BeautifulSoup
from mailjet_rest import Client
from datetime import datetime
from pathlib import Path

def main_loop():
    base_path = Path(__file__).parent
    file_path = (base_path / "mail_config.csv").resolve()
    configFileHandler = open(file_path, encoding='utf-8')
    config = json.load(configFileHandler)
    configFileHandler.close()

    whiteListRequest = requests.get(config['URL_TO_CHECK'])
    soup = BeautifulSoup(whiteListRequest.content, 'html.parser')
    signinElement = soup.find(class_="signin")
    today = datetime.now()

    if signinElement.text.find(config['NOT_OPEN_TEXT']) == -1:
        mailjet = Client(auth=(config['MAIL_API_KEY'], config['MAIL_API_SECRET']))
        data = {
            'Recipients': [{"Email": config['MAIL_RECIPIENT_EMAIL']}],
            'FromEmail': config['MAIL_SENDER_EMAIL'],
            'Subject': 'DES PLACES POUR FAILY V !',
            'Text-part': 'GO GO GO !',
            'Html-part': '<a href="' + config['URL_TO_CHECK'] + '">GO GO GO !</p> ',
        }
        result = mailjet.send.create(data=data)

        with open('entry.log', 'a') as the_file:
            the_file.write('[' + today.strftime("%d/%m/%Y %H:%M:%S") + '] OPENNNNNNNNNNNNNNN\n')
    else:
        with open('entry.log', 'a') as the_file:
            the_file.write('[' + today.strftime("%d/%m/%Y %H:%M:%S") + '] Close\n')


if __name__ == '__main__':
    main_loop()
