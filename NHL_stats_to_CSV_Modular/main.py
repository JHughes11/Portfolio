
from writeToCSV import writeToCSV
from generateTeamStats import generateTeamStats
from api import buildRequest
import requests

BASE_URL = "https://statsapi.web.nhl.com"
STANDINGS_ENDPOINT = "/api/v1/standings"
MAX_NUMBER_OF_ITERATIONS = 50


def main():
    print('Enter in a starting year: ')
    year1 = int(input())
    print('Enter in an ending year: ')
    year2 = int(input())
    print("StartYear: ", year1, "EndYear: ", year2)

    timesToIterate = year2 - year1
    while (timesToIterate > 0):
        if timesToIterate > MAX_NUMBER_OF_ITERATIONS:
            print(
                f'Too many files to be created, please choose less than {MAX_NUMBER_OF_ITERATIONS} years apart ({timesToIterate})')
            break
        # Work backwards - Startyear + iterator
        startYear = year2 - timesToIterate
        endYear = startYear + 1

        queryParams = {"season": int(f'{startYear}{endYear}'), "expand": "standings.record"}

        url, headers = buildRequest(
            url=BASE_URL, endpoint=STANDINGS_ENDPOINT, queryParams=queryParams)

        timesToIterate -= 1
        try:
            response = requests.request("GET", url=url, headers=headers, data={})
            print("URL: {url}, METHOD: GET, headers={headers}".format(url=url, headers=headers))
            results = response.json()
            print(
                'Response: {code}, Response-time: {time}'.format(code=response.status_code, time=response.elapsed))

            # Write to CSV
            writeToCSV(title=f'NHL Stats {startYear}-{endYear}.csv',
                       headers=['YEAR', 'DIVISION', 'TEAM NAME', 'POINTS', 'WINS', 'LOSSES', 'OT'],
                       # Generate Team Stats
                       rows=generateTeamStats(results=results, year=f'{startYear}-{endYear}'))
        except:
            print("An exception occurred")


main()
