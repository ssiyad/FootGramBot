import datetime
from threading import Timer

from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import FGM, COMPETITIONS
from FootGramBot import dp, updater


def update_matches():
    MATCH_LIST = []
    for comp in COMPETITIONS:
        _matches = FGM.matches(comp)
        if 'matches' in _matches:
            _matches = _matches['matches']
            for match in _matches:
                match['comp'] = comp
                MATCH_LIST.append(match)

    if MATCH_LIST:
        FGM.save_data(MATCH_LIST)


def update_live():
    live_data = FGM.live_matches()
    LIVE = []
    for match in live_data['games']:
        d = {'homeTeam': {'name': match['homeTeamName']}, 'awayTeam': {'name': match['awayTeamName']},
             'score': {'fullTime': {'homeTeam': str(match['goalsHomeTeam']), 'awayTeam': str(match['goalsAwayTeam'])}},
             'league': match['league'], 'time': str(match['time'])}
        LIVE.append(d)

    FGM.save_file(LIVE, 'live.json')


@run_async
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello there! I'm a bot made by @ssiyad . Feel free to contact him for any assistance")


@run_async
def matches(update, context):
    SCHEDULED = []
    LIVE = []
    FINISHED = []
    SCHEDULED_MSG = 'No Upcoming Matches'
    LIVE_MSG = 'No Live Matches'
    FINISHED_MSG = 'No Finished Matches'
    match_data = FGM.read_data()
    for match in match_data:
        match_date = datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        time_diff = match_date - datetime.datetime.utcnow()
        if -3 < time_diff.days < 3:
            if match['status'] == 'SCHEDULED':
                SCHEDULED.append(match)
            elif match['status'] == 'FINISHED':
                FINISHED.append(match)
            else:
                LIVE.append(match)

    if SCHEDULED:
        SCHEDULED_MSG = 'UPCOMING\n'
        for match in SCHEDULED:
            SCHEDULED_MSG += '---\n' \
                             + datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ').strftime('%A %d %B %l:%M %p') \
                             + '\n**' \
                             + match['homeTeam']['name'] \
                             + '** vs **' \
                             + match['awayTeam']['name'] \
                             + '**\n'

    if LIVE:
        LIVE_MSG = 'LIVE\n'
        for match in LIVE:
            LIVE_MSG += '---\n' \
                        + match['homeTeam']['name'] \
                        + ' vs ' \
                        + match['awayTeam']['name'] \
                        + '\n'

    if FINISHED:
        FINISHED_MSG = 'FINISHED\n'
        for match in FINISHED:
            FINISHED_MSG += '---\n' \
                            + match['homeTeam']['name'] \
                            + ' ' \
                            + str(match['score']['fullTime']['homeTeam']) \
                            + ' vs ' \
                            + str(match['score']['fullTime']['awayTeam']) \
                            + ' ' \
                            + match['awayTeam']['name'] \
                            + '\n'

    context.bot.send_message(update.effective_chat.id, FINISHED_MSG, parse_mode="MARKDOWN")
    context.bot.send_message(update.effective_chat.id, LIVE_MSG, parse_mode="MARKDOWN")
    context.bot.send_message(update.effective_chat.id, SCHEDULED_MSG, parse_mode="MARKDOWN")


@run_async
def live(update, context):
    LIVE_MSG = 'No live matches! Use /matches to get match list'
    live_scores = FGM.read_file('live.json')
    if live_scores:
        LIVE_MSG = 'LIVE\n'
        for score in live_scores:
            LIVE_MSG += '---\n' \
                        + score['time'] \
                        + ' ' \
                        + score['homeTeam']['name'] \
                        + ' ' \
                        + score['score']['fullTimer']['homeTeam'] \
                        + ' vs ' \
                        + score['fullTime']['awayTeam'] \
                        + ' ' \
                        + score['awayTeam']['name'] \
                        + '\n'

    context.bot.send_message(update.effective_chat.id, LIVE_MSG, parse_mode="MARKDOWN")


def timer_func():
    Timer(10.0, timer_func).start()
    update_matches()


def timer_func2():
    Timer(4.0, timer_func2).start()
    update_live()


def main():
    timer_func()
    timer_func2()
    FGM.live_matches()
    dp.add_handler(CommandHandler('start', start, filters=Filters.private))
    dp.add_handler(CommandHandler('matches', matches, filters=Filters.private))
    dp.add_handler(CommandHandler('live', live, filters=Filters.private))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
