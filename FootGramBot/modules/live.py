from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import dp, FGM


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


dp.add_handler(CommandHandler('live', live, filters=Filters.private))
