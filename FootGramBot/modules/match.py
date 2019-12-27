import datetime

from telegram.ext import CommandHandler

from FootGramBot import dp
from FootGramBot.modules.helpers.database import Match, Live


def search_match(update, context):
    if context.args:
        FINISHED = []
        SCHEDULED = []
        LIVE = []
        query_raw = ' '.join(context.args)
        query = query_raw.lower()
        SEARCH_MSG = f'No results for {query}'
        count = 0
        RESULTS = Match.select()
        for result in RESULTS:
            match_date = datetime.datetime.strptime(result.date_utc, '%Y-%m-%dT%H:%M:%SZ')
            time_diff = match_date - datetime.datetime.utcnow()
            if -4 < time_diff.days < 5:
                if count < 20:
                    if query in result.home.lower() or query in result.away.lower():
                        if result.status == 'FINISHED':
                            FINISHED.append(result)
                            count += 1

                        elif result.status == 'SCHEDULED':
                            SCHEDULED.append(result)
                        count += 1
                else:
                    break

        LIVE_MATCHES = Live.select()
        for result in LIVE_MATCHES:
            if query in result.home.lower() or query in result.away.lower():
                if 'UTC' not in result.time and 'FT' not in result.time:
                    LIVE.append(result)

        if FINISHED or SCHEDULED or LIVE:
            SEARCH_MSG = f'Results for {query_raw}\n---\n\n'

        if FINISHED:
            SEARCH_MSG += f'Recent matches\n'
            for result in FINISHED:
                SEARCH_MSG += '---\n*' \
                              + result.home \
                              + '* _' \
                              + str(result.full_home) \
                              + '_ vs _' \
                              + str(result.full_away) \
                              + '_ *' \
                              + result.away \
                              + '*\n'

        if SCHEDULED:
            if FINISHED:
                SEARCH_MSG += f'---\n\nUpcoming matches\n'
            else:
                SEARCH_MSG += f'Upcoming matches\n'
            for result in SCHEDULED:
                SEARCH_MSG += '---\n_' \
                              + datetime.datetime.strptime(result.date_utc, '%Y-%m-%dT%H:%M:%SZ').strftime('%A %d %B %l:%M %p') \
                              + '_\n*' \
                              + result.home \
                              + '* vs *' \
                              + result.away \
                              + '*\n'

        if LIVE:
            if FINISHED or SCHEDULED:
                SEARCH_MSG += f'---\n\nLive matches\n'
            else:
                SEARCH_MSG += f'Live matches\n'
            for result in LIVE:
                SEARCH_MSG += '---\n_' \
                              + str(result.time) \
                              + '_ *' \
                              + result.home \
                              + '* _' \
                              + str(result.goals_home) \
                              + '_ vs _' \
                              + str(result.goals_away) \
                              + '_ *' \
                              + result.away \
                              + '*\n'

    else:
        SEARCH_MSG = 'Err!'

    context.bot.send_message(update.effective_chat.id, SEARCH_MSG, parse_mode="MARKDOWN")


dp.add_handler(CommandHandler('match', search_match))
