import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import dp, FGM


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


dp.add_handler(CommandHandler('upcoming', upcoming, filters=Filters.private))
