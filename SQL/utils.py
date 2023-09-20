import psycopg2
from config import config


def isTableEmpty(tablename):
    conn = None
    try:
        # Grab parameters from config
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*) FROM {0} LIMIT 1
        """.format(tablename.replace('\'', '\'\'')))
        if cur.fetchone()[0] == 0:
            cur.close()
            return True

        cur.close()
        return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def checkTableExists(tablename):
    conn = None
    try:
        # Grab parameters from config
        params = config()

        print('Connecting to the database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
        if cur.fetchone()[0] == 1:
            cur.close()
            return True

        cur.close()
        return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
