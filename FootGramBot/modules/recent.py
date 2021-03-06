import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, run_async, MessageHandler
from telegram.ext import Filters

from FootGramBot import dp, FGM
from FootGramBot.modules.helpers.database import Match


@run_async
def recent(update, context):
    COMPS = []
    FINISHED_MSG = 'No Recent Matches'
    match_data = Match.select().where(Match.status == 'FINISHED')
    for match in match_data:
        match_date = datetime.datetime.strptime(
            match.date_utc, '%Y-%m-%dT%H:%M:%SZ')
        time_diff = match_date - datetime.datetime.utcnow()
        if -4 < time_diff.days < 0:
            if match.comp not in COMPS:
                COMPS.append(match.comp)

    if COMPS:
        FINISHED_MSG = 'Select below to get recent matches\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(FGM.find_comp(
            comp), callback_data='recent' + str(comp))]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

    context.bot.send_message(update.effective_chat.id, FINISHED_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


dp.add_handler(CommandHandler('recent', recent, filters=Filters.private))
dp.add_handler(MessageHandler(Filters.private & Filters.regex(r'Recent'), recent))
