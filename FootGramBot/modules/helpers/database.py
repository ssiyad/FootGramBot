import datetime

import peewee

db = peewee.SqliteDatabase("db.db")


class Match(peewee.Model):
    id = peewee.PrimaryKeyField()
    match_id = peewee.IntegerField()
    comp = peewee.IntegerField()
    matchday = peewee.CharField()
    stage = peewee.CharField()
    group = peewee.CharField()
    winner = peewee.CharField(null=True)
    duration = peewee.CharField()
    full_home = peewee.IntegerField()
    full_away = peewee.IntegerField()
    half_home = peewee.IntegerField()
    half_away = peewee.IntegerField()
    extra_home = peewee.IntegerField(null=True)
    extra_away = peewee.IntegerField(null=True)
    pen_home = peewee.IntegerField(null=True)
    pen_away = peewee.IntegerField(null=True)
    home = peewee.CharField()
    away = peewee.CharField()
    home_id = peewee.IntegerField()
    away_id = peewee.IntegerField()
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
