from telegram.ext import CommandHandler

from FootGramBot import dp


def show_help(update, context):
    HELP_MSG = '''
Hello! How can I help you?

`/start`:       Start the bot
`/recent`:      Get recent matches with scores
`/live`:        Get live matches with scores
`/upcoming`:    Get upcoming fixtures

Group Commands:
`Coming Soon!`'''

    context.bot.send_message(update.effective_chat.id, HELP_MSG, parse_mode="MARKDOWN")


dp.add_handler(CommandHandler('help', show_help))
