
from db import connect
from utils import checkTableExists


def create_relational_tables():
    commands_list = []
    if (checkTableExists('team') == False):
        print('Table team Does not Exist - Creating Table...')
        commands_list.append(""" 
                CREATE TABLE team (
                    team_id SERIAL PRIMARY KEY,
                    team_name VARCHAR(255) NOT NULL,
                    division VARCHAR(255) NOT NULL
                )
                """)
    if (checkTableExists('years_played') == False):
        print('Table years_played Does not Exist - Creating Table...')
        commands_list.append(""" 
            CREATE TABLE years_played (
                year_id SERIAL PRIMARY KEY,
                year VARCHAR(255) NOT NULL
            )
            """)
    if (checkTableExists('team_year') == False):
        print('Table team_year Does not Exist - Creating Table...')
        commands_list.append(""" 
            CREATE TABLE team_year (
                team_id INTEGER NOT NULL,
                year_id INTEGER NOT NULL,
                PRIMARY KEY (team_id, year_id),
                FOREIGN KEY (year_id)
                    REFERENCES years_played (year_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (team_id)
                    REFERENCES team (team_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)
    if (checkTableExists('records') == False):
        print('Table records Does not Exist - Creating Table...')
        commands_list.append("""
            CREATE TABLE records (
                team_id INTEGER NOT NULL,
                year_id INTEGER NOT NULL,
                team_name VARCHAR(255) NOT NULL,
                year VARCHAR(255) NOT NULL,
                points VARCHAR(255) NOT NULL,
                wins VARCHAR(255) NOT NULL,
                loss VARCHAR(255) NOT NULL,
                ot VARCHAR(255) NOT NULL,
                PRIMARY KEY (year_id, team_id),
                FOREIGN KEY (year_id)
                    REFERENCES years_played (year_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (team_id)
                    REFERENCES team (team_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)

    else:
        print('Table Already Exists...')
    connect(commands=tuple(commands_list))
