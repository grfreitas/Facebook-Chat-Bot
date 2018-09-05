from flask import Flask, request
from pymessenger.bot import Bot
from brain import fb_msg_handler
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['POST'])
def receive_message():
    try:
        output = request.get_json()
        if 'messaging' in output['entry'][0]:
            if 'message' in output['entry'][0]['messaging'][0]:
                recipient_id = output['entry'][0]['messaging'][0]['sender']['id']
                response = fb_msg_handler(output)
                send_message(recipient_id, response)
        return 'Message Processed.'
    except Exception as e:
        print(e)
        return 'Error.'

@app.route("/", methods=['GET'])
def verify_token():
    token_sent = request.args.get('hub.verify_token')
    if token_sent == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid Verification Token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return 'Message Sent.'

if __name__ == "__main__":
    app.run(debug=True)
