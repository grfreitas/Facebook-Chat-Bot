#-*- coding: utf-8 -*-

from datetime import datetime
import pytz

tz = pytz.timezone('America/Sao_Paulo')

def fb_msg_handler(info):
    try:
        message_sent_at     = datetime.fromtimestamp(info['entry'][0]['messaging'][0]['timestamp']/1e3, tz=tz)
        message_received_at = datetime.fromtimestamp(info['entry'][0]['time']/1e3, tz=tz)

        message_text = info['entry'][0]['messaging'][0]['message']['text']

        response = 'Mensagem: '+str(message_text)+'\nEnviada em: '+str(message_sent_at)+'\nRecebida em: '+str(message_received_at)

    except Exception as e:
        print(e)
        response = 'Erro.'

    return response
