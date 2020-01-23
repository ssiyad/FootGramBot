from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, run_async, MessageHandler
from telegram.ext import Filters

from FootGramBot import dp
from FootGramBot.modules.helpers.database import Live


KEY_BUTTONS = ['Recent', 'Live', 'Upcoming']


@run_async
def live(update, context):
    COMPS = []
    LIVE_MSG = 'No live matches! Use /recent or /upcoming to get match list'
    match_data = Live.select()
    for match in match_data:
        if match.league not in COMPS and ('UTC' not in match.time and 'FT' not in match.time):
            COMPS.append(match.league)

    if COMPS:
        LIVE_MSG = 'Select below to get live scores\n'

    KEYBOARD = []

    for comp in COMPS:
        but = [InlineKeyboardButton(comp, callback_data='live' + comp)]
        KEYBOARD.append(but)

    REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)
    REPLY_MARKUP_MAIN = ReplyKeyboardMarkup(
        [[KeyboardButton(x) for x in KEY_BUTTONS]], resize_keyboard=True)

    context.bot.send_message(update.effective_chat.id,
                             '_Some competions may not be supported due to pricing issues (service provider)_', parse_mode='MARKDOWN', reply_markup=REPLY_MARKUP_MAIN)
    context.bot.send_message(update.effective_chat.id, LIVE_MSG,
                             parse_mode="MARKDOWN", reply_markup=REPLY_MARKUP)


dp.add_handler(CommandHandler('live', live, filters=Filters.private))
dp.add_handler(MessageHandler(Filters.private & Filters.regex(r'Live'), live))
