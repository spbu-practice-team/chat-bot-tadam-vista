from peewee import *
from resources import strings

db_name = 'statistics.db'
db = SqliteDatabase(db_name)

class BotStats(Model):
    request = CharField()

    class Meta:
        database = db

def add_stats(event):
    try:
        BotStats.create(request=event)
    except Exception:
        print(strings.STATS_CHANGE_ERROR)
