from telegram.ext import CommandHandler, run_async
from telegram.ext import Filters

from FootGramBot import dp


@run_async
def start(update, context):

    START_MSG = '''
Hello there! I'm bot written in python by @ssiyad . Please pass any feedback to him!

If you'r interested in my source code, it is available at https://github.com/ssiyad/FootGramBot

You can get some help by using `/help` command.

Please help me evolve and keep #Love #Football ;)'''

    context.bot.send_message(chat_id=update.effective_chat.id, text=START_MSG, parse_mode='MARKDOWN')


dp.add_handler(CommandHandler('start', start, filters=Filters.private))
