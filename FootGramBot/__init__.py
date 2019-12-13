import http.client
import json
from telegram.ext import Updater

import config
from competitions import comps as competitions

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
    def find_comp(comp):
        if comp in competitions:
            return competitions[comp]
        else:
            return 'Err! Report this'

    @staticmethod
    def read_data():
        with open('data.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def save_data(data):
        with open('data.json', 'w') as file:
            json.dump(data, file)


updater = Updater(BOT_API, use_context=True)
dp = updater.dispatcher
