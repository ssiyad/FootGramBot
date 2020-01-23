import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, run_async, MessageHandler
from telegram.ext import Filters

from FootGramBot import dp, FGM
from FootGramBot.modules.helpers.database import Match


@run_async
def upcoming(update, context):
    COMPS = []
    SCHEDULED_MSG = 'No Upcoming Matches'
    match_data = Match.select().where(Match.status == 'SCHEDULED')
    for match in match_data:
        match_date = datetime.datetime.strptime(
            match.date_utc, '%Y-%m-%dT%H:%M:%SZ')
        time_diff = match_date - datetime.datetime.utcnow()
        if -1 < time_diff.days < 3:
            if match.comp not in COMPS:
                COMPS.append(match.comp)

    if COMPS:
        SCHEDULED_MSG = 'Choose below to see upcoming matches\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(FGM.find_comp(
            comp), callback_data='upcoming' + str(comp))]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

    context.bot.send_message(update.effective_chat.id, SCHEDULED_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


dp.add_handler(CommandHandler('upcoming', upcoming, filters=Filters.private))
dp.add_handler(MessageHandler(Filters.private & Filters.regex(r'Upcoming'), upcoming))
