#-*- coding: utf-8 -*-

import os
import pytz
from requests import get
from datetime import datetime
from pymessenger.bot import Bot

from weather import get_weather
from correios import get_package_status, get_codes

FB_ACCESS_TOKEN     = os.environ['FB_ACCESS_TOKEN']
CLIMATEMPO_TOKEN    = os.environ['CLIMATEMPO_TOKEN']

bot = Bot(FB_ACCESS_TOKEN)

tz = pytz.timezone('America/Sao_Paulo')

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'Message Sent.'

def msg_handler(info):
    entry = info['entry'][0]
    recipient_id = entry['messaging'][0]['sender']['id']
    try:
        msg_sent_at     = datetime.fromtimestamp(entry['messaging'][0]['timestamp']/1e3, tz=tz)
        msg_received_at = datetime.fromtimestamp(entry['time']/1e3, tz=tz)

        msg_params = entry['messaging'][0]['message']

        # checks if there is text in the message
        if 'text' in msg_params:
            msg_text = msg_params['text'].lower()
        else:
        	msg_text = ''

        # checks if there is nlp in message paramaters
        if 'nlp' in msg_params:
            if 'entities' in msg_params['nlp']:
                msg_nlp_entities = msg_params['nlp']['entities']

        # checks if there is temperature in text and location in nlp entities
        if 'temperatura' in msg_text and 'location' in msg_nlp_entities:
            location = msg_nlp_entities['location'][0]['value'].title()
            send_message(recipient_id, 'Vou ver para você! ^_^')
            response = get_weather(location, CLIMATEMPO_TOKEN)
            send_message(recipient_id, response)

        elif 'rastr' in msg_text:
        	words = [list(x) for x in msg_text.replace(',', '').split()]
        	codes = get_codes()
        	if codes:
        		for code in codes:
        			statuses = get_package_status(code)
        			for status in statuses:
        				send_message(recipient_id, status)

        else:
        	send_message(recipient_id, 'Mensagem: '+str(msg_text)+'\nEnviada em: '+str(msg_sent_at)+'\nRecebida em: '+str(msg_received_at))

    except Exception as e:
        print(e)
        send_message(recipient_id, 'Erro. :poop:')

    return
