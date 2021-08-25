# -*- coding: utf8 -*-
import time
import requests
import json
from bs4 import BeautifulSoup
from mailjet_rest import Client

def main_loop():
    while True:
        configFileHandler = open('mail_config.json', encoding='utf-8')
        config = json.load(configFileHandler)
        configFileHandler.close()

        whiteListRequest = requests.get(config['URL_TO_CHECK'])
        soup = BeautifulSoup(whiteListRequest.content, 'html.parser')
        signinElement = soup.find(class_="signin")

        if signinElement.text.find(config['NOT_OPEN_TEXT']) == -1:
            mailjet = Client(auth=(config['MAIL_API_KEY'], config['MAIL_API_SECRET']))
            data = {
                'Recipients': [{"Email": config['MAIL_RECIPIENT_EMAIL']}],
                'FromEmail': config['MAIL_SENDER_EMAIL'],
                'Subject': 'DES PLACES POUR FAILY V !',
                'Text-part': 'GO GO GO !',
                'Html-part': '<p>GO GO GO !</p>',
            }
            result = mailjet.send.create(data=data)
            print(result.status_code)
            print(result.json())
        time.sleep(20)

if __name__ == '__main__':
    main_loop()