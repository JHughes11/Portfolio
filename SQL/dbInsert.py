

import psycopg2
from utils import isTableEmpty
from config import config


def generateInjectionStrings(array):
    numberOfStrings = ""
    array_len = len(array)
    for i in range(0, array_len):
        numberOfStrings += f'%s{"," if i!=array_len-1 else ""}'
    return numberOfStrings


def insert(table, headers, values, fetchFromTables=False, tableValues=None, whereClause=None):
    conn = None
    if (isTableEmpty(tablename=table) == True):
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            data = None
            if (fetchFromTables == True):
                select = 'SELECT {} FROM {} {}'.format(
                    ','.join(tableValues),
                    ','.join(values),
                    whereClause)

                print('Executing Commands', select)
                cur.execute(select)
                data = cur.fetchall()

            sql = "INSERT INTO {}({}) VALUES ({})".format(
                table, ','.join(headers), generateInjectionStrings(array=headers)
            )

            values_to_inject = values if fetchFromTables == False else data
            print('Executing Commands', sql, values_to_inject)
            cur.executemany(sql, values_to_inject)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error in insert: ', error)
        finally:
            if conn is not None:
                print('Insert Finished - Closing connection... ')
                conn.close()
    else:
        print('Table already has values...')


def fetch_and_insert(
    insertionTable,
        insertionHeaders,
        insertionValues,
        queryTable,
        queryValues,
        queryClause):
    conn = None
    if (isTableEmpty(tablename=insertionTable) == True):
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            team_ids = tuple([i[0] for i in list(insertionValues)])
            select = 'SELECT {} FROM {} {}'.format(
                ','.join(queryValues),
                ','.join(queryTable),
                queryClause)

            print('Executing SELECT Command: ', select)
            cur.execute(select, (team_ids, 1))
            data = cur.fetchall()

            insert = "INSERT INTO {}({}) VALUES ({})".format(
                insertionTable,
                ','.join(insertionHeaders),
                generateInjectionStrings(array=insertionHeaders)
            )
            print('Executing INSERT Command: ', insert)

            values_to_insert = [(incomingData[0:2] +
                                 queriedData[2:4] +
                                 incomingData[2:]) for queriedData,
                                incomingData in zip(data, insertionValues)
                                if queriedData[0] == incomingData[0] and queriedData[1] ==
                                incomingData[1]]

            cur.executemany(insert, values_to_insert)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error in fetch_and_insert: ', error)
        finally:
            if conn is not None:
                print('fetch_and_insert Finished - Closing connection... ')
                conn.close()
    else:
        print('Table already has values...')
