from peewee import DoesNotExist
from telegram.ext import CommandHandler

from FootGramBot import dp, FGM
from FootGramBot.modules.helpers.database import Team, Match, Player


def team(update, context):
    RESULT_MSG = 'Err!'
    if context.args:
        arg_team_name = ' '.join(context.args)

        try:
            SQUAD = '*SQUAD*:\n'
            res = Team.get(Team.name == arg_team_name)
            sqd = Player.select().where(Player.team == arg_team_name)
            for man in sqd:
                SQUAD += man.name + '\n'
            RESULT_MSG = f'*{res.name}* ({res.tla})\nFounded: _{res.founded}_\nStadium: _{res.stadium}_\n\n' \
                         f'_{res.address}_\n\nPhone: _{res.phone}_\nWebsite: _{res.website}_\nEmail: _{res.email}_\n\n' \
                         f'{SQUAD}'

        except DoesNotExist:
            try:
                team_m = Match.get((Match.home == arg_team_name) or (Match.away == arg_team_name))
                if team_m:
                    DATA = []
                    SQUAD = '*SQUAD*:\n'
                    if team_m.home == arg_team_name:
                        team_m_id = team_m.home_id
                    else:
                        team_m_id = team_m.away_id

                    team_a = FGM.get_team(team_m_id)

                    Team.insert(team_id=team_a['id'],
                                name=team_a['name'],
                                short_name=team_a['shortName'],
                                tla=team_a['tla'],
                                crest_url=team_a['crestUrl'],
                                address=team_a['address'],
                                phone=team_a['phone'],
                                website=team_a['website'],
                                email=team_a['email'],
                                founded=team_a['founded'],
                                stadium=team_a['venue']).on_conflict('replace').execute()

                    for man in team_a['squad']:
                        if man['role'] == 'PLAYER':
                            d = {'player_id': man['id'],
                                 'name': man['name'],
                                 'team': arg_team_name,
                                 'position': man['position'],
                                 'dob': man['dateOfBirth'],
                                 'born_in': man['countryOfBirth'],
                                 'nationality': man['nationality'],
                                 'shirt_no': man['shirtNumber'],
                                 'role': 'player'}
                            DATA.append(d)

                            SQUAD += man['name'] + '\n'

                    Player.insert_many(DATA).on_conflict('replace').execute()

                    RESULT_MSG = f'*{team_a["name"]}* ({team_a["tla"]})\nFounded: _{team_a["founded"]}_\nStadium: _{team_a["venue"]}_\n\n' \
                                 f'_{team_a["address"]}_\n\nPhone: _{team_a["phone"]}_\nWebsite: _{team_a["website"]}_\nEmail: _{team_a["email"]}_\n\n' \
                                 f'{SQUAD}'

            except DoesNotExist:
                RESULT_MSG = "Can't find team."

    context.bot.send_message(update.effective_chat.id, RESULT_MSG, parse_mode="MARKDOWN")


dp.add_handler(CommandHandler('team', team))
