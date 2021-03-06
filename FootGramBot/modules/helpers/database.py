import datetime

import peewee

db = peewee.SqliteDatabase("db.db")


class Match(peewee.Model):
    id = peewee.PrimaryKeyField()
    match_id = peewee.IntegerField(unique=True)
    comp = peewee.CharField()
    matchday = peewee.IntegerField()
    date_utc = peewee.CharField()
    status = peewee.CharField()
    stage = peewee.CharField(null=True)
    group = peewee.CharField(null=True)
    winner = peewee.CharField(null=True)
    duration = peewee.CharField(null=True)
    full_home = peewee.IntegerField(null=True)
    full_away = peewee.IntegerField(null=True)
    half_home = peewee.IntegerField(null=True)
    half_away = peewee.IntegerField(null=True)
    extra_home = peewee.IntegerField(null=True)
    extra_away = peewee.IntegerField(null=True)
    pen_home = peewee.IntegerField(null=True)
    pen_away = peewee.IntegerField(null=True)
    home = peewee.CharField()
    away = peewee.CharField()
    home_id = peewee.IntegerField()
    away_id = peewee.IntegerField()
    updated = peewee.DateField(default=datetime.datetime.now())

    class Meta:
        database = db
        table_name = 'matches'


class Live(peewee.Model):
    id = peewee.PrimaryKeyField()
    league = peewee.CharField()
    time = peewee.CharField()
    goals_home = peewee.IntegerField()
    goals_away = peewee.IntegerField()
    home = peewee.CharField()
    away = peewee.CharField()
    updated = peewee.DateField(default=datetime.datetime.now())

    class Meta:
        database = db
        table_name = 'lives'


class Team(peewee.Model):
    id = peewee.PrimaryKeyField()
    team_id = peewee.IntegerField()
    name = peewee.CharField()
    short_name = peewee.CharField()
    tla = peewee.CharField()
    crest_url = peewee.CharField()
    address = peewee.CharField()
    phone = peewee.CharField(null=True)
    website = peewee.CharField(null=True)
    email = peewee.CharField(null=True)
    founded = peewee.CharField()
    stadium = peewee.CharField()
    updated = peewee.DateField(default=datetime.datetime.now())

    class Meta:
        database = db
        table_name = 'teams'


class Player(peewee.Model):
    id = peewee.PrimaryKeyField()
    player_id = peewee.IntegerField()
    name = peewee.CharField()
    team = peewee.CharField()
    position = peewee.CharField()
    dob = peewee.CharField()
    born_in = peewee.CharField()
    nationality = peewee.CharField()
    shirt_no = peewee.IntegerField(null=True)
    role = peewee.CharField()
    updated = peewee.DateField(default=datetime.datetime.now())

    class Meta:
        database = db
        table_name = 'players'


class Sub(peewee.Model):
    id = peewee.PrimaryKeyField()
    chat_id = peewee.IntegerField()
    chat_type = peewee.CharField()
    team = peewee.CharField()

    class Meta:
        database = db
        table_name = 'subs'


# create_tables
Match.create_table()
Live.create_table()
Team.create_table()
Player.create_table()
Sub.create_table()
