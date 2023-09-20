from OBT import create_one_big_table
from relationalTables import create_relational_tables
from dbInsert import insert, fetch_and_insert
from mockData import OBT_VALUES, TEAM_VALUES, YEARS_PLAYED_VALUES, RECORD_VALUES


def main():
    print('Creating ONE BIG TABLE...')
    create_one_big_table()

    OBT_TABLENAME = 'nhl_records'
    OBT_HEADERS = ['years', 'division', 'team_name', 'points', 'wins', 'loss', 'ot']
    insert(table=OBT_TABLENAME, headers=OBT_HEADERS, values=OBT_VALUES)

    print('Creating Relational Tables...')
    create_relational_tables()

    TEAM_TABLENAME = 'team'
    TEAM_HEADERS = ['team_name', 'division']
    insert(table=TEAM_TABLENAME, headers=TEAM_HEADERS, values=TEAM_VALUES)

    YEARS_PLAYED_TABLENAME = 'years_played'
    YEARS_PLAYED_HEADERS = ['year']
    insert(table=YEARS_PLAYED_TABLENAME, headers=YEARS_PLAYED_HEADERS, values=YEARS_PLAYED_VALUES)

    TEAM_YEAR_TABLENAME = 'team_year'
    TEAM_YEAR_HEADERS = ['team_id', 'year_id']
    insert(
        table=TEAM_YEAR_TABLENAME, headers=TEAM_YEAR_HEADERS, values=['team', 'years_played'],
        fetchFromTables=True, tableValues=['team_id', 'year_id'],
        whereClause='WHERE year_id = 1')

    TEAM_YEAR_RECORDS_TABLENAME = 'records'
    TEAM_YEAR_RECORDS_HEADERS = ['team_id', 'year_id',
                                 'team_name', 'year', 'points', 'wins', 'loss', 'ot']
    fetch_and_insert(
        insertionTable=TEAM_YEAR_RECORDS_TABLENAME,
        insertionHeaders=TEAM_YEAR_RECORDS_HEADERS,
        insertionValues=RECORD_VALUES,
        queryTable=['team_year', 'team', 'years_played'],
        queryValues=['team_year.team_id', 'team_year.year_id', 'team.team_name', 'years_played.year'],
        queryClause='''WHERE team_year.team_id IN %s AND team_year.year_id = %s 
                        AND team_year.team_id = team.team_id AND 
                        team_year.year_id = years_played.year_id
                    '''
    )


main()
