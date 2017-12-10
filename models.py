import datetime
from peewee import *


DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    '''Entry table in database. Fields below.'''
    title = CharField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now)
    spent = CharField(max_length=100)
    learned = TextField
    resources = TextField

    class Meta:
        database = DATABASE
        order_by = ('-date')

    # Generate new journal entry
    @classmethod
    def create_entry(cls, title, date, spent, learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    date=date,
                    spent=spent,
                    learned=learned,
                    resources=resources
                    )
        except IntegrityError:
            raise ValueError('Title already exists. Enter different title.')


def initialize():
    '''Initializing the database'''
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
