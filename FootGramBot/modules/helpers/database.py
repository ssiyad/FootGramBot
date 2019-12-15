import datetime

import peewee

db = peewee.SqliteDatabase("db.db")


class Match(peewee.Model):
    id = peewee.PrimaryKeyField()
    match_id = peewee.IntegerField()
    comp = peewee.IntegerField()
    stage = peewee.CharField()
    group = peewee.CharField()
    winner = peewee.CharField()
    duration = peewee.CharField()
    full_home = peewee.IntegerField()
    full_away = peewee.IntegerField()
    half_home = peewee.IntegerField()
    half_away = peewee.IntegerField()
    extra_home = peewee.IntegerField(default=None)
    extra_away = peewee.IntegerField(default=None)
    pen_home = peewee.IntegerField(default=None)
    pen_away = peewee.IntegerField(default=None)
    home = peewee.CharField()
    away = peewee.CharField()
    updated = peewee.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

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
    updated = peewee.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        database = db
        table_name = 'lives'


# create_tables
Match.create_table()
Live.create_table()
