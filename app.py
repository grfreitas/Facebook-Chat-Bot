from flask import Flask, request
from brain import msg_handler
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']

@app.route("/", methods=['POST'])
def receive_message():
    try:
        output = request.get_json()
        if 'messaging' in output['entry'][0]:
            if 'message' in output['entry'][0]['messaging'][0]:
                msg_handler(output)
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

if __name__ == "__main__":
    app.run(debug=True)
