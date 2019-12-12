import http.client
import json

from telegram.ext import Updater

import config

COMPETITIONS = config.COMPETITIONS
BOT_API = config.BOT_API


class FGM(object):
    @staticmethod
    def matches(comp):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': config.KEY}
        connection.request('GET', f'/v2/competitions/{comp}/matches', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        return response

    @staticmethod
    def live_matches():
        connection = http.client.HTTPConnection('soccer-cli.appspot.com')
        connection.request('GET', '/')
        response = json.loads(connection.getresponse().read().decode())
        return response

    @staticmethod
    def read_data():
        with open('data.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def save_data(data):
        with open('data.json', 'w') as file:
            json.dump(data, file)

    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_file(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)


updater = Updater(BOT_API, use_context=True)
dp = updater.dispatcher
