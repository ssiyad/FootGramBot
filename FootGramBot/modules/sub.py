from telegram.ext import CommandHandler, run_async

from FootGramBot import dp
from FootGramBot.modules.helpers.database import Live, Sub
from mwt import MWT


@MWT(timeout=60 * 60)
def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def add_to_sub(update, team):
    SUB_MSG = ''
    match_data = Live.select()
    for match in match_data:
        print(team in (match.home, match.away))
        if team in (match.home, match.away):
            Sub.insert(chat_id=update.effective_chat.id,
                       chat_type=update.effective_chat.type,
                       team=team).on_conflict('replace').execute()
            SUB_MSG = f'Added {team} to sub list'
            break
        else:
            SUB_MSG = f'Can not find {team} in /live matches'

    return SUB_MSG


@run_async
def sub(update, context):
    SUB_MSG = 'Syntax is `/sub <team>`'
    if context.args:
        team = ' '.join(context.args)
        if update.effective_chat.type == 'private':
            SUB_MSG = add_to_sub(update, team)

        else:
            if update.effective_chat.all_members_are_administrators \
                    or update.effective_user.id in get_admin_ids(context.bot, update.effective_chat.id):
                SUB_MSG = add_to_sub(update, team)
            else:
                SUB_MSG = 'Admin only command!'

    context.bot.send_message(update.effective_chat.id, SUB_MSG, parse_mode="MARKDOWN")


dp.add_handler(CommandHandler('sub', sub))
