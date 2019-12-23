from threading import Thread
from time import sleep

import schedule

from FootGramBot import FGM, COMPETITIONS
from FootGramBot.modules.helpers.database import Match, Live


def update_matches():
    for comp in COMPETITIONS:
        _matches = FGM.matches(comp)
        MATCH_DATA = []
        if 'matches' in _matches:
            _matches = _matches['matches']
            for match in _matches:
                d = {'match_id': match['id'],
                     'comp': comp,
                     'matchday': match['season']['currentMatchday'],
                     'date_utc': match['utcDate'],
                     'status': match['status'],
                     'stage': match['stage'],
                     'group': match['group'],
                     'winner': match['score']['winner'],
                     'duration': match['score']['duration'],
                     'full_home': match['score']['fullTime']['homeTeam'],
                     'full_away': match['score']['fullTime']['awayTeam'],
                     'half_home': match['score']['halfTime']['homeTeam'],
                     'half_away': match['score']['halfTime']['awayTeam'],
                     'extra_home': match['score']['extraTime']['homeTeam'],
                     'extra_away': match['score']['extraTime']['awayTeam'],
                     'pen_home': match['score']['penalties']['homeTeam'],
                     'pen_away': match['score']['penalties']['awayTeam'],
                     'home': match['homeTeam']['name'],
                     'away': match['awayTeam']['name'],
                     'home_id': match['homeTeam']['id'],
                     'away_id': match['awayTeam']['id']}

                MATCH_DATA.append(d)
        Match.insert_many(MATCH_DATA).on_conflict('replace').execute()


def update_live():
    live_matches = FGM.live()
    Live.delete().execute()
    if live_matches['games']:
        LIVE_DATA = []
        for match in live_matches['games']:
            d = {'league': match['league'],
                 'time': match['time'],
                 'goals_home': match['goalsHomeTeam'],
                 'goals_away': match['goalsAwayTeam'],
                 'home': match['homeTeamName'],
                 'away': match['awayTeamName']}

            LIVE_DATA.append(d)
        Live.insert_many(LIVE_DATA).on_conflict('replace').execute()


def run_scheduler():
    while True:
        schedule.run_pending()
        sleep(1)


def threaded(job):
    Thread(target=job).start()


schedule.every().day.at('00:00').do(threaded, update_matches)
schedule.every(5).seconds.do(threaded, update_live)

threaded(run_scheduler)
