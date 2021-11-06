import os
from dotenv import load_dotenv
import requests
from flask import jsonify

load_dotenv()

def slack_message(message):
    '''sends an HTTP POST request to a slack bot. Uses
    the Python package "requests" to send the request.
    Function takes in message as a parameter which will be 
    a string and the body of the message posted by the bot'''

    url = 'https://slack.com/api/chat.postMessage'

    required_params = {
        'channel': 'task-notifications', 
        'text': message
    }
    headers = {
        'Authorization': f'{os.environ.get("SLACK_BOT_TOKEN")}'
    }

    message_to_post = requests.post(url, params=required_params, headers=headers)

    return message_to_post.json