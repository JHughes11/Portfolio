import psycopg2
from config import config


def fetch_from_tables_and_insert(**kwargs):
    table = kwargs['table']
    foreignTables = kwargs['foreignTables']
    teamHeaders = kwargs['teamHeaders']
    yearsPlayedHeaders = kwargs['yearsPlayedHeaders']
    insertHeaders = kwargs['insertHeaders']
    values = kwargs['values']

    team_id = foreignTables[1] + f'.{teamHeaders[0]}'
    year_id = foreignTables[0] + f'.{yearsPlayedHeaders[0]}'

    # Figure out passing tuple values to execute many
    team_ids = tuple(str(tup[1]) for tup in values)

    foreign_sql = 'SELECT {} from {} WHERE {} = {} AND {} IN {}'.format(
        ','.join([team_id, year_id]),
        ','.join(foreignTables),
        year_id, 1, team_id, team_ids)

    values_to_inject = ""
    header_len = len(insertHeaders)
    for i in range(0, header_len):
        if i == header_len-1:
            values_to_inject += "%s"
        else:
            values_to_inject += "%s, "

    conn = None
    id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(foreign_sql)
        foreign_values = cur.fetchall()

        print(foreign_values)
        insert_teams = "INSERT INTO {}({}) VALUES (%s, %s)".format(
            table, ','.join(teamHeaders + yearsPlayedHeaders))
        print(insert_teams)

        cur.executemany(insert_teams, foreign_values)
        # add_stats_to_teams(list(foreign_values), list(values))
        # cur.executemany(insert_sql, add_stats_to_teams(list(foreign_values), list(values)))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error', error)
    finally:
        if conn is not None:
            conn.close()

    return id
