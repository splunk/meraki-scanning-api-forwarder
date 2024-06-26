from flask import Flask, abort, request
import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPLUNK_HEC_URL = os.environ['SPLUNK_HEC_URL']
SPLUNK_HEC_TOKEN = os.environ['SPLUNK_HEC_TOKEN']
MERAKI_VALIDATOR = os.environ['MERAKI_VALIDATOR']
MERAKI_SECRET = os.environ['MERAKI_SECRET']

application = Flask(__name__)
application.logger.setLevel(logging.INFO)


@application.before_request
def log_request_info():
    application.logger.info(f'Request: {request}\n{request.headers}\nARGS={request.args}')


@application.route('/')
def index():
    return 'Flask server is up.'


def send_to_hec(data: dict):
    url = f"{SPLUNK_HEC_URL}/services/collector/event"
    application.logger.info(f'Forwarding data to HEC {url}.')
    resp = requests.post(url, json=data, headers={
        "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}"
    })
    application.logger.info(resp)
    resp.raise_for_status()


@application.route('/meraki', methods=['GET'])
def meraki_get():
    return MERAKI_VALIDATOR


@application.route('/meraki', methods=['POST'])
def meraki_post():
    data = request.get_json()
    secret = data.get('secret')
    if secret == MERAKI_SECRET:
        payload = data.copy()
        del payload['secret']
        hec_event = {
            "event": payload,
            "source": f"cisco_meraki_scanning_api",
            "sourcetype": "json_no_timestamp",
        }
        send_to_hec(data=hec_event)
        return 'Received'
    else:
        abort(403)


if __name__ == '__main__':
    # application.debug = True
    application.run()
