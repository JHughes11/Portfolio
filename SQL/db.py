import psycopg2
from config import config


def getAvailableTables(dbCursor):
    dbCursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    print('Tables Available: ')
    for table in dbCursor.fetchall():
        print(table)


def connect(commands=None):
    conn = None
    try:
        # Grab parameters from config
        params = config()
        print('Connecting to the database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        getAvailableTables(dbCursor=cur)

        if commands is not None:
            if type(commands) is tuple:
                for command in commands:
                    try:
                        cur.execute(command)
                    except (Exception) as error:
                        print(error)
            else:
                print('Executing Comands...', commands)
                cur.execute(commands)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
