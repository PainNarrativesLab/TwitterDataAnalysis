"""
Created by adam on 5/19/18
"""
__author__ = 'adam'

import json
import xml.etree.ElementTree as ET

import requests
import environment


def load_credentials_file( filepath=environment.SLACK_CREDENTIAL_FILE ):
    """
    Opens the credentials file and loads the attributes
    """
    return ET.parse( filepath )


def load_webhook_url():
    credentials = load_credentials_file()
    return credentials.find('webhook_url').text


def send_slack_update( text ):
    url = load_webhook_url()
    payload = { "text": text, "icon_emoji": ":ghost:" }
    payload = json.dumps( payload )
    r = requests.post( url, data=payload )
    if r.status_code == 200:
        print( 'slack notified: %s ' % text )


def slack_heartbeat(count, limit=environment.SLACK_HEARTBEAT_LIMIT):
    """Sends a periodic update to slack"""
    mod = count % limit
    if mod == 0:
        txt = "%s tweets processed" % count
        send_slack_update(txt)


if __name__ == '__main__':
    pass
