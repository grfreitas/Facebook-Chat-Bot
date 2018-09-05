#-*- coding: utf-8 -*-

from requests import get
from datetime import datetime
from pymessenger.bot import Bot
import os
import pytz


ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
bot = Bot(ACCESS_TOKEN)

tz = pytz.timezone('America/Sao_Paulo')
climatempo_token = os.environ['CLIMATEMPO_TOKEN']

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'Message Sent.'

def get_weather(location):
    id_call = 'http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={}&token={}'.format(location, climatempo_token)

    if len(get(id_call).json()) > 0:
        id = get(id_call).json()[0]['id']

        weather_call = 'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{}/current?token={}'.format(id, climatempo_token)
        weather = get(weather_call).json()

        temperature = weather['data']['temperature']
        condition   = weather['data']['condition']
        humidity    = weather['data']['humidity']
        location    = weather['name'] + '-' + weather['state']

        return 'Em {} está fazendo {} graus Celsius, umidade relativa de {}% e com condição de {}'.format(location, temperature, humidity, condition.lower())
    else:
        return 'Cidade Inválida! Por favor, tente novamente :)'

def msg_handler(info):
    entry = info['entry'][0]
    recipient_id = entry['messaging'][0]['sender']['id']
    try:
        msg_sent_at     = datetime.fromtimestamp(entry['messaging'][0]['timestamp']/1e3, tz=tz)
        msg_received_at = datetime.fromtimestamp(entry['time']/1e3, tz=tz)

        msg_params = entry['messaging'][0]['message']

        if 'text' in msg_params:
            msg_text = msg_params['text'].lower()
        else: msg_text = ''

        if 'nlp' in msg_params:
            if 'entities' in msg_params['nlp']:
                msg_nlp_entities = msg_params['nlp']['entities']

        if 'temperatura' in msg_text and 'location' in msg_nlp_entities:
            location = msg_nlp_entities['location'][0]['value'].title()
            send_message(recipient_id, 'Vou ver para você! ^_^')
            response = get_weather(location)
            send_message(recipient_id, response)

        else: send_message(recipient_id, 'Mensagem: '+str(msg_text)+'\nEnviada em: '+str(msg_sent_at)+'\nRecebida em: '+str(msg_received_at))

    except Exception as e:
        print(e)
        send_message(recipient_id, 'Erro. :poop:')

    return
