from db import connect
from utils import checkTableExists


def create_one_big_table(tablename='nhl_records'):
    if (checkTableExists(tablename) == False):
        print('Table {} Does not Exist - Creating Table...'.format(tablename))
        command = (
            """ CREATE TABLE {} (
                team_id SERIAL PRIMARY KEY,
                years VARCHAR(255) NOT NULL,
                division VARCHAR(255) NOT NULL,
                team_name VARCHAR(255) NOT NULL,
                points INTEGER NOT NULL,
                wins INTEGER NOT NULL,
                loss INTEGER NOT NULL,
                ot INTEGER NOT NULL
            )""".format(tablename)
        )
        connect(commands=command)
    else:
        print('Table {} Already Exists...'.format(tablename))
