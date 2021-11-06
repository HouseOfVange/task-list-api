import os
from dotenv import load_dotenv
import requests
from flask import jsonify

load_dotenv()

def slack_message(text):
    url = 'https://slack.com/api/chat.postMessage'
    required_params = {
        'channel': 'task-notifications', 
        'text': text
    }
    headers = {
        'Authorization': f'{os.environ.get("SLACK_BOT_TOKEN")}'
    }

    message_to_post = requests.post(url, params=required_params, headers=headers)

    return message_to_post.json