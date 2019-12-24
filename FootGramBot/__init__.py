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
    def get_team(team_id):
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': config.KEY}
        connection.request('GET', f'/v2/teams/{team_id}', None, headers)
        response = json.loads(connection.getresponse().read().decode())
        return response

    @staticmethod
    def live():
        connection = http.client.HTTPConnection('soccer-cli.appspot.com')
        connection.request('GET', '/')
        response = json.loads(connection.getresponse().read().decode())
        return response

    @staticmethod
    def find_comp(comp):
        if comp in competitions:
            return competitions[comp]
        else:
            return 'Err! Report this'


updater = Updater(BOT_API, use_context=True)
dp = updater.dispatcher
