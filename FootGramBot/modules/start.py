from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import dp


@run_async
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello there! I'm a bot made by @ssiyad . Feel free to contact him for any assistance")


dp.add_handler(CommandHandler('start', start, filters=Filters.private))
