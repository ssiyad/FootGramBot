import datetime
from threading import Timer

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import escape_markdown
from telegram.ext import CommandHandler, CallbackQueryHandler, run_async
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


@run_async
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello there! I'm a bot made by @ssiyad . Feel free to contact him for any assistance")


@run_async
def upcoming(update, context):
    SCHEDULED = []
    COMPS = []
    SCHEDULED_MSG = 'No Upcoming Matches'
    match_data = FGM.read_data()
    for match in match_data:
        match_date = datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        time_diff = match_date - datetime.datetime.utcnow()
        if -1 < time_diff.days < 3:
            if match['status'] == 'SCHEDULED':
                if match['comp'] not in COMPS:
                    COMPS.append(match['comp'])
                SCHEDULED.append(match)

    if SCHEDULED:
        SCHEDULED_MSG = 'Choose below to see upcoming matches\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(FGM.find_comp(str(comp)), callback_data='upcoming' + str(comp))]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

    context.bot.send_message(update.effective_chat.id, SCHEDULED_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


@run_async
def recent(update, context):
    FINISHED = []
    COMPS = []
    FINISHED_MSG = 'No Recent Matches'
    match_data = FGM.read_data()
    for match in match_data:
        match_date = datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        time_diff = match_date - datetime.datetime.utcnow()
        if -4 < time_diff.days < 0:
            if match['status'] == 'FINISHED':
                if match['comp'] not in COMPS:
                    COMPS.append(match['comp'])
                FINISHED.append(match)

    if FINISHED:
        FINISHED_MSG = 'Select below to get recent matches\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(FGM.find_comp(str(comp)), callback_data='recent' + str(comp))]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

    context.bot.send_message(update.effective_chat.id, FINISHED_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


@run_async
def live(update, context):
    LIVE = []
    COMPS = []
    LIVE_MSG = 'No live matches! Use /recent or /upcoming to get match list'
    match_data = FGM.read_data()
    for match in match_data:
        if match['status'] == 'IN_PLAY':
            if match['comp'] not in COMPS:
                COMPS.append(match['comp'])
            LIVE.append(match)

    if LIVE:
        LIVE_MSG = 'Select below to get live scores\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(FGM.find_comp(str(comp)), callback_data='live' + str(comp))]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

    context.bot.send_message(update.effective_chat.id, LIVE_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


@run_async
def button(update, context):
    query = update.callback_query

    EDIT_MSG = ''

    if 'upcoming' in query.data:
        SCHEDULED = []
        comp = FGM.find_comp(query.data.replace('upcoming', ''))
        EDIT_MSG = 'No Upcoming Matches in ' + comp
        match_data = FGM.read_data()
        for match in match_data:
            match_date = datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            time_diff = match_date - datetime.datetime.utcnow()
            if -1 < time_diff.days < 3:
                if match['status'] == 'SCHEDULED' and str(match['comp']) == query.data.replace('upcoming', ''):
                    SCHEDULED.append(match)

        if SCHEDULED:
            EDIT_MSG = f'*Upcoming {comp} matches*\n'
            for match in SCHEDULED:
                EDIT_MSG += '---\n_' \
                            + datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ').strftime('%A %d %B %l:%M %p') \
                            + '_\n*' \
                            + match['homeTeam']['name'] \
                            + '* vs *' \
                            + match['awayTeam']['name'] \
                            + '*\n'

    elif 'recent' in query.data:
        FINISHED = []
        comp = FGM.find_comp(query.data.replace('recent', ''))
        match_data = FGM.read_data()
        EDIT_MSG = 'No recent matches in ' + comp
        for match in match_data:
            match_date = datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            time_diff = match_date - datetime.datetime.utcnow()
            if -4 < time_diff.days < 0:
                if match['status'] == 'FINISHED' and str(match['comp']) == query.data.replace('recent', ''):
                    FINISHED.append(match)

        if FINISHED:
            EDIT_MSG = f'*Recent {comp} matches*\n'
            for match in FINISHED:
                EDIT_MSG += '---\n*' \
                            + match['homeTeam']['name'] \
                            + '* _' \
                            + str(match['score']['fullTime']['homeTeam']) \
                            + '_ vs _' \
                            + str(match['score']['fullTime']['awayTeam']) \
                            + '_ *' \
                            + match['awayTeam']['name'] \
                            + '*\n'

    elif 'live' in query.data:
        LIVE = []
        comp = FGM.find_comp(query.data.replace('live', ''))
        match_data = FGM.read_data()
        EDIT_MSG = 'No live matches in ' + comp
        for match in match_data:
            if match['status'] == 'IN_PLAY' and str(match['comp']) == query.data.replace('live', ''):
                LIVE.append(match)

        if LIVE:
            EDIT_MSG = f'*Live {comp} matches*\n'
            for match in LIVE:
                EDIT_MSG += '---\n*' \
                            + match['homeTeam']['name'] \
                            + '* _' + str(match['score']['fullTime']['homeTeam']) \
                            + '_ vs _' \
                            + str(match['score']['fullTime']['awayTeam']) \
                            + '_ *' \
                            + match['awayTeam']['name'] \
                            + '*\n'

    context.bot.edit_message_text(text=EDIT_MSG, chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  parse_mode='MARKDOWN')


def timer_func():
    Timer(60.0, timer_func).start()
    update_matches()


def main():
    # timer_func()
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('start', start, filters=Filters.private))
    dp.add_handler(CommandHandler('recent', recent, filters=Filters.private))
    dp.add_handler(CommandHandler('upcoming', upcoming, filters=Filters.private))
    dp.add_handler(CommandHandler('live', live, filters=Filters.private))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
