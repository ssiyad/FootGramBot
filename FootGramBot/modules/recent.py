import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import dp, FGM


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


dp.add_handler(CommandHandler('recent', recent, filters=Filters.private))
