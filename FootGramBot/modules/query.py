import datetime

from telegram.ext import CallbackQueryHandler, run_async

from FootGramBot import dp, FGM
from FootGramBot.modules.helpers.database import Match, Live


@run_async
def button(update, context):
    query = update.callback_query

    EDIT_MSG = ''

    if 'upcoming' in query.data:
        SCHEDULED = []
        comp = FGM.find_comp(query.data.replace('upcoming', ''))
        EDIT_MSG = 'No Upcoming Matches in ' + comp
        match_data = Match.select().where(Match.status == 'SCHEDULED')
        for match in match_data:
            match_date = datetime.datetime.strptime(match.date_utc, '%Y-%m-%dT%H:%M:%SZ')
            time_diff = match_date - datetime.datetime.utcnow()
            if -1 < time_diff.days < 3:
                if str(match.comp) == query.data.replace('upcoming', ''):
                    SCHEDULED.append(match)

        if SCHEDULED:
            EDIT_MSG = f'*Upcoming {comp} matches*\n'
            for match in SCHEDULED:
                EDIT_MSG += '---\n_' \
                            + datetime.datetime.strptime(match.date_utc, '%Y-%m-%dT%H:%M:%SZ').strftime('%A %d %B %l:%M %p') \
                            + '_\n*' \
                            + match.home \
                            + '* vs *' \
                            + match.away \
                            + '*\n'

    elif 'recent' in query.data:
        FINISHED = []
        comp = FGM.find_comp(query.data.replace('recent', ''))
        match_data = Match.select().where(Match.status == 'FINISHED')
        EDIT_MSG = 'No recent matches in ' + comp
        for match in match_data:
            match_date = datetime.datetime.strptime(match.date_utc, '%Y-%m-%dT%H:%M:%SZ')
            time_diff = match_date - datetime.datetime.utcnow()
            if -4 < time_diff.days < 0:
                if str(match.comp) == query.data.replace('recent', ''):
                    FINISHED.append(match)

        if FINISHED:
            EDIT_MSG = f'*Recent {comp} matches*\n'
            for match in FINISHED:
                EDIT_MSG += '---\n*' \
                            + match.home \
                            + '* _' \
                            + str(match.full_home) \
                            + '_ vs _' \
                            + str(match.full_away) \
                            + '_ *' \
                            + match.away \
                            + '*\n'

    elif 'live' in query.data:
        LIVE = []
        comp = FGM.find_comp(query.data.replace('live', ''))
        match_data = Live.select()
        EDIT_MSG = 'No live matches in ' + comp
        for match in match_data:
            if match.league == query.data.replace('live', '') and 'UTC' not in match.time:
                LIVE.append(match)

        if LIVE:
            EDIT_MSG = f'*Live {comp} matches*\n'
            for match in LIVE:
                EDIT_MSG += '---\n_' \
                            + str(match.time) \
                            + '_  *' \
                            + match.home \
                            + '* _' \
                            + str(match.goals_home) \
                            + '_ vs _' \
                            + str(match.goals_away) \
                            + '_ *' \
                            + match.away \
                            + '*\n'

    context.bot.edit_message_text(text=EDIT_MSG, chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  parse_mode='MARKDOWN')


dp.add_handler(CallbackQueryHandler(button))
