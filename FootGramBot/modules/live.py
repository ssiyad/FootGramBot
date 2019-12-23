from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import dp
from FootGramBot.modules.helpers.database import Live


@run_async
def live(update, context):
    COMPS = []
    LIVE_MSG = 'No live matches! Use /recent or /upcoming to get match list'
    match_data = Live.select()
    for match in match_data:
        if match.league not in COMPS and (match.time.isdigit() or match.time == 'HT'):
            COMPS.append(match.league)

    if COMPS:
        LIVE_MSG = 'Select below to get live scores\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(comp, callback_data='live' + comp)]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

    context.bot.send_message(update.effective_chat.id, LIVE_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


dp.add_handler(CommandHandler('live', live, filters=Filters.private))
