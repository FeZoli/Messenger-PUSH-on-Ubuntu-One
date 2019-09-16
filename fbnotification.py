#!/usr/bin/python

import signal
import sys
import requests
import json
from datetime import datetime, timedelta

from fbchat import Client
from fbchat.models import *

DEBUG = True
LOG_FILENAME = "debug.log"

USER = "<your facebook login email>"
PASSWORD = "<your facebook login password>"

UBUNTU_ONE_URL = "https://push.ubports.com/notify"
HEADERS = {"Content-Type" : "application/json"}

card = {
    "icon" : "notification",
    "body" : "",
    "summary" : "Messenger",
    "popup" : True,
    "persist" : True
}

notification = {
    "card" : card,
    "vibrate" : True,
    "sound"   : True
    }

data = {
    "notification" : notification,
    }

params = {
    "appid" : "pushclient.christianpauly_pushclient",
    "token" : "<your ubuntu one app token>",
    "expire_on" : "",
    "data" : data
}


client = None
logfile = None

def log(log_msg):
    if DEBUG:
        logfile.write(f'{str(log_msg)}\n')
        logfile.flush()
def signal_handler(sig, frame):
    log('Exiting with signal {sig}')
    if client and client.isLoggedIn():
        client.logout()
    if logfile:
        logfile.close()
    sys.exit(0)


class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        if not DEBUG and author_id == self.uid:
            return
        dt = datetime.now() + timedelta(days=1)
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:00.000Z")
        if message_object:
            if message_object.text:
                body = message_object.text[:15]
            else:
                body = "Media content received"
            params["expire_on"] = dt_str
            params["data"]["notification"]["card"]["body"] = body
            json_data = json.dumps(params)
            log(f'Data sent:\n {json_data}\n')
            r = requests.post(url=UBUNTU_ONE_URL, headers=HEADERS, data=json_data)
            log(r.json())

##################### MAIN #####################
if __name__ == "__main__":

    if DEBUG:
        print(f'Loggin in: {LOG_FILENAME}')
        logfile = open(LOG_FILENAME, "a")

    client = CustomClient(USER, PASSWORD)

    log(f'User logged in: {client.isLoggedIn()}')
    log(client.getSession())

    signal.signal(signal.SIGINT, signal_handler)

    client.listen()

    Change <your facebook login ema
