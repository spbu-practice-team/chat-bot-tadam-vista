from peewee import SqliteDatabase, Model, CharField, IntegerField

db_name = 'statistics.db'
db = SqliteDatabase(db_name)


class BotStats(Model):
    client = CharField()
    request = CharField()
    count = IntegerField(default=0)

    class Meta:
        database = db


def add_stats(room, event):
    try:
        temp = BotStats.select().where(BotStats.client == room, BotStats.request == event).get()
        temp.count += 1
        temp.save()
    except Exception:
        BotStats.create(client=room, request=event, count=1)
