from flask import Flask, request
from pymessenger.bot import Bot
from brain import fb_msg_handler
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])

def receive_message():
    
    try:

        if request.method == 'GET':

            token_sent = request.args.get("hub.verify_token")
            return verify_fb_token(token_sent)

        elif request.method == 'POST':
            output = request.get_json()
            for event in output['entry']:
                for info in event['messaging']:
                    if 'message' in info:
                        recipient_id = info['sender']['id']
                        response = fb_msg_handler(info)
                        send_message(recipient_id, response)

        return "Message Processed"

    except Exception as e: 
        print(e)

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()