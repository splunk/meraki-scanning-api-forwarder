from flask import Flask, request
import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPLUNK_HEC_URL = os.environ['SPLUNK_HEC_URL']
SPLUNK_HEC_TOKEN = os.environ['SPLUNK_HEC_TOKEN']

application = Flask(__name__)
application.logger.setLevel(logging.INFO)


@application.before_request
def log_request_info():
    application.logger.info(f'Request: {request}\n{request.headers}\nARGS={request.args}\nBODY={request.get_data()}')


@application.route('/')
def index():
    param = request.args.get('x', default='World')
    return f'Hello {param}!'


def send_to_hec(data: dict):
    url = f"{SPLUNK_HEC_URL}/services/collector/event"
    application.logger.info(f'Forwarding data to {url}')
    resp = requests.post(url, json=data, headers={
        "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}"
    })
    application.logger.info(resp)
    resp.raise_for_status()


@application.route('/meraki', methods=['GET'])
def meraki_get():
    return 'GET'


@application.route('/meraki', methods=['POST'])
def meraki_post():
    # TODO: filter traffic from Meraki only
    # Maybe configure this as the AWS SG level
    data = request.get_json()
    application.logger.info(f'POST JSON data: f{data}')
    send_to_hec(data={"event": data})
    return 'Received'


if __name__ == '__main__':
    application.debug = True
    application.run()
